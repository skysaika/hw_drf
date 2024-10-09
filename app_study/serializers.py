from rest_framework import serializers

from app_study.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор курса"""
    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор урока"""
    class Meta:
        model = Lesson
        fields = '__all__'
