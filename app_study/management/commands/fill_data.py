from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from app_study.models import Course, Lesson, Payment
from users.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Наполнение базы данных данными'

    def handle(self, *args, **options):
        # Удаление токенов
        self.stdout.write(self.style.WARNING('Удаление токенов...'))
        Token.objects.all().delete()

        # Удаление существующих данных
        self.stdout.write(self.style.WARNING('Удаление существующих данных...'))
        Course.objects.all().delete()
        Lesson.objects.all().delete()
        Payment.objects.all().delete()
        User.objects.all().delete()
        Group.objects.filter(name='moderators').delete()

        # Создание пользователей
        users = [
            {'username': 'user1', 'email': 'user3@example.com', 'password': 'password123'},
            {'username': 'user2', 'email': 'user4@example.com', 'password': 'password123'},
        ]

        for user_data in users:
            User.objects.create_user(**user_data)

        # Создание курсов
        courses = [
            {'title': 'Курс 1', 'description': 'Описание курса 1', 'owner_id': 1},
            {'title': 'Курс 2', 'description': 'Описание курса 2', 'owner_id': 2},
        ]

        for course_data in courses:
            Course.objects.create(**course_data)

        # Создание уроков
        lessons = [
            {'title': 'Урок 1', 'description': 'Описание урока 1', 'course_id': 1, 'owner_id': 1},
            {'title': 'Урок 2', 'description': 'Описание урока 2', 'course_id': 1, 'owner_id': 1},
            {'title': 'Урок 3', 'description': 'Описание урока 3', 'course_id': 2, 'owner_id': 2},
        ]

        for lesson_data in lessons:
            Lesson.objects.create(**lesson_data)

        # Создание платежей
        payments = [
            {'user_id': 1, 'course_id': 1, 'amount': 100.00, 'payment_method': 'cash'},
            {'user_id': 2, 'course_id': 2, 'amount': 200.00, 'payment_method': 'transfer'},
        ]

        for payment_data in payments:
            Payment.objects.create(**payment_data)

        # Создание группы модераторов
        moderator_group, created = Group.objects.get_or_create(name='Модераторы')

        ct_course = ContentType.objects.get_for_model(Course)
        ct_lesson = ContentType.objects.get_for_model(Lesson)

        permission_view_course = Permission.objects.get_or_create(
            codename='view_course',
            name='Can view course',
            content_type=ct_course
        )[0]

        permission_change_course = Permission.objects.get_or_create(
            codename='change_course',
            name='Can change course',
            content_type=ct_course
        )[0]

        permission_view_lesson = Permission.objects.get_or_create(
            codename='view_lesson',
            name='Can view lesson',
            content_type=ct_lesson
        )[0]

        permission_change_lesson = Permission.objects.get_or_create(
            codename='change_lesson',
            name='Can change lesson',
            content_type=ct_lesson
        )[0]

        moderator_group.permissions.add(permission_view_course, permission_change_course, permission_view_lesson, permission_change_lesson)

        self.stdout.write(self.style.SUCCESS('База данных успешно очищена и наполнена данными'))
        self.stdout.write(self.style.SUCCESS('Группа модераторов создана и настроена'))
