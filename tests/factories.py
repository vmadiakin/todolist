from factory.django import DjangoModelFactory
from factory import Faker, SubFactory
from core.models import User
from goals.models import Board, GoalCategory, Goal


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    username = Faker('user_name')
    email = Faker('email')
    password = Faker('password', length=10)
    role = User.USER
    birthdate = Faker('date_of_birth')


class BoardFactory(DjangoModelFactory):
    class Meta:
        model = Board

    title = Faker('sentence', nb_words=4)  # Генерируем случайное название из 4 слов
    is_deleted = False


class GoalCategoryFactory(DjangoModelFactory):
    class Meta:
        model = GoalCategory

    board = SubFactory(BoardFactory)  # Используем фабрику для создания связанного объекта Board
    title = Faker('sentence', nb_words=3)  # Генерируем случайное название из 3 слов
    user = SubFactory(UserFactory)  # Используем фабрику для создания связанного объекта User
    is_deleted = False


class GoalFactory(DjangoModelFactory):
    class Meta:
        model = Goal

    user = SubFactory(UserFactory)  # Используем фабрику для создания связанного объекта User
    category = SubFactory(GoalCategoryFactory)  # Используем фабрику для создания связанного объекта GoalCategory
    title = Faker('sentence', nb_words=5)  # Генерируем случайный заголовок из 5 слов
    description = Faker('text', max_nb_chars=200)  # Генерируем случайное описание до 200 символов
    due_date = Faker('date_between', start_date='+1d', end_date='+1y')  # Генерируем случайную дату выполнения в пределах года
    status = Goal.Status.to_do
    priority = Goal.Priority.medium
