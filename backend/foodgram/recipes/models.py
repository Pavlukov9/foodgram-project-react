from colorfield.fields import ColorField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

import constants
from users.models import User


class Tag(models.Model):

    #COLOR_PALETTE = [
    #    ('#00ff00', 'green'),
    #    ('#ffff00', 'yellow'),
    #    ('#ff0000', 'red')
    #]

    name = models.CharField(
        'Название',
        max_length=constants.LENGTH_TAG_NAME,
        blank=False,
        unique=True
    )
    color = models.CharField(
        'Цвет',
        #choices=COLOR_PALETTE,
        max_length=constants.LENGTH_TAG_COLOR,
        blank=False,
        unique=True
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
        max_length=constants.LENGTH_INGREDIENT_NAME,
        blank=False
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=constants.LENGTH_INGREDIENT_MEASUREMENT_UNIT
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент',
        verbose_name_plural = 'Ингредиенты'

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
        max_length=constants.LENGTH_RECIPE_NAME,
        blank=False
    )
    image = models.ImageField(
        'Картинка',
        upload_to='media/',
        blank=False
    )
    text = models.CharField(
        'Описание рецепта',
        max_length=constants.LENGTH_RECIPE_TEXT,
        blank=False
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
        blank=False
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        blank=False
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
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'


#class FavoriteShoppingCart(models.Model):
 #   user = models.ForeignKey(
 #       User,
 #       on_delete=models.CASCADE,
 #       related_name='favorites',
 #       verbose_name='Пользователь',
 #       null=True
 #   )
 #   recipe = models.ForeignKey(
 #       Recipe,
 #       on_delete=models.CASCADE,
 #       related_name='favorites',
 #       verbose_name='Рецепт',
 #       null=True
  #  )


class Favorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.user.username} добавил {self.recipe.name} в избранное.'


class ShoppingCart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'

    def __str__(self):
        return (f'{self.user.username} добавил'
                f'{self.recipe.name} в список покупок.')
