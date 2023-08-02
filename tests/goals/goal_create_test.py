from django.test import TestCase
from goals.models import Goal
from tests.factories import GoalFactory


class GoalTests(TestCase):
    def test_create_goal(self):
        goal = GoalFactory()
        self.assertIsInstance(goal, Goal)
        self.assertIsNotNone(goal.title)
        self.assertIsNotNone(goal.due_date)


class GoalTestsWithParametres(TestCase):
    def test_create_goal(self):
        goal = GoalFactory(title="My Test Goal", due_date="2023-08-10")
        self.assertIsInstance(goal, Goal)
        self.assertEqual(goal.title, "My Test Goal")
        self.assertEqual(goal.due_date, "2023-08-10")
