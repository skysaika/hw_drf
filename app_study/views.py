from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, BasePermission

from app_study.models import Course, Lesson, Payment
from app_study.paginators import CoursePaginator, LessonPaginator, PaymentPaginator
from app_study.permissions import IsModerator, IsOwner, NotModerator, IsOwnerOrModerator
from app_study.serializers import CourseSerializer, LessonSerializer, PaymentSerializer


# на основе вьюсета ModelViewSet
class CourseViewSet(viewsets.ModelViewSet):
    """Представление для курса на основе вьюсета"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

    def get_queryset(self):
        print(f"Получение курсов: Пользователь - {self.request.user}, Суперпользователь - {self.request.user.is_superuser}, Модератор - {self.request.user.groups.filter(name='moderators').exists()}")
        if self.request.user.is_superuser or self.request.user.groups.filter(name='moderators').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

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
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = LessonPaginator

    def get_queryset(self):
        print(f"Список уроков: Пользователь - {self.request.user}, Супер - {self.request.user.is_superuser}, Модератор - {self.request.user.groups.filter(name='moderators').exists()}")
        if self.request.user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Представление для получения конкретного урока на основе дженериков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

    def has_object_permission(self, request, view, obj):
        print(f"Получение урока: Пользователь - {self.request.user}, Супер - {self.request.user.is_superuser}, Модератор - {self.request.user.groups.filter(name='moderators').exists()}")
        return obj.owner == request.user or request.user.groups.filter(name='moderators').exists()



class LessonUpdateAPIView(generics.UpdateAPIView):  # поддерживает как  PUT так и PATCH
    """Представление для обновления урока на основе дженериков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

    def patch(self, request, *args, **kwargs):
        print(
            f"Обновление урока: Пользователь - {self.request.user}, Супер - {self.request.user.is_superuser}, Модератор - {self.request.user.groups.filter(name='moderators').exists()}")
        return super().patch(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        print(
            f"Обновление урока: Пользователь - {self.request.user}, Супер - {self.request.user.is_superuser}, Модератор - {self.request.user.groups.filter(name='moderators').exists()}")
        return super().put(request, *args, **kwargs)


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
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ('payment_date',) # ?ordering=payment_date (по возрастанию)/?ordering=-payment_date (по убыванию).
    permission_classes = [IsAuthenticated]
    pagination_class = PaymentPaginator

    def get_queryset(self):
        print(
            f"Получение платежей: Пользователь - {self.request.user}, Супер - {self.request.user.is_superuser}, Модератор - {self.request.user.groups.filter(name='moderators').exists()}")
        return super().get_queryset()
