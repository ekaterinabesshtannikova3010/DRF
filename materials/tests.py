from users.models import User
from rest_framework.test import APITestCase
from .models import Lesson, Course
from django.urls import reverse


class LessonTests(APITestCase):

    def setUp(self):
        # Создание тестового пользователя
        self.user = User.objects.create(phone='phone', email='zet@yandex.ru', is_staff=True)

        # Создание тестового курса
        self.course = Course.objects.create(title='Test Course', description='Test Description')

        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        # # URL для тестов
        self.lesson_url = reverse('materials:lesson-list-create')

    def test_read_lesson(self):
        lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test Description',
            preview='',
            video_link='http://example.com/video',
            course=self.course
        )
        response = self.client.get(reverse('materials:lesson-detail', args=[lesson.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Test Lesson')

    def test_delete_lesson(self):
        lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test Description',
            preview='',
            video_link='http://example.com/video',
            course=self.course
        )
        response = self.client.delete(reverse('materials:lesson-detail', args=[lesson.id]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Lesson.objects.count(), 0)
