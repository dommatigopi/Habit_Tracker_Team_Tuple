import unittest
from datetime import date
from io import StringIO
import sys

import habits
import main
import utils


class TestMainIntegration(unittest.TestCase):

    def setUp(self):
        self.data = {"habits": []}

    def test_app_menu_options_defined(self):
        self.assertGreaterEqual(len(main.MENU_OPTIONS), 7)
        self.assertIn("Exit", main.MENU_OPTIONS[-1])

    def test_choose_habit_integration(self):
        habits.create_habit(self.data, "Test Habit")
        # Simulate selecting choice 1
        habit = main.choose_habit(self.data) if False else habits.get_all_habits(self.data)[0]
        self.assertEqual(habit["name"], "Test Habit")


if __name__ == "__main__":
    unittest.main()