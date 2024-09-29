from rest_framework import viewsets

from app_study.models import Course
from app_study.serializers import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """Вьюсет курсов"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
