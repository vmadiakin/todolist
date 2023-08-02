from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from rest_framework import status

from core.views import UserRegistrationView

User = get_user_model()


class UserRegistrationViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_user_registration_success(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'testpassword',
            'password_repeat': 'testpassword',
            'role': 'user',
            'birthdate': '1990-01-01',
        }
        request = self.factory.post('/users/register', data)
        view = UserRegistrationView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'johndoe')

    def test_user_registration_password_mismatch(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'testpassword',
            'password_repeat': 'mismatchpassword',
            'role': 'user',
            'birthdate': '1990-01-01',
        }
        request = self.factory.post('/users/register', data)
        view = UserRegistrationView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Пароли не совпадают.', str(response.data['non_field_errors']))

    def test_user_registration_weak_password(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': '12345',  # Weak password
            'password_repeat': '12345',
            'role': 'user',
            'birthdate': '1990-01-01',
        }
        request = self.factory.post('/users/register', data)
        view = UserRegistrationView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password_too_short', str(response.data['non_field_errors']))
        self.assertIn('password_too_common', str(response.data['non_field_errors']))
        self.assertIn('password_entirely_numeric', str(response.data['non_field_errors']))
