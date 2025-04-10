from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from app_study.serializers import PaymentSerializer
from app_study.models import Payment
from users.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    payments = serializers.SerializerMethodField()  # Поле истории платежей

    class Meta:
        model = User
        fields = ('id', 'email', 'payments')  # Добавьте нужные поля

    def get_payments(self, obj):
        return PaymentSerializer(Payment.objects.filter(user=obj), many=True).data

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавление пользовательских полей в токен
        token['email'] = user.email
        return token

