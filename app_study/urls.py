from django.urls import path

from app_study.apps import AppStudyConfig
from rest_framework.routers import DefaultRouter

from app_study.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentCreateAPIView, PaymentListAPIView, \
    CourseSubscriptionCreateAPIView, CourseSubscriptionDeleteAPIView

app_name = AppStudyConfig.name
# роутер для курсов на основе вьюсета
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

# роутер для уроков на основе дженериков
urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),  # путь для создания урока
    path('lesson/list/', LessonListAPIView.as_view(), name='lesson-list'),  # путь для списка уроков
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-detail'),  # путь для просмотра урока
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),  # путь для обновления урока
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),  # путь для удаления урока

    # payment
    path('payment/create', PaymentCreateAPIView.as_view(), name='payment-create'), # путь для создания платежа
    path('payment/list/', PaymentListAPIView.as_view(), name='payment-list'), # путь для списка платежей

    # coursesubscription
    path('courses/<int:course_id>/subscribe/', CourseSubscriptionCreateAPIView.as_view(), name='course-subscribe'),
    path('courses/<int:course_id>/unsubscribe/', CourseSubscriptionDeleteAPIView.as_view(), name='course-unsubscribe'),
] + router.urls
