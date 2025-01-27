from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from users.models import Subscription, User
from .models import Course
from datetime import timedelta


@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(id=course_id)
    subscribers = Subscription.objects.filter(course=course)
    for subscriber in subscribers:
        send_mail(
            subject='Обновление курса',
            message=f'Курс "{course.title}" был обновлен. Проверьте новые материалы!',
            from_email='from@example.com',
            recipient_list=[subscriber.user.email],
        )


@shared_task
def check_user_activity():
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()
        print(f'Пользователь {user.username} заблокирован из-за отсутствия активности более месяца.')
