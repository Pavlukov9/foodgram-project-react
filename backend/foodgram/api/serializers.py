from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipes.models import (Recipe, Tag, Ingredient,
                            RecipeIngredient, Favorite,
                            ShoppingCart)
from users.models import User, Follow
from .utils import Base64ImageField


class UserSerializer(serializers.ModelSerializer):

    """Сериализатор для проверки подписан ли пользователь."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id',
                  'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and obj.followed.filter(user=user).exists()
        )


class FollowSerializer(UserSerializer):

    """Serializer для модели Follow. Всё о подписки пользователя"""

    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, author):
        return author.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.recipes.all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return RecipeMiniSerializer(recipes, many=True).data


class FollowUserSerializer(serializers.ModelSerializer):

    """Serializer для модели Follow.
    Всё о подписки пользователя,связанное с пользователями."""

    class Meta:
        model = Follow
        fields = '__all__'

    def validate(self, data):
        user = self.context.get('request').user
        result = user.follower.filter(author=data.follower).exists()
        if result:
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя!'
            )
        if user == data.followed:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return data


class RecipeMiniSerializer(serializers.ModelSerializer):
    """Сериализатор предназначен для вывода рецептом в FollowSerializer."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image',)


class IngredientSerializer(serializers.ModelSerializer):
    """Список ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = '__all__',


class TagSerializer(serializers.ModelSerializer):
    """Список тегов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = '__all__',

    def validate_tags(self, value):
        tags = value
        if not tags:
            raise serializers.ValidationError(
                'Нужен минимум один тег!'
            )

        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise serializers.ValidationError(
                    'Теги не должны повторяться!'
                )
            tags_list.append(tag)

        return value


class RecipeIngridientSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода кол-ва ингредиентов."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class AddIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления ингредиентов"""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')

    def validate_amount(self, value):
        amount = value
        if amount == 0:
            raise serializers.ValidationError(
                'Количество ингредиентов должно быть больше нуля!'
            )
        return value


class RecipeListSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов"""

    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer()
    ingredients = RecipeIngridientSerializer(many=True, read_only=True,
                                             source='recipeingredients')
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return (user.is_authenticated
                and user.favorites.filter(recipe=obj).exists())

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return (user.is_authenticated
                and user.carts.filter(recipe=obj).exists())


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления рецептов"""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = AddIngredientSerializer(many=True, write_only=True)
    image = Base64ImageField()
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Recipe
        fields = ('author', 'ingredients', 'tags',
                  'image', 'name', 'text', 'cooking_time')

    def validate_ingredients(self, value):
        ingredients = value
        if not ingredients:
            raise serializers.ValidationError(
                {'ingredients': 'Нужно выбрать ингредиент!'})
        ingredients_list = []
        for item in ingredients:
            ingredient = get_object_or_404(Ingredient, name=item['id'])
            if ingredient in ingredients_list:
                raise serializers.ValidationError(
                    {'ingredients': 'Ингридиенты повторяются!'})
            ingredients_list.append(ingredient)
        return value

    def validate_cooking_time(self, value):
        cooking_time = value
        if not cooking_time:
            raise serializers.ValidationError(
                {'cooking_time': 'Нужно указать время приготовления!'}
            )
        return value

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeListSerializer(instance, context=context).data

    @staticmethod
    def add_tags_ingredients(ingredients, tags, model):
        for ingredient in ingredients:
            RecipeIngredient.objects.update_or_create(
                recipe=model,
                ingredient=ingredient['id'],
                amount=ingredient['amount'])
        model.tags.set(tags)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        self.add_tags_ingredients(ingredients, tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.ingredients.clear()
        self.add_tags_ingredients(ingredients, tags, instance)
        return super().update(instance, validated_data)


class FavoriteShoppingCartSerializer(serializers.ModelSerializer):
    """Общий сериализатор для избранного и списка покупок. """

    name = serializers.ReadOnlyField(
        source='recipe.name',
        read_only=True)
    image = serializers.ImageField(
        source='recipe.image',
        read_only=True)
    coocking_time = serializers.IntegerField(
        source='recipe.cooking_time',
        read_only=True)
    id = serializers.PrimaryKeyRelatedField(
        source='recipe',
        read_only=True)


class FavoriteSerializer(FavoriteShoppingCartSerializer):
    """Сериализатор для избранного."""

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'coocking_time')


class ShoppingCartSerializer(FavoriteShoppingCartSerializer):
    """Сериализатор для списка покупок."""

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'coocking_time')
