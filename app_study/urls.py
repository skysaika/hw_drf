from django.urls import path

from app_study.apps import AppStudyConfig
from rest_framework.routers import DefaultRouter

from app_study.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView

app_name = AppStudyConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),  # путь для создания урока
    path('lesson/list/', LessonListAPIView.as_view(), name='lesson-list'),  # путь для получения списка уроков
] + router.urls
