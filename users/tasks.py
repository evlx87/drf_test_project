from celery import shared_task
from django.utils import timezone
from users.models import User


@shared_task
def check_users_and_block_inactive():
    current_date = timezone.now().date()
    inactive_period = timezone.timedelta(days=30)
    inactive_date = current_date - inactive_period

    inactive_users = User.objects.filter(last_login__lt=inactive_date)
    for user in inactive_users:
        if user.role != 'moderator' and not user.is_superuser:
            user.is_active = False
            user.save()
