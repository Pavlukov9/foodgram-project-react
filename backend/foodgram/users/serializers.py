from djoser.serializers import UserSerializer
from rest_framework import serializers


from recipes.models import Recipe
from .models import User, Follow


class UserSerializer(UserSerializer):

    """Сериализатор для проверки подписан ли пользователь."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id',
                  'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        else:
            subscribe = Follow.objects.filter(user=user, author=obj).exists()
            if subscribe:
                return subscribe
            else:
                return False


class RecipeMiniSerializer(serializers.ModelSerializer):
    """Сериализатор предназначен для вывода рецептом в FollowSerializer."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image',)


class FollowSerializer(serializers.ModelSerializer):

    """Serializer для модели Follow. Всё о подписки пользователя"""

    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    # Найдем кол-во рецептов и рецепты, на которые подписан пользователь.
    def get_recipes_count(self, author):
        return Recipe.objects.filter(author=author).count()

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
        model = User
        fields = fields = ('email', 'id', 'username', 'first_name',
                           'last_name')

    def validate(self, data):
        user = self.context.get('request').user
        result = Follow.objects.filter(author=data['author'],
                                       user=user).exists()
        if result:
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя!'
            )
        if user == data['author']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return data
