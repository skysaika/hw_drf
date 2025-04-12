from django.core.management import BaseCommand
from dotenv import load_dotenv
import os

from users.models import User


class Command(BaseCommand):
    help = "Создать нового суперпользователя"

    def handle(self, *args, **options):
        email = 'admin@sky.pro'
        password = os.getenv("SUPERUSER_PASSWORD")

        # Удаление существующего суперпользователя (если он существует)
        try:
            user = User.objects.get(email=email)
            user.delete()
            self.stdout.write(self.style.SUCCESS(f"Суперпользователь с email {email} успешно удален"))
        except User.DoesNotExist:
            self.stdout.write(self.style.WARNING(f"Суперпользователь с email {email} не найден"))

        # Создание нового суперпользователя
        user = User.objects.create(
            email=email,
            first_name='Admin',
            last_name='SkyPro',
            is_staff=True,
            is_superuser=True,
        )
        user.set_password(password)
        user.save()

        self.stdout.write(self.style.SUCCESS(f"Новый суперпользователь с email {email} успешно создан"))