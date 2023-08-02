from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import force_authenticate
from goals.models import Board, GoalCategory, Goal, BoardParticipant
from goals.views import GoalView


class GoalDetailViewTest(TestCase):
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

    def test_goal_detail_view(self):
        # Создаем тестовую цель, привязанную к текущей категории и пользователю
        goal = Goal.objects.create(title='Goal 1', description='Description 1', user=self.user, category=self.category)

        # Создаем GET-запрос для получения информации о цели
        request = self.factory.get(f'/goal/{goal.pk}')
        force_authenticate(request, user=self.user)

        # Отправляем запрос в представление
        view = GoalView.as_view()
        response = view(request, pk=goal.pk)

        # Проверяем, что запрос успешен
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что возвращенные данные соответствуют цели
        self.assertEqual(response.data['title'], 'Goal 1')
        self.assertEqual(response.data['description'], 'Description 1')
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['category'], self.category.id)
