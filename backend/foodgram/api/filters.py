from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter


from recipes.models import Recipe, User,Tag


class RecipeFilter(FilterSet):

    """Для сортировки по тегам, в избранном, в корзине покупок."""

    author = filters.ModelChoiceFilter(
        queryset=User.objects.all()
    )
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited',
                  'is_in_shopping_cart')
        
    def filter_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(favorites__author=self.request.user)
        return queryset
        
    def filter_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(shopping_carts__authorr=self.request.user)
        return queryset


class IngredientSearchFilter(SearchFilter):

    """Для сортировки ингредиентов."""

    search_param = 'name'
