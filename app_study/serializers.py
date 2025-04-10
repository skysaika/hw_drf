from rest_framework import serializers
from .models import Course, Lesson

# перенести сериализатор уроков выше в документе, чем сериализатор курсов
class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор урока"""
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор курса"""
    lesson_count = serializers.SerializerMethodField()  # поле для вывода количества уроков
    lessons = LessonSerializer(many=True, read_only=True)  # поле для вывода уроков

    class Meta:
        model = Course
        fields = '__all__'

    def get_lesson_count(self, obj):
        return obj.lessons.count()  # возвращает количество уроков
