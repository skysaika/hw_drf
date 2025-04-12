from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from app_study.models import Course, Lesson

class Command(BaseCommand):
    help = 'Создание группы модераторов'

    def handle(self, *args, **kwargs):
        group_name = 'moderators'  # используйте то же имя, что в проверках

        # Удаляем группу, если есть
        try:
            Group.objects.get(name=group_name).delete()
            self.stdout.write(self.style.WARNING(f'Существующая группа "{group_name}" удалена'))
        except Group.DoesNotExist:
            self.stdout.write(f'Группа "{group_name}" не найдена, будет создана новая')

        # Создаём группу
        moderator_group, created = Group.objects.get_or_create(name=group_name)
        if created:
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" создана'))
        else:
            self.stdout.write(f'Группа "{group_name}" уже существует')

        # Получаем ContentType моделей
        ct_course = ContentType.objects.get_for_model(Course)
        ct_lesson = ContentType.objects.get_for_model(Lesson)

        # Список нужных прав
        needed_codenames = [
            'view_course',
            'change_course',
            'view_lesson',
            'change_lesson',
        ]

        permissions = []
        for codename in needed_codenames:
            try:
                perm = Permission.objects.get(codename=codename,
                                              content_type=ct_course if 'course' in codename else ct_lesson)
                permissions.append(perm)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Права с codename="{codename}" не найдены. Проверьте миграции.'))
                return

        # Назначаем права группе (заменяем все текущие)
        moderator_group.permissions.set(permissions)
        moderator_group.save()

        self.stdout.write(self.style.SUCCESS(f'Права для группы "{group_name}" назначены: {[p.codename for p in permissions]}'))
