from django.urls import reverse
from rest_framework.test import APITestCase

from materials.models import Course
from users.models import User, Subscription


class LessonTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(phone='phone', email='zet@yandex.ru', is_staff=True)

        # Создание тестового курса
        self.course = Course.objects.create(title='Test Course', description='Test Description')

        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

    def test_create_subscription(self):
        """Тест на создание подписки"""
        subscription = Subscription.objects.create(user=self.user, course=self.course)
        self.assertIsNotNone(subscription.id)  # Проверяем, что подписка была создана
        self.assertEqual(Subscription.objects.count(), 1)  # Проверяем, что в базе данных одна подписка

    def test_subscription(self):
        response = self.client.post(reverse('users:subscribe-course', args=[self.course.id]), {
            'user': self.user.id,
            'course': self.course.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Subscription.objects.count(), 1)

    def test_unique_subscription(self):
        """Тест на уникальность подписки"""
        Subscription.objects.create(user=self.user, course=self.course)
        with self.assertRaises(Exception):  # Ожидаем исключение при попытке создать дубликат
            Subscription.objects.create(user=self.user, course=self.course)
