from django.core.management.base import BaseCommand
from users.models import Payment
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson

class Command(BaseCommand):
    help = 'Load payment data'

    def handle(self, *args, **kwargs):
        user = get_user_model().objects.get(id=1)  # Получаем пользователя с ID 1
        course = Course.objects.get(id=1)  # Получаем курс с ID 1
        lesson = Lesson.objects.get(id=1)  # Получаем урок с ID 1

        # Создаем платеж
        Payment.objects.create(
            user=user,
            paid_course=course,
            paid_lesson=lesson,
            amount=100.00,
            payment_method='cash'
        )
        self.stdout.write(self.style.SUCCESS('Платеж успешно загружен'))