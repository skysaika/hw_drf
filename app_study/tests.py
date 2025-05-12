from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User
from app_study.models import Course, Lesson, CourseSubscription

# class LessonCRUDTestCase(APITestCase):
#
#     def setUp(self):
#         """ Предусловия для тестов"""
#         self.user = User.objects.create_user(email='testuser@example.com', password='testpass')
#         self.client = APIClient()
#
#         # Получаем JWT токен
#         url = reverse('users:token_obtain_pair')  # путь к получению токена
#         response = self.client.post(url, {'email': 'testuser@example.com', 'password': 'testpass'}, format='json')
#         self.assertEqual(response.status_code, 200)
#         token = response.json()['access']
#
#         # Добавляем токен в заголовок авторизации
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
#         # Создаём курс и урок
#         self.course = Course.objects.create(title='Test Course', description='Desc', owner=self.user)
#
#         self.lesson = Lesson.objects.create(
#             title='Test Lesson',
#             description='Lesson desc',
#             course=self.course,
#             owner=self.user
#         )
#
#     def test_create_lesson(self):
#         """ Тестирование создания урока """
#         url = reverse('app_study:lesson-create')
#         data = {
#             'title': 'New Lesson',
#             'description': 'New lesson description',
#             'course': self.course.id
#         }
#         response = self.client.post(url, data=data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#         json_response = response.json()
#         self.assertEqual(json_response['title'], data['title'])
#         self.assertEqual(json_response['description'], data['description'])
#         self.assertEqual(json_response['course'], data['course'])
#         self.assertIn('id', json_response)
#         print(json_response)
#
#     def test_list_lessons(self):
#         """ Тестирование вывода списка уроков """
#         url = reverse('app_study:lesson-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         json_response = response.json()
#         self.assertTrue(len(json_response['results']) >= 1)  # с пагинацией
#
#     def test_retrieve_lesson(self):
#         """ Тестирование получения урока """
#         url = reverse('app_study:lesson-detail', args=[self.lesson.id])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         json_response = response.json()
#         self.assertEqual(json_response['title'], self.lesson.title)
#
#     def test_update_lesson(self):
#         """ Тестирование обновления урока """
#         url = reverse('app_study:lesson-update', args=[self.lesson.id])
#         data = {'title': 'Updated Lesson'}
#         response = self.client.patch(url, data=data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         json_response = response.json()
#         self.assertEqual(json_response['title'], data['title'])
#
#     def test_delete_lesson(self):
#         """ Тестирование удаления урока """
#         url = reverse('app_study:lesson-delete', args=[self.lesson.id])
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from app_study.models import Course, Lesson
import json


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        """ Предусловия: создай пользователя, токен, курс и урок """
        # Создаём пользователя
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')

        # Получаем JWT токен
        url = reverse('users:token_obtain_pair')  # или ваш путь к получению токена
        response = self.client.post(url, data=json.dumps({
            'email': 'testuser@example.com',
            'password': 'testpass'
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.json()['access']

        # Устанавливаем токен в заголовок Authorization
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Создаём курс и урок
        self.course = Course.objects.create(
            title='Test Course',
            description='Desc',
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Lesson desc',
            course=self.course,
            owner=self.user
        )

    # --- CRUD уроков ---
    def test_create_lesson(self):
        """ Тестирование создания урока """
        url = reverse('app_study:lesson-create')
        data = {
            'title': 'New Lesson',
            'description': 'New lesson description',
            'course': self.course.id
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        json_response = response.json()
        self.assertEqual(json_response['title'], data['title'])
        self.assertEqual(json_response['description'], data['description'])
        self.assertEqual(json_response['course'], data['course'])
        self.assertIn('id', json_response)

    def test_list_lessons(self):
        """ Тестирование вывода списка уроков """
        url = reverse('app_study:lesson-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = response.json()
        self.assertTrue(len(json_response['results']) >= 1)  # с пагинацией

    def test_retrieve_lesson(self):
        """ Тестирование получения урока """
        url = reverse('app_study:lesson-detail', args=[self.lesson.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = response.json()
        self.assertEqual(json_response['title'], self.lesson.title)
        print(json_response)

    def test_update_lesson(self):
        """ Тестирование обновления урока """
        url = reverse('app_study:lesson-update', args=[self.lesson.id])
        data = {'title': 'Updated Lesson'}
        response = self.client.patch(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = response.json()
        self.assertEqual(json_response['title'], data['title'])

    def test_delete_lesson(self):
        """ Тестирование удаления урока """
        url = reverse('app_study:lesson-delete', args=[self.lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    # --- Подписка на курс ---
    def test_subscribe_to_course(self):
        url = reverse('app_study:course-subscribe', args=[self.course.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что подписка создана в промежуточной модели
        self.assertTrue(CourseSubscription.objects.filter(user=self.user, course=self.course).exists())
        print(response.status_code, response.json())

    def test_unsubscribe_from_course(self):
        # Создаём подписку
        CourseSubscription.objects.create(user=self.user, course=self.course)

        url = reverse('app_study:course-unsubscribe', args=[self.course.id])
        # Используем DELETE, если вьюха ожидает именно этот метод
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(CourseSubscription.objects.filter(user=self.user, course=self.course).exists())
        print(response)

    # --- Тесты для курсов ---
    def test_create_course(self):
        url = reverse('app_study:courses-list')  # DefaultRouter создает имя 'courses-list' для списка/создания
        data = {
            'title': 'New Course',
            'description': 'New course description',
            'owner': self.user.id
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        json_response = response.json()
        self.assertEqual(json_response['title'], data['title'])
        self.assertEqual(json_response['description'], data['description'])

    def test_list_courses(self):
        url = reverse('app_study:courses-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = response.json()
        # В зависимости от пагинации может быть 'results' или просто список
        self.assertTrue('results' in json_response or isinstance(json_response, list))

    def test_retrieve_course(self):
        url = reverse('app_study:courses-detail', args=[self.course.id])  # DefaultRouter создает имя 'courses-detail'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = response.json()
        self.assertEqual(json_response['title'], self.course.title)

    def test_update_course(self):
        url = reverse('app_study:courses-detail', args=[self.course.id])
        data = {'title': 'Updated Course'}
        response = self.client.patch(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = response.json()
        self.assertEqual(json_response['title'], data['title'])

    def test_delete_course(self):
        url = reverse('app_study:courses-detail', args=[self.course.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Course.objects.filter(id=self.course.id).exists())