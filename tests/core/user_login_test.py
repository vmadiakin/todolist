from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from rest_framework import status
from core.views import UserLoginView

User = get_user_model()


class UserLoginViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='johndoe',
            password='testpassword',
            is_active=True,  # Пользователь активен
        )

    def test_user_login_success(self):
        data = {
            'username': 'johndoe',
            'password': 'testpassword',
        }
        request = self.factory.post('/users/login', data)
        view = UserLoginView.as_view()

        # Включаем поддержку сеансов для тестового запроса
        request.session = self.client.session
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login_invalid_credentials(self):
        data = {
            'username': 'johndoe',
            'password': 'wrongpassword',
        }
        request = self.factory.post('/users/login', data)
        view = UserLoginView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_user_login_inactive_account(self):
        self.user.is_active = False
        self.user.save()
        data = {
            'username': 'johndoe',
            'password': 'testpassword',
        }
        request = self.factory.post('/users/login', data)
        view = UserLoginView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
