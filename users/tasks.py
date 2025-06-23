from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from users.models import User

@shared_task
def deactivate_inactive_users():
    month_ago = timezone.now() - timedelta(days=30)
    users = User.objects.filter(is_active=True, last_login__lt=month_ago)
    count = users.update(is_active=False)
    return f'Deactivated {count} users.'