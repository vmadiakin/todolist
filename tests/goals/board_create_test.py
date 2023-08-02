from django.test import TestCase
from goals.models import Board
from tests.factories import BoardFactory


class BoardTests(TestCase):
    def test_create_board(self):
        board = BoardFactory()
        self.assertIsInstance(board, Board)
        self.assertIsNotNone(board.title)
        self.assertFalse(board.is_deleted)
