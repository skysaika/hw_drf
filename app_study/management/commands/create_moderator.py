from django.core.management.base import BaseCommand
from users.models import User
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Создает модератора'

    def handle(self, *args, **options):
        email = 'moderator@example.com'
        password = 'moderator123'

        user = User.objects.filter(email=email).first()

        if user is None:
            user = User.objects.create_user(email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Модератор {email} создан'))
        else:
            self.stdout.write(self.style.WARNING(f'Пользователь с email {email} уже существует'))

        moderators_group, created = Group.objects.get_or_create(name='moderators')
        user.groups.add(moderators_group)
        self.stdout.write(self.style.SUCCESS(f'Модератор {email} добавлен в группу модераторов'))
