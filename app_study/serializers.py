from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Course, Lesson, Payment, CourseSubscription
from .services import create_payment_intent
from .validators import YouTubeOnlyURLValidator


# перенести сериализатор уроков выше в документе, чем сериализатор курсов
class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор урока"""
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [YouTubeOnlyURLValidator(field='video_link')]


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор курса"""
    lesson_count = serializers.SerializerMethodField()  # поле для вывода количества уроков
    lessons = LessonSerializer(many=True, read_only=True)  # поле для вывода
    is_subscribed = serializers.SerializerMethodField()  # поле подписки на курс

    class Meta:
        model = Course
        fields = '__all__'  # можно явно перечислить поля, добавив is_subscribed
        # fields = ['id', 'title', 'preview', 'description', 'owner', 'lesson_count', 'lessons', 'is_subscribed']

    def get_lesson_count(self, obj):
        return obj.lessons.count()  # возвращает количество уроков

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user  # получаем текущего пользователя
        if user.is_anonymous:
            return False  # если пользователь не аутентифицирован, считаем, что подписки нет
        # проверяем, есть ли запись подписки для данного пользователя и данного курса
        return CourseSubscription.objects.filter(user=user, course=obj).exists()


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор платежа"""

    class Meta:
        model = Payment
        fields = '__all__'


class CourseSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubscription
        fields = '__all__'
        read_only_fields = ('user', 'subscribed_at')


class StripePaymentsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("course",)

    def create(self, validated_data):
        user = self.context['request'].user
        course = validated_data['course']
        intent = create_payment_intent(course, user)
        return {
            'client_secret': intent.client_secret,
            'payment_intent_id': intent.id,
        }



