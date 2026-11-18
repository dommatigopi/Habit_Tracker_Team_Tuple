import unittest
from datetime import date
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import analytics
import habits


class TestHabitsIntegration(unittest.TestCase):

    def setUp(self):
        self.data = {"habits": []}

    def test_habit_creation_and_analytics_flow(self):
        habit = habits.create_habit(self.data, "Coding", "Practice Python")
        streak = analytics.calculate_current_streak(habit)
        rate = analytics.calculate_completion_rate(habit)
        self.assertEqual(streak, 0)
        self.assertEqual(rate, 0.0)

    def test_habit_completion_and_streak_update(self):
        habit = habits.create_habit(self.data, "Reading", "Read articles")
        today = date.today()
        self.assertTrue(habits.mark_completed(self.data, habit["id"], today))

        streak = analytics.calculate_current_streak(habit, today=today)
        self.assertEqual(streak, 1)


if __name__ == "__main__":
    unittest.main()
