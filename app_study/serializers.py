from rest_framework import serializers
from .models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор курса"""
    lesson_count = serializers.SerializerMethodField()  # поле для вывода количества уроков

    class Meta:
        model = Course
        fields = '__all__'

    def get_lesson_count(self, obj):
        return obj.lessons.count()  # возвращает количество уроков


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор урока"""
    class Meta:
        model = Lesson
        fields = '__all__'
