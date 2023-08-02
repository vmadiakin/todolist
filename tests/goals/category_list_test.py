from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import force_authenticate
from goals.models import Board, GoalCategory, BoardParticipant
from goals.views import GoalCategoryCreateView


class CategoryCreationTest(TestCase):
    def setUp(self):
        # Получаем модель пользователя
        self.user_model = get_user_model()
        # Создаем тестового пользователя с помощью менеджера
        self.user = self.user_model.objects.create(username='testuser', password='testpassword')
        # Создаем тестовую доску
        self.board = Board.objects.create(title='Test Board')
        # Создаем объект BoardParticipant и связываем его с пользователем и доской
        BoardParticipant.objects.create(board=self.board, user=self.user, role=BoardParticipant.Role.owner)
        # Создаем экземпляр RequestFactory
        self.factory = RequestFactory()

    def test_category_creation(self):
        # Создаем POST-запрос для создания категории
        data = {'title': 'Test Category', 'board': self.board.id}
        request = self.factory.post('/category/create', data)
        force_authenticate(request, user=self.user)

        # Отправляем запрос в представление
        view = GoalCategoryCreateView.as_view()
        response = view(request)

        # Проверяем, что запрос успешен и категория создана
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что категория создана с правильным названием
        category = GoalCategory.objects.filter(title='Test Category').first()
        self.assertIsNotNone(category)

        # Проверяем, что категория привязана к правильной доске и пользователю
        self.assertEqual(category.board, self.board)
        self.assertEqual(category.user, self.user)
