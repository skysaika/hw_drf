from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from app_study.permissions import IsOwner
from .models import User
from .serializers import UserProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsOwner()]

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
