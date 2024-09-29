from rest_framework import serializers

from app_study.models import Course


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор курса"""
    class Meta:
        model = Course
        fields = '__all__'
