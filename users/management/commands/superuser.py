from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):

        user = User.objects.create(
            email='admin@sky.pro',  # после создания нужно входить через этот адрес
            first_name='Admin',
            last_name='SkyPro',
            is_staff=True,
            is_superuser=True,
        )
        # зададим пароль
        user.set_password('123qwe')
        # сохраняем
        user.save()