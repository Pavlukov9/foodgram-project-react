from django.core.validators import (RegexValidator,
                                    MinValueValidator,
                                    MaxValueValidator)
from django.db import models

import constants
from users.models import User


class Tag(models.Model):

    name = models.CharField(
        'Название',
        max_length=constants.LENGTH_TAG_NAME,
        blank=False,
        unique=True
    )
    color = models.CharField(
        'Цвет',
        max_length=7,
        blank=False,
        unique=True,
        validators=[
            RegexValidator(
                regex="^#([a-f0-9]{6}|[a-f0-9]{3})$",
                message='Неправильный формат ввода',
            )
        ]
    )
    slug = models.SlugField(
        'Слаг',
        blank=False,
        unique=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег',
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингредиента',
        max_length=constants.LENGTH_INGREDIENT_NAME
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=constants.LENGTH_INGREDIENT_MEASUREMENT_UNIT
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент',
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_name_measurement_unit'
            )
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField(
        'Название рецепта',
        max_length=constants.LENGTH_RECIPE_NAME
    )
    image = models.ImageField(
        'Картинка',
        upload_to='media/'
    )
    text = models.CharField(
        'Описание рецепта',
        max_length=constants.LENGTH_RECIPE_TEXT
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[
            MinValueValidator(
                1, 'Время приготовления не может быть меньше 1 минуты.'
            ),
            MaxValueValidator(
                180, 'Время приготовления не может быть больше 180 минут.'
            )
        ]
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipeingredients',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipeingredients',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveIntegerField(
        'Количество ингредиента',
        blank=False,
        validators=[
            MinValueValidator(
                1, 'Кол-во ингредиентов не может быть меньше 1!'
            ),
            MaxValueValidator(
                15, 'Кол-во ингредиентов не может быть больше 15!'
            )
        ]
    )

    class Meta:
        ordering = ['recipe']
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]


class FavoriteShoppingCart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        abstract = True


class Favorite(FavoriteShoppingCart):

    class Meta:
        default_related_name = 'favorites'
        ordering = ['user']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user.username} добавил {self.recipe.name} в избранное.'


class ShoppingCart(FavoriteShoppingCart):

    class Meta:
        default_related_name = 'carts'
        ordering = ['user']
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'

    def __str__(self):
        return (f'{self.user.username} добавил'
                f'{self.recipe.name} в список покупок.')
