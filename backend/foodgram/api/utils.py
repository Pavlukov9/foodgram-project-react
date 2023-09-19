import base64
from django.core.files.base import ContentFile
from rest_framework import serializers, status
from rest_framework.response import Response


class Base64ImageField(serializers.ImageField):
    """Для работы с изображениями."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


def post_delete_method(self, request, recipe, serializer_name, model_name):
    user = self.request.user
    if request.method == 'POST':
        if model_name.objects.filter(user=user,
                                     recipe=recipe).exists():
            return Response({'errors': 'Рецепт уже добавлен!'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = serializer_name(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user, recipe=recipe)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    if not model_name.objects.filter(user=user,
                                     recipe=recipe).exists():
        return Response({'errors': 'Объект не найден'},
                        status=status.HTTP_400_BAD_REQUEST)
    model_name.objects.get(recipe=recipe).delete()
    return Response('Рецепт успешно удалён.',
                    status=status.HTTP_204_NO_CONTENT)
