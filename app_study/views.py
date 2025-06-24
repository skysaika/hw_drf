from decimal import Decimal
from locale import currency

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from app_study.models import Course, Lesson, Payment, CourseSubscription
from app_study.paginators import CoursePaginator, LessonPaginator, PaymentPaginator
from app_study.permissions import IsModerator, IsOwner, NotModerator, IsOwnerOrModerator
from app_study.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, CourseSubscriptionSerializer
from app_study.services import create_payment_intent, retrieve_payment_intent


# на основе вьюсета ModelViewSet
class CourseViewSet(viewsets.ModelViewSet):
    """Представление для курса на основе вьюсета"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all().order_by('id')  # <--- добавлено order_by
    pagination_class = CoursePaginator

    def get_queryset(self):
        print(f"Получение курсов: Пользователь - {self.request.user}, Суперпользователь - {self.request.user.is_superuser}, Модератор - {self.request.user.groups.filter(name='moderators').exists()}")
        if self.request.user.is_superuser or self.request.user.groups.filter(name='moderators').exists():
            return Course.objects.all().order_by('id')  # <--- добавлено order_by
        return Course.objects.filter(owner=self.request.user).order_by('id')  # <--- добавлено order_by

    def get_permissions(self):
        print(f"Права доступа для курса: {self.action}")
        if self.action == 'create':
            permission_classes = [IsAuthenticated, NotModerator]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsOwnerOrModerator]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner, NotModerator]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]




# на основе дженериков по CRUD для Generic
class LessonCreateAPIView(generics.CreateAPIView):
    """Представление для создания урока на основе дженериков"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, NotModerator]


    # сохраняем owner при создании урока
    def perform_create(self, serializer):
        print(
            f"Создание урока: Пользователь - {self.request.user}, Супер - {self.request.user.is_superuser}, Модератор - {self.request.user.groups.filter(name='moderators').exists()}")
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """Представление для получения списка уроков на основе дженериков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all().order_by('id')  # <--- добавлено order_by
    permission_classes = [IsAuthenticated]
    pagination_class = LessonPaginator

    def get_queryset(self):
        print(f"Список уроков: Пользователь - {self.request.user}, Супер - {self.request.user.is_superuser}, Модератор - {self.request.user.groups.filter(name='moderators').exists()}")
        if self.request.user.groups.filter(name='moderators').exists():
            return Lesson.objects.all().order_by('id')  # <--- добавлено order_by
        return Lesson.objects.filter(owner=self.request.user).order_by('id')  # <--- добавлено order_by


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Представление для получения конкретного урока на основе дженериков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

    def has_object_permission(self, request, view, obj):
        print(f"Получение урока: Пользователь - {self.request.user}, Супер - {self.request.user.is_superuser}, Модератор - {self.request.user.groups.filter(name='moderators').exists()}")
        return obj.owner == request.user or request.user.groups.filter(name='moderators').exists()



from app_study.tasks import send_course_update_emails  # импорт задачи

class LessonUpdateAPIView(generics.UpdateAPIView):  # поддерживает как PUT, так и PATCH
    """Представление для обновления урока на основе дженериков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

    def patch(self, request, *args, **kwargs):
        print(
            f"Обновление урока: Пользователь - {request.user}, Супер - {request.user.is_superuser}, Модератор - {request.user.groups.filter(name='moderators').exists()}"
        )
        response = super().patch(request, *args, **kwargs)

        lesson = self.get_object()
        if lesson.course:
            print(f'Calling send_course_update_emails for course ID: {lesson.course.id}')
            send_course_update_emails.delay(lesson.course.id)

        return response

    def put(self, request, *args, **kwargs):
        print(
            f"Обновление урока: Пользователь - {request.user}, Супер - {request.user.is_superuser}, Модератор - {request.user.groups.filter(name='moderators').exists()}"
        )
        response = super().put(request, *args, **kwargs)

        lesson = self.get_object()
        if lesson.course:
            print(f'Calling send_course_update_emails for course ID: {lesson.course.id}')
            send_course_update_emails.delay(lesson.course.id)



class LessonDestroyAPIView(generics.DestroyAPIView):  # поддерживает только DELETE
    """Представление для удаления урока на основе дженериков"""
    queryset = Lesson.objects.all()  # здесь только queryset
    permission_classes = [IsAuthenticated, IsOwner, NotModerator]

    def delete(self, request, *args, **kwargs):
        print(
            f"Удаление урока: Пользователь - {self.request.user}, Супер - {self.request.user.is_superuser}, Модератор - {self.request.user.groups.filter(name='moderators').exists()}")
        return super().delete(request, *args, **kwargs)


# ViewSet для модели Payment на основе generic
class PaymentCreateAPIView(generics.CreateAPIView):
    """Представление для создания платежа на основе дженериков"""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print(
            f"Создание платежа: Пользователь - {self.request.user}, Супер - {self.request.user.is_superuser}, Модератор - {self.request.user.groups.filter(name='moderators').exists()}")
        return super().post(request, *args, **kwargs)


class PaymentListAPIView(generics.ListAPIView):
    """Представление для получения списка платежей на основе дженериков"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all().order_by('id')  # <--- добавлено order_by
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ('payment_date',) # ?ordering=payment_date (по возрастанию)/?ordering=-payment_date (по убыванию).
    permission_classes = [IsAuthenticated]
    pagination_class = PaymentPaginator

    def get_queryset(self):
        print(
            f"Получение платежей: Пользователь - {self.request.user}, Супер - {self.request.user.is_superuser}, Модератор - {self.request.user.groups.filter(name='moderators').exists()}")
        return super().get_queryset()


class CourseSubscriptionCreateAPIView(APIView):
    """Представление для оформления подписки пользователя на курс."""
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        user = request.user
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'detail': 'Курс не найден'}, status=status.HTTP_404_NOT_FOUND)

        subscription, created = CourseSubscription.objects.get_or_create(user=user, course=course)
        if created:
            serializer = CourseSubscriptionSerializer(subscription)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Вы уже подписаны на этот курс'}, status=status.HTTP_200_OK)

class CourseSubscriptionDeleteAPIView(APIView):
    """Представление для отмены подписки пользователя на курс."""
    permission_classes = [IsAuthenticated]

    def delete(self, request, course_id):
        user = request.user
        try:
            subscription = CourseSubscription.objects.get(user=user, course_id=course_id)
            subscription.delete()
            return Response({'detail': 'Подписка удалена'}, status=status.HTTP_204_NO_CONTENT)
        except CourseSubscription.DoesNotExist:
            return Response({'detail': 'Подписка не найдена'}, status=status.HTTP_404_NOT_FOUND)


class StripePaymentIntentCreateAPIView(APIView):
    """Представление для создания платежа для курса через Stripe."""
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'detail': 'Курс не найден'}, status=status.HTTP_404_NOT_FOUND)
        # Создаем платежв Stripe
        intent = create_payment_intent(course, request.user)

        # Сохраняем платеж в базу
        Payment.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
            payment_method='transfer',
        )

        return Response({'client_secret': intent.client_secret}, status=status.HTTP_200_OK)


class StripePaymentStatusRetrieveAPIView(APIView):
    """Представление для получения статуса платежа через Stripe."""
    permission_classes = [IsAuthenticated]

    def get(self, request, payment_intent_id):
        try:
            intent = retrieve_payment_intent(payment_intent_id)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'status': intent.status,
            'amount': intent.amount,
            'currency': intent.currency,
        }, status=status.HTTP_200_OK)