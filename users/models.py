from django.contrib.auth.models import AbstractUser, Group
from django.db import models

# Create your models here.
NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """Класс, описывающий модель пользователь"""
    username = None
    email = models.EmailField(
        max_length=200,
        verbose_name='электронная почта',
        unique=True)
    phone = models.CharField(
        max_length=35,
        verbose_name='телефон',
        **NULLABLE)
    avatar = models.ImageField(
        upload_to='users/',
        verbose_name='аватар',
        **NULLABLE)
    city = models.CharField(
        max_length=150,
        verbose_name='город',
        **NULLABLE)

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        verbose_name='Custom user permissions',
        help_text='Specific permissions for this user.',
    )

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',
        blank=True,
        verbose_name='Custom user groups',
        help_text='The groups this user belongs to.',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
