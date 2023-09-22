from django.contrib.auth.models import AbstractUser
from django.db import models
#from django.conf import settings
#from django.db.models.signals import post_save
#from django.dispatch import receiver
#from rest_framework.authtoken.models import Token

import constants


class User(AbstractUser):
    username = models.CharField(
        'Логин пользователя',
        max_length=constants.LENGTH_USER_USERNAME,
        help_text='Введите Ваш логин, не превышающий 50 символов.',
        unique=True,
        blank=False,
        null=False
    )
    password = models.CharField(
        'Пароль',
        max_length=constants.LENGTH_USER_PASSWORD,
        help_text='Введите Ваш пароль, не превышающий 100 символов.',
        blank=False,
        null=False
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=constants.LENGTH_USER_EMAIL,
        unique=True,
        blank=False,
        null=False
    )
    first_name = models.CharField(
        'Имя',
        max_length=constants.LENGTH_USER_FIRST_NAME,
        help_text='Введите Ваше имя.',
        blank=False,
        null=False
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=constants.LENGTH_USER_LAST_NAME,
        help_text='Введите Вашу фамилию.',
        blank=False,
        null=False
    )

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
    
    #@receiver(post_save, sender=settings.AUTH_USER_MODEL)
    #def create_auth_token(sender, instance=None, created=False, **kwargs):
    #    if created:
    #        Token.objects.create(user=instance)


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
