from django.contrib import admin

# админка для пользователя
from .models import User

admin.site.register(User)