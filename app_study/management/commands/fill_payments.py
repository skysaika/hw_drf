from django.core.management.base import BaseCommand
from app_study.models import Payment, Course, Lesson
from users.models import User


class Command(BaseCommand):
    help = 'Заполняет модель Payment тестовыми данными'

    def handle(self, *args, **kwargs):
        try:
            user = User.objects.get(id=1)
        except User.DoesNotExist:
            user = User.objects.create_user('example@example.com', '123qwe')

        # Создание платежей для курсов
        course_payments = [
            {'user': user, 'course': Course.objects.get(id=1), 'lesson': None, 'amount': 100.00,
             'payment_method': 'cash'},
            {'user': user, 'course': Course.objects.get(id=2), 'lesson': None, 'amount': 150.00,
             'payment_method': 'transfer'},
            {'user': user, 'course': Course.objects.get(id=3), 'lesson': None, 'amount': 200.00,
             'payment_method': 'cash'},
        ]

        # Создание платежей для уроков
        lesson_payments = [
            {'user': user, 'course': None, 'lesson': Lesson.objects.get(id=1), 'amount': 20.00,
             'payment_method': 'transfer'},
            {'user': user, 'course': None, 'lesson': Lesson.objects.get(id=3), 'amount': 30.00,
             'payment_method': 'cash'},
            {'user': user, 'course': None, 'lesson': Lesson.objects.get(id=5), 'amount': 40.00,
             'payment_method': 'transfer'},
        ]

        # Пакетное добавление платежей
        payments_for_create = []
        for payment_item in course_payments + lesson_payments:
            payments_for_create.append(Payment(**payment_item))

        Payment.objects.bulk_create(payments_for_create)

        self.stdout.write(self.style.SUCCESS('Данные успешно добавлены'))
