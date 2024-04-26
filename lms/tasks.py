from celery import shared_task
from django.core.mail import send_mail

from config import settings


@shared_task
def course_update_notification(course, email):
    send_mail(
        subject='Уведомление от сервиса обучения',
        message=f'Курс {course} на который вы подписаны обновлен',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
        )
