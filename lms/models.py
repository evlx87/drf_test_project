from django.conf import settings
from django.db import models

# Create your models here.
NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    """Модель курса обучения"""
    name = models.CharField(
        max_length=100,
        verbose_name='наименование')
    preview = models.ImageField(
        upload_to='course_previews/',
        verbose_name='картинка',
        **NULLABLE)
    description = models.TextField(
        verbose_name='описание')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
        ordering = ['name', ]


class Lesson(models.Model):
    """Модель урока курса обучения"""
    name = models.CharField(
        max_length=100,
        verbose_name='название урока')
    preview = models.ImageField(
        upload_to='lesson_previews/',
        verbose_name='картинка',
        **NULLABLE)
    description = models.TextField(
        verbose_name='описание')
    video_url = models.URLField(
        verbose_name='видеоурок',
        **NULLABLE)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='курс')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = ['course', 'name', ]
