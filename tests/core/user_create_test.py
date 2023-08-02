from django.test import TestCase
from core.models import User
from tests.factories import UserFactory


class UserTests(TestCase):
    def test_create_user(self):
        user = UserFactory()
        self.assertIsInstance(user, User)
        self.assertIsNotNone(user.username)
        self.assertIsNotNone(user.email)
