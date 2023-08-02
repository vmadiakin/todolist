from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import force_authenticate
from goals.models import Board, GoalCategory, Goal, BoardParticipant
from goals.views import GoalListView


class GoalListViewTest(TestCase):
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

    def test_goal_list_view(self):
        # Создаем несколько тестовых целей, привязанных к текущей категории и пользователю
        Goal.objects.create(title='Goal 1', description='Description 1', user=self.user, category=self.category)
        Goal.objects.create(title='Goal 2', description='Description 2', user=self.user, category=self.category)

        # Создаем GET-запрос для получения списка целей
        request = self.factory.get('/goal/list')
        force_authenticate(request, user=self.user)

        # Отправляем запрос в представление
        view = GoalListView.as_view()
        response = view(request)

        # Проверяем, что запрос успешен
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что на странице присутствуют тестовые цели
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Goal 1')
        self.assertEqual(response.data[1]['title'], 'Goal 2')

