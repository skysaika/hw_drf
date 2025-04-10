from rest_framework import serializers
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
