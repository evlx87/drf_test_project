from django.contrib.auth.models import AbstractUser
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
