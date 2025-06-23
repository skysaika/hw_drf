from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from app_study.models import Course, CourseSubscription


@shared_task
def send_course_update_emails(course_id):
    print(f'[TASK START] Calling send_course_update_emails for course ID: {course_id}')  # <-- вот это добавляем

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        print(f'[TASK ERROR] Course with ID {course_id} does not exist.')
        return 'Course does not exist.'

    if timezone.now() - course.updated_at < timedelta(hours=4):
        print('[TASK INFO] Course was updated less than 4 hours ago. Skipping.')
        return 'Course was updated less than 4 hours ago.'

    subscriptions = CourseSubscription.objects.filter(course=course)
    for sub in subscriptions:
        send_mail(
            subject=f'Обновление курса: {course.title}',
            message='В курсе появились новые материалы. Проверьте обновления.',
            from_email='no-reply@example.com',
            recipient_list=[sub.user.email],
        )
        print(f'[TASK INFO] Email sent to: {sub.user.email}')

    print(f'[TASK COMPLETE] Sent emails to {subscriptions.count()} subscribers.')
    return f"Sent emails to {subscriptions.count()} subscribers."