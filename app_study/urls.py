from app_study.apps import AppStudyConfig
from rest_framework.routers import DefaultRouter

from app_study.views import CourseViewSet

app_name = AppStudyConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
urlpatterns = [

] + router.urls
