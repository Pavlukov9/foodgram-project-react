from django.contrib.auth.models import AbstractUser
from django.db import models

import constants


class User(AbstractUser):
    password = models.CharField(
        'Пароль',
        max_length=constants.LENGTH_USER_PASSWORD,
        help_text='Введите Ваш пароль, не превышающий 100 символов.',
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=constants.LENGTH_USER_EMAIL,
        unique=True,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name'
    )

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


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
        ordering = ['user']
        verbose_name = 'Мои подписки'
        verbose_name_plural = 'Мои подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_user_author'
            )
        ]

    def __str__(self):
        return f'Пользователь {self.user} подписан на {self.author}'
