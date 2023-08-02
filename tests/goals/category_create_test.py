from django.test import TestCase

from goals.models import GoalCategory
from tests.factories import GoalCategoryFactory


class GoalCategoryTests(TestCase):
    def test_create_goal_category(self):
        goal_category = GoalCategoryFactory()
        self.assertIsInstance(goal_category, GoalCategory)
        self.assertIsNotNone(goal_category.title)
        self.assertFalse(goal_category.is_deleted)
