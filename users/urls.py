from django.urls import path

from .apps import UsersConfig
from .views import UserProfileView, CustomObtainAuthToken

app_name = UsersConfig.name  # Убедитесь, что app_name указан

urlpatterns = [
    path('token/', CustomObtainAuthToken.as_view(), name='custom_token'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]
