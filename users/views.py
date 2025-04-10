from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserProfileSerializer

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]  # Ограничение доступа для аутентифицированных пользователей

    def get_object(self):
        return self.request.user  # Возвращает текущего аутентифицированного пользователя

# Кастомное представление для получения токена
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request=request, email=email, password=password)
        if user is None:
            return Response({'non_field_errors': ['Unable to log in with provided credentials.']}, status=401)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
