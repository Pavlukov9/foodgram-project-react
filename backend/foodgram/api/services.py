import datetime

from django.db.models import Sum
from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response

from recipes.models import RecipeIngredient


def download_shopping_cart_(self, request):
    user = request.user
    if not user.carts.exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)

    ingredients = RecipeIngredient.objects.filter(
        recipe__carts__user=request.user
    ).values(
        'ingredient__name',
        'ingredient__measurement_unit'
    ).annotate(cart_amount=Sum('amount'))

    today = datetime.datetime.now().strftime('%d-%m-%Y')
    shopping_list = f'Список покупок на: {today}\n\n'
    for ingredient in ingredients:
        shopping_list += (
            f'{ingredient["ingredient__name"]} - '
            f'{ingredient["cart_amount"]} '
            f'{ingredient["ingredient__measurement_unit"]}\n'
        )
    shopping_list += f'\n\nFoodgram ({today})'
    response = FileResponse(shopping_list, content_type='text/plain')
    return response
