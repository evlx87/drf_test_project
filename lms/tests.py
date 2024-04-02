import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django

django.setup()

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from lms.models import Course
from users.models import User


# Create your tests here.
class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(
            email='test@test.test',
            password='123test',
        )

        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='test',
            description='test',
            owner=self.user
        )

    def test_create_lesson(self):
        data = {
            'course': self.course.id,
            'title': 'test',
            'description': 'test',
            'image': '',
            'url_video': 'https://www.youtube.com/watch?v=Zst2ps35XiQ'
        }

        response = self.client.post('/lesson/create/', data=data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json(),
            {
                'id': 1,
                'title': 'test',
                'description': 'test',
                'image': None,
                'url_video': 'https://www.youtube.com/watch?v=Zst2ps35XiQ',
                'owner': 1,
                'course': 1
            }
        )

    def test_create_lesson_validation(self):
        data = {
            'course': self.course.id,
            'title': 'test',
            'description': 'test',
            'image': '',
            'url_video': 'https://www.vimeo.com/'
        }

        response = self.client.post('/lesson/create/', data=data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Недопустимая ссылка на видео']}
        )

    def test_list_lesson(self):
        response = self.client.get(reverse('lms:lesson_list'))
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)
        self.assertEqual(
            response.json(), {
                'count': 0, 'next': None, 'previous': None, 'results': []})

    def test_retrieve_lesson(self):
        data = {
            'course': self.course.id,
            'title': 'test',
            'description': 'test',
            'image': '',
            'url_video': 'https://www.youtube.com/watch?v=Zst2ps35XiQ'
        }
        response = self.client.post('/lesson/create/', data=data)
        print(response.json())

        response = self.client.get('/lesson/1/')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'id': 1,
                'title': 'test',
                'description': 'test',
                'image': None,
                'url_video': 'https://www.youtube.com/watch?v=Zst2ps35XiQ',
                'owner': 1,
                'course': 1
            }
        )

    def test_update_lesson(self):
        data = {
            'course': self.course.id,
            'title': 'test',
            'description': 'test',
            'image': '',
            'url_video': 'https://www.youtube.com/watch?v=Zst2ps35XiQ'
        }
        response = self.client.post('/lesson/create/', data=data)
        print(response.json())

        data = {
            'course': self.course.id,
            'title': 'UPDATED test',
            'description': 'UPDATED test',
            'image': '',
            'url_video': 'https://www.youtube.com/watch?v=Zst2ps35XiQ'
        }
        response = self.client.put('/lesson/update/1/', data=data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        data = {
            'course': self.course.id,
            'title': 'test',
            'description': 'test',
            'image': '',
            'url_video': 'https://www.youtube.com/watch?v=Zst2ps35XiQ'
        }
        response = self.client.post('/lesson/create/', data=data)
        print(response.json())

        response = self.client.delete('/lesson/delete/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(
            email='test@test.test',
            password='123test',
        )

        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='test',
            description='test',
            owner=self.user
        )

    def test_create_subscription(self):
        data = {
            'user': self.user.id,
            'course': self.course.id,
        }

        response = self.client.post('/subscription/create/', data=data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {'message': 'подписка добавлена'}
        )

    def test_list_subscription(self):
        response = self.client.get(reverse('lms:subscription_list'))
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 4)
        self.assertEqual(
            response.json(), {
                'count': 0, 'next': None, 'previous': None, 'results': []})

    def test_delete_subscription(self):
        data = {
            'user': self.user.id,
            'course': self.course.id,
        }

        response = self.client.post('/subscription/create/', data=data)

        self.assertEqual(
            response.json(),
            {'message': 'подписка добавлена'}
        )
        print(response.json())

        response = self.client.post('/subscription/create/', data=data)
        self.assertEqual(
            response.json(),
            {'message': 'подписка удалена'}
        )
        print(response.json())
