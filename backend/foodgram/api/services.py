from datetime import date

from django.db.models import Sum
from django.http import FileResponse

from recipes.models import RecipeIngredient


def download_shopping_cart(self, request, author):
    """Скачивание списка продуктов для выбранных рецептов пользователя."""
    sum_ingredients_in_recipes = RecipeIngredient.objects.filter(
        recipe__shopping_cart__author=author
    ).values(
        'ingredient__name', 'ingredient__measurement_unit'
    ).annotate(
        amounts=Sum('amount', distinct=True)).order_by('amounts')
    today = date.today().strftime("%d-%m-%Y")
    shopping_list = f'Список покупок на: {today}\n\n'
    for ingredient in sum_ingredients_in_recipes:
        shopping_list += (
            f'{ingredient["ingredient__name"]} - '
            f'{ingredient["amounts"]} '
            f'{ingredient["ingredient__measurement_unit"]}\n'
        )
    shopping_list += f'\n\nFoodgram ({today})'
    filename = 'shopping_list.txt'
    response = FileResponse(open(filename, 'rb'))
    return response
