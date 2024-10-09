from django.urls import path

from app_study.apps import AppStudyConfig
from rest_framework.routers import DefaultRouter

from app_study.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView

app_name = AppStudyConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),  # путь для создания урока
    path('lesson/list/', LessonListAPIView.as_view(), name='lesson-list'),  # путь для списка уроков
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-detail'),  # путь для просмотра урока
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),  # путь для обновления урока
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),  # путь для удаления урока
] + router.urls
