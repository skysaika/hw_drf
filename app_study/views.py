from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from app_study.models import Course, Lesson, Payment
from app_study.serializers import CourseSerializer, LessonSerializer, PaymentSerializer


# на основе вьюсета ModelViewSet
class CourseViewSet(viewsets.ModelViewSet):
    """Представление для курса на основе вьюсета"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()  # возвращает все курсы
    permission_classes = [IsAuthenticated] # права только авторизованным


# на основе дженериков по CRUD для Generic
class LessonCreateAPIView(generics.CreateAPIView):
    """Представление для создания урока на основе дженериков"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonListAPIView(generics.ListAPIView):
    """Представление для получения списка уроков на основе дженериков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Представление для получения конкретного урока на основе дженериков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonUpdateAPIView(generics.UpdateAPIView):  # поддерживает как  PUT так и PATCH
    """Представление для обновления урока на основе дженериков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonDestroyAPIView(generics.DestroyAPIView):  # поддерживает только DELETE
    """Представление для удаления урока на основе дженериков"""
    queryset = Lesson.objects.all()  # здесь только queryset
    permission_classes = [IsAuthenticated]

# ViewSet для модели Payment на основе generic
class PaymentCreateAPIView(generics.CreateAPIView):
    """Представление для создания платежа на основе дженериков"""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]


class PaymentListAPIView(generics.ListAPIView):
    """Представление для получения списка платежей на основе дженериков"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ('payment_date',) # ?ordering=payment_date (по возрастанию)/?ordering=-payment_date (по убыванию).
    permission_classes = [IsAuthenticated]
