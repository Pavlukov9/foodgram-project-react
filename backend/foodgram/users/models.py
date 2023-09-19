from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField(
        'Логин пользователя',
        max_length=50,
        help_text='Введите Ваш логин, не превышающий 50 символов.',
        unique=True,
        blank=False,
        null=False
    )
    password = models.CharField(
        'Пароль',
        max_length=100,
        help_text='Введите Ваш пароль, не превышающий 100 символов.',
        blank=False,
        null=False
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    first_name = models.CharField(
        'Имя',
        max_length=50,
        help_text='Введите Ваше имя.',
        blank=False,
        null=False
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=100,
        help_text='Введите Вашу фамилию.',
        blank=False,
        null=False
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username