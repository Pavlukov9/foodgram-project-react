from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        SAFE_METHODS, IsAuthenticatedOrReadOnly)
from rest_framework.response import Response


from .filters import IngredientSearchFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAdminAuthorOrReadOnly
from recipes.models import (Favorite, Ingredient, Recipe,
                            ShoppingCart, Tag)
from .services import download_shopping_cart
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeWriteSerializer, RecipeListSerializer,
                          ShoppingCartSerializer, TagSerializer,
                          FollowUserSerializer, FollowSerializer, UserSerializer)
from users.models import User, Follow
from .utils import post_delete_method


class CustomUserViewSet(UserViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class UserViewSet(viewsets.ModelViewSet):

    """Viewset для пользователя. """

    queryset = User.objects.all()
    permission_classes = (IsAdminAuthorOrReadOnly, )
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    @action(detail=True,
            methods=['post', 'delete'],
            serializer_class=FollowSerializer,
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, *args, **kwargs):
        author = get_object_or_404(User, id=self.kwargs.get('pk'))
        if request.method == 'POST':
            Follow.objects.create(user=request.user, author=author)
            return Response(
                self.serializer_class(author,
                                      context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )

        if Follow.objects.filter(user=request.user, author=author).exists():
            Follow.objects.get(user=request.user_id, author=author.id).delete()
            return Response('Отписка прошла успешно',
                            status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Вы не подписаны на этого пользователя'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,
            methods=['post'],
            serializer_class=FollowSerializer,
            permission_classes=[IsAuthenticated])
    def subscriptions(self):
        return User.objects.filter(following__user=self.request.user.follower)


class TagViewSet(viewsets.ReadOnlyModelViewSet):

    """Вьюсет для работы с тегами."""

    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):

    """Вьюсет для работы с ингредиентами."""

    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter, )
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):

    """Вьюсет для работы с рецептами."""

    queryset = Recipe.objects.all().select_related('author').prefetch_related('tags')
    permission_classes = (IsAdminAuthorOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    pagination_class = CustomPagination
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeListSerializer
        return RecipeWriteSerializer

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated, ])
    def favorite(self, request, pk):

        """Добавление в избранное и удаление из него."""

        recipe = get_object_or_404(Recipe, id=pk)
        return post_delete_method(self, request, recipe,
                                  FavoriteSerializer, Favorite)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated, ])
    def shopping_cart(self, request, pk):

        """Добавление в список покупок и удаление из него."""

        recipe = get_object_or_404(Recipe, id=pk)
        return post_delete_method(self, request, recipe,
                                  ShoppingCartSerializer, ShoppingCart)

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated, ])
    def download_chopping_cart(self, request, author):

        """Отправка файла со списком покупок."""

        return download_shopping_cart(self, request, author)
