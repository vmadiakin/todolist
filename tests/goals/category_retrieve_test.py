from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import force_authenticate
from goals.models import Board, GoalCategory, BoardParticipant
from goals.views import GoalCategoryView


class GoalCategoryViewTest(TestCase):
    def setUp(self):
        # Получаем модель пользователя
        self.user_model = get_user_model()
        # Создаем тестового пользователя с помощью менеджера
        self.user = self.user_model.objects.create(username='testuser', password='testpassword')
        # Создаем тестовую доску
        self.board = Board.objects.create(title='Test Board')
        # Создаем объект BoardParticipant и связываем его с пользователем и доской
        BoardParticipant.objects.create(board=self.board, user=self.user, role=BoardParticipant.Role.owner)
        # Создаем тестовую категорию и связываем ее с доской и пользователем
        self.category = GoalCategory.objects.create(title='Test Category', board=self.board, user=self.user)
        # Создаем экземпляр RequestFactory
        self.factory = RequestFactory()

    def test_goal_category_view(self):
        # Создаем GET-запрос для получения информации о категории
        request = self.factory.get(f'/goal_category/{self.category.pk}')
        force_authenticate(request, user=self.user)

        # Отправляем запрос в представление
        view = GoalCategoryView.as_view()
        response = view(request, pk=self.category.pk)

        # Проверяем, что запрос успешен
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что возвращенные данные соответствуют категории
        self.assertEqual(response.data['title'], 'Test Category')
        self.assertEqual(response.data['board'], self.board.id)
        self.assertEqual(response.data['user']['id'], self.user.id)
