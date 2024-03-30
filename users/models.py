from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser, Group
from django.db import models

from lms.models import Course, Lesson
from django.utils.translation import gettext_lazy as _

# Create your models here.
NULLABLE = {'blank': True, 'null': True}
PAYMENT_CHOICES = (('card', 'карта'), ('cash', 'наличные'),)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class UserRoles(models.TextChoices):
    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')


class User(AbstractUser):
    """Класс, описывающий модель пользователь"""
    username = None
    email = models.EmailField(
        max_length=200,
        verbose_name='электронная почта',
        unique=True)
    phone = models.CharField(
        max_length=50,
        verbose_name='номер телефона',
        blank=True,
        null=True)
    avatar = models.ImageField(
        upload_to='users/',
        verbose_name='аватар',
        blank=True,
        null=True)
    city = models.CharField(
        max_length=100,
        verbose_name='город',
        blank=True,
        null=True)
    role = models.CharField(
        max_length=20,
        choices=UserRoles.choices,
        default=UserRoles.MEMBER,
        verbose_name='роль')
    objects = CustomUserManager()

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


class Payment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        **NULLABLE)
    payment_date = models.DateField(
        auto_now_add=True,
        verbose_name='дата оплаты')
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='курс',
        **NULLABLE)
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name='урок',
        **NULLABLE)
    amount = models.PositiveIntegerField(
        verbose_name='стоимость',
        **NULLABLE)
    payment_method = models.CharField(
        max_length=50,
        verbose_name='метод оплаты',
        choices=PAYMENT_CHOICES,
        default='card')

    def __str__(self):
        return f'{
            self.course if self.course else self.lesson} - {self.payment_date}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ('-payment_date',)
