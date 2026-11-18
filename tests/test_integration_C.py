import unittest
from datetime import date, timedelta

import analytics
import habits


class TestAnalyticsIntegration(unittest.TestCase):

    def setUp(self):
        self.data = {"habits": []}
        self.today = date.today()

    def test_multi_day_streak_integration(self):
        habit = habits.create_habit(
            self.data, "Pushups", created_on=self.today - timedelta(days=5)
        )
        habits.mark_completed(self.data, habit["id"], self.today - timedelta(days=1))
        habits.mark_completed(self.data, habit["id"], self.today)

        current = analytics.calculate_current_streak(habit, today=self.today)
        longest = analytics.calculate_longest_streak(habit)
        self.assertEqual(current, 2)
        self.assertEqual(longest, 2)

    def test_completion_rate_integration(self):
        start = self.today - timedelta(days=9)
        habit = habits.create_habit(self.data, "Hydration", created_on=start)
        for i in range(5):
            habits.mark_completed(self.data, habit["id"], start + timedelta(days=i))

        rate = analytics.calculate_completion_rate(
            habit, start_date=start, end_date=self.today
        )
        self.assertEqual(rate, 50.0)


if __name__ == "__main__":
    unittest.main()
