from datetime import date

from django.core.management.base import BaseCommand

from users.models import Payment, User, Course, Lesson


class Command(BaseCommand):
    help = (
        'Заполняет таблицу модели Payment для всех пользователей с разными методами '
        'оплаты в зависимости от ID '
        'пользователя')

    def handle(self, *args, **kwargs):
        users = User.objects.all()

        for user in users:
            if user.id % 2 == 0:
                payment_method = 'card'
                amount = 500
                course = Course.objects.get(id=1)
                lesson = None
            else:
                payment_method = 'cash'
                amount = 100
                course = None
                lesson = Lesson.objects.get(id=1)

            payment = Payment.objects.create(
                user=user,
                payment_date=date.today(),
                amount=amount,
                payment_method=payment_method,
                course=course,
                lesson=lesson
            )
