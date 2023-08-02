from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import force_authenticate
from goals.models import Board
from goals.views import BoardCreateView


class BoardCreationTest(TestCase):
    def setUp(self):
        # Получаем модель пользователя
        self.user_model = get_user_model()
        # Создаем тестового пользователя с помощью менеджера
        self.user = self.user_model.objects.create(username='testuser', password='testpassword')
        # Создаем экземпляр RequestFactory
        self.factory = RequestFactory()

    def test_board_creation(self):
        # Создаем POST-запрос для создания доски
        data = {'title': 'Test Board'}
        request = self.factory.post('/board/create', data)
        force_authenticate(request, user=self.user)

        # Отправляем запрос в представление
        view = BoardCreateView.as_view()
        response = view(request)

        # Проверяем, что запрос успешен и доска создана
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что доска создана с правильным названием
        board = Board.objects.filter(title='Test Board').first()
        self.assertIsNotNone(board)
