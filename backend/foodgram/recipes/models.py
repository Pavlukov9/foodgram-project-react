from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=100,
        blank=False,
        unique=True
    )
    color = models.CharField(
        'Цвет',
        max_length=7,
        blank=False,
        unique=True
    )
    slug = models.SlugField(
        'Слаг',
        blank=False,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег',
        verbose_name_plural = 'Теги'
    
    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингредиента',
        max_length=100,
        blank=False
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=100
    )

    class Meta:
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
        null=True
    )
    name = models.CharField(
        'Название рецепта',
        max_length=256,
        blank=False
    )
    image = models.ImageField(
        'Картинка',
        upload_to='media/',
        blank=False
    )
    text = models.CharField(
        'Описание рецепта',
        max_length=500,
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
                1, 'Время приготовления не может быть меньше 1 минуты'
            )
        ]
    )

    class Meta:
        ordering = ['-id']
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
            )
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
        null=True
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
        null=True
    )

    class Meta:
        ordering = ['-id']
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
        null=True
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Рецепт',
        null=True
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        

    def __str__(self):
        return f'{self.user.username} добавил {self.recipe.name} в список покупок.'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='follower',
        on_delete=models.CASCADE
        )
    author = models.ForeignKey(
        User,
        verbose_name='Подписка',
        related_name='followed',
        on_delete=models.CASCADE,
        )

    class Meta:
        verbose_name = 'Мои подписки'
        verbose_name_plural = 'Мои подписки'

    def __str__(self):
        return f'Пользователь {self.user} подписан на {self.author}'