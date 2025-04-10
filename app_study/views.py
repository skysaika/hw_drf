from rest_framework import viewsets, generics

from app_study.models import Course, Lesson, Payment
from app_study.serializers import CourseSerializer, LessonSerializer, PaymentSerializer


# на основе вьюсета ModelViewSet
class CourseViewSet(viewsets.ModelViewSet):
    """Представление для курса на основе вьюсета"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()  # возвращает все курсы


# на основе дженериков по CRUD для Generic
class LessonCreateAPIView(generics.CreateAPIView):
    """Представление для создания урока на основе дженериков"""
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    """Представление для получения списка уроков на основе дженериков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Представление для получения конкретного урока на основе дженериков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):  # поддерживает как  PUT так и PATCH
    """Представление для обновления урока на основе дженериков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):  # поддерживает только DELETE
    """Представление для удаления урока на основе дженериков"""
    queryset = Lesson.objects.all()  # здесь только queryset

# ViewSet для модели Payment на основе generic
class PaymentCreateAPIView(generics.CreateAPIView):
    """Представление для создания платежа на основе дженериков"""
    serializer_class = PaymentSerializer


class PaymentListAPIView(generics.ListAPIView):
    """Представление для получения списка платежей на основе дженериков"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
