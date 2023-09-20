from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from api.pagination import CustomPagination
from django.shortcuts import get_object_or_404

from .models import User, Follow
from .serializers import FollowUserSerializer, FollowSerializer
from api.permissions import IsCurrentUserOrAdminOrReadOnly


class UserViewSet(viewsets.ModelViewSet):

    """Viewset для пользователя. """

    queryset = User.objects.all()
    permission_classes = (IsCurrentUserOrAdminOrReadOnly, )
    serializer_class = FollowUserSerializer
    pagination_class = CustomPagination

    @action(detail=True,
            methods=['post', 'delete'],
            serializer_class=FollowUserSerializer,
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
        return User.objects.filter(following__user=self.request.user)
