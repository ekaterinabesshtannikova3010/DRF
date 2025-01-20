from users.models import User, Subscription

from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Lesson, Course


# class LessonCRUDTests(TestCase):
#
#     def setUp(self):
#         # Создание тестового курса
#         self.course = Course.objects.create(title='Тестовый курс', description='Описание курса')
#
#         # Создание тестовых пользователей
#         self.user_with_access = User.objects.create_user(phone='phone', email='email')
#         self.user_without_access = User.objects.create_user(phone='phone', email='email')
#
#         # Создание токена для аутентификации
#         self.token = Token.objects.create(user=self.user_with_access)
#
#         # Создание тестового урока
#         self.lesson_data = {
#             'title': 'Тестовый урок',
#             'description': 'Описание урока',
#             'preview': 'path/to/preview.jpg',
#             'video_link': 'http://example.com/video',
#             'course': self.course.id
#         }
#
#     def test_create_lesson(self):
#         self.client.force_authenticate(user=self.user_with_access)
#         response = self.client.post('/api/lessons/', self.lesson_data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#     def test_create_lesson_without_access(self):
#         self.client.force_authenticate(user=self.user_without_access)
#         response = self.client.post('/api/lessons/', self.lesson_data)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_read_lesson(self):
#         self.client.force_authenticate(user=self.user_with_access)
#         lesson = Lesson.objects.create(**self.lesson_data)
#         response = self.client.get(f'/api/lessons/{lesson.id}/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_update_lesson(self):
#         self.client.force_authenticate(user=self.user_with_access)
#         lesson = Lesson.objects.create(**self.lesson_data)
#         updated_data = {'title': 'Обновленный урок'}
#         response = self.client.patch(f'/api/lessons/{lesson.id}/', updated_data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         lesson.refresh_from_db()
#         self.assertEqual(lesson.title, 'Обновленный урок')
#
#     def test_delete_lesson(self):
#         self.client.force_authenticate(user=self.user_with_access)
#         lesson = Lesson.objects.create(**self.lesson_data)
#         response = self.client.delete(f'/api/lessons/{lesson.id}/')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Lesson.objects.filter(id=lesson.id).exists())
#
#
# class SubscriptionTests(TestCase):
#
#     def setUp(self):
#         self.course = Course.objects.create(title='Тестовый курс', description='Описание курса')
#         self.user = User.objects.create_user(phone='phone', email='email')
#         self.client.force_authenticate(user=self.user)
#
#     def test_subscribe_to_course(self):
#         response = self.client.post('/api/subscriptions/', {'course': self.course.id})
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())
#
#     def test_unsubscribe_from_course(self):
#         Subscription.objects.create(user=self.user, course=self.course)
#         response = self.client.delete(f'/api/subscriptions/{self.user.id}/{self.course.id}/')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
import unittest
from rest_framework.test import APIClient
from django.urls import reverse
# from .models import User, Course, Lesson, Subscription


class LessonTests(unittest.TestCase):

    def setUp(self):
        self.client = APIClient()

        # Создание тестового пользователя
        self.user = User.objects.create_user(phone='phone', email='zet@yandex.ru')
        self.user.is_staff = True
        self.user.save()

        # Создание тестового курса
        self.course = Course.objects.create(title='Test Course', description='Test Description')

        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        # URL для тестов
        self.lesson_url = reverse('lesson-list')  # Предполагается, что у Вас есть соответствующий URL

    def test_create_lesson(self):
        response = self.client.post(self.lesson_url, {
            'title': 'Test Lesson',
            'description': 'Test Description',
            'preview': '',  # Укажите путь к изображению, если необходимо
            'video_link': 'http://example.com/video',
            'course': self.course.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(Lesson.objects.get().title, 'Test Lesson')

    def test_read_lesson(self):
        lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test Description',
            preview='',
            video_link='http://example.com/video',
            course=self.course
        )
        response = self.client.get(reverse('lesson-detail', args=[lesson.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Test Lesson')

    def test_update_lesson(self):
        lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test Description',
            preview='',
            video_link='http://example.com/video',
            course=self.course
        )
        response = self.client.put(reverse('lesson-detail', args=[lesson.id]), {
            'title': 'Updated Lesson',
            'description': 'Updated Description',
            'preview': '',
            'video_link': 'http://example.com/updated_video',
            'course': self.course.id
        })
        self.assertEqual(response.status_code, 200)
        lesson.refresh_from_db()
        self.assertEqual(lesson.title, 'Updated Lesson')

    def test_delete_lesson(self):
        lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test Description',
            preview='',
            video_link='http://example.com/video',
            course=self.course
        )
        response = self.client.delete(reverse('lesson-detail', args=[lesson.id]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_subscription(self):
        response = self.client.post(reverse('subscription-list'), {
            'user': self.user.id,
            'course': self.course.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Subscription.objects.count(), 1)

    def test_unique_subscription(self):
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.post(reverse('subscription-list'), {
            'user': self.user.id,
            'course': self.course.id
        })
        self.assertEqual(response.status_code, 400)  # Ожидаем ошибку из-за уникальности


if __name__ == '__main__':
    unittest.main()

# Для проверки покрытия тестами используйте команду:
# python manage.py test --coverage
