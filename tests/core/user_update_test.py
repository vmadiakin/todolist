from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import User


class UserUpdateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
        self.client.force_authenticate(user=self.user)

    def test_change_password_success(self):
        url = reverse('change-password')
        data = {
            'old_password': 'testpassword',
            'new_password': 'newpassword123'
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Пароль успешно изменен.')

        # Verify if the password has changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_change_password_invalid_old_password(self):
        url = reverse('change-password')
        data = {
            'old_password': 'wrongpassword',
            'new_password': 'newpassword123'
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Неправильный текущий пароль.', response.data['non_field_errors'])

        # Verify if the password remains unchanged
        self.assertTrue(self.user.check_password('testpassword'))

    def test_change_password_same_old_and_new_password(self):
        url = reverse('change-password')
        data = {
            'old_password': 'testpassword',
            'new_password': 'testpassword'
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['new_password'], 'Новый пароль должен отличаться от текущего.')

        # Verify if the password remains unchanged
        self.assertTrue(self.user.check_password('testpassword'))
