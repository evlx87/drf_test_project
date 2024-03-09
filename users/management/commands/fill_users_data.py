import json
import os
from datetime import date, datetime

from django.core.management.base import BaseCommand

from config import settings
from lms.models import Course, Lesson
from users.models import Payment, User


def load_from_json(file_name):
    """
    Загружает данные из JSON-файла.

    :param file_name: имя файла без расширения
    :return: данные из файла в формате словаря
    """
    with open(os.path.join(settings.JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    """Django команда для заполнения базы данных"""

    def handle(self, *args, **options):
        materials_data = load_from_json('materials_data')

        for item in materials_data:
            if item['model'] == 'materials.course':
                course_fields = item['fields']
                Course.objects.create(
                    id=item['pk'],
                    name=course_fields['title'],
                    preview=course_fields['image'],
                    description=course_fields['description']
                )
            elif item['model'] == 'materials.lesson':
                lesson_fields = item['fields']
                Lesson.objects.create(
                    id=item['pk'],
                    course_id=lesson_fields['course'],
                    name=lesson_fields['title'],
                    preview=lesson_fields['image'],
                    description=lesson_fields['description'],
                    video_url=lesson_fields['url_video']
                )

        users_data = load_from_json('users_data')

        User.objects.all().delete()
        for item in users_data:
            if item['model'] == 'users.user':
                user_fields = item['fields']
                User.objects.create(
                    id=item['pk'],
                    password=user_fields['password'],
                    last_login=user_fields['last_login'],
                    is_superuser=user_fields['is_superuser'],
                    first_name=user_fields['first_name'],
                    last_name=user_fields['last_name'],
                    is_staff=user_fields['is_staff'],
                    is_active=user_fields['is_active'],
                    date_joined=user_fields['date_joined'],
                    email=user_fields['email'],
                    phone=user_fields['phone'],
                    city=user_fields['city'],
                    avatar=user_fields['avatar']
                )

        payments_data = load_from_json('payments_data')

        for item in payments_data:
            payment_fields = item['fields']
            payment_id = item['pk']

            # Проверяем, существует ли платеж с таким же ID
            existing_payment = Payment.objects.filter(id=payment_id).first()

            if existing_payment:
                # Обрабатываем случай, когда платеж уже существует
                # Можно обновить существующий платеж или обработать его в соответствии с вашими требованиями
                pass
            else:
                # Создаем новый платеж, если его не существует
                Payment.objects.create(
                    id=payment_id,
                    user_id=payment_fields['user'],
                    payment_date=payment_fields['payment_date'],
                    course_id=payment_fields['course'],
                    lesson_id=payment_fields['lesson'],
                    amount=payment_fields['amount'],
                    payment_method=payment_fields['payment_method']
                )
