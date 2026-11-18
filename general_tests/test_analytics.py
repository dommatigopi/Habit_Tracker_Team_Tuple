import unittest
from datetime import date, timedelta

import analytics
from analytics import (
    calculate_completion_rate,
    calculate_current_streak,
    calculate_longest_streak,
    weekly_summary,
)


class TestAnalyticsModule(unittest.TestCase):

    def setUp(self):
        self.today = date(2026, 11, 15)
        self.sample_habit = {
            "id": "h1",
            "name": "Reading",
            "created_on": "2026-11-01",
            "completed_dates": [
                "2026-11-10",
                "2026-11-11",
                "2026-11-12",
                "2026-11-14",
                "2026-11-15",
            ],
        }

    def test_current_streak_active_today(self):
        streak = calculate_current_streak(self.sample_habit, today=self.today)
        self.assertEqual(streak, 2)

    def test_current_streak_active_yesterday(self):
        habit = {"completed_dates": ["2026-11-13", "2026-11-14"]}
        streak = calculate_current_streak(habit, today=self.today)
        self.assertEqual(streak, 2)

    def test_current_streak_broken(self):
        habit = {"completed_dates": ["2026-11-10", "2026-11-11"]}
        streak = calculate_current_streak(habit, today=self.today)
        self.assertEqual(streak, 0)

    def test_current_streak_empty_or_none(self):
        self.assertEqual(calculate_current_streak(None), 0)
        self.assertEqual(calculate_current_streak({}), 0)
        self.assertEqual(calculate_current_streak([]), 0)

    def test_longest_streak(self):
        longest = calculate_longest_streak(self.sample_habit)
        self.assertEqual(longest, 3)

    def test_longest_streak_single_day(self):
        habit = {"completed_dates": ["2026-11-05"]}
        self.assertEqual(calculate_longest_streak(habit), 1)

    def test_longest_streak_ignores_duplicates(self):
        habit = {"completed_dates": ["2026-11-01", "2026-11-01", "2026-11-02"]}
        self.assertEqual(calculate_longest_streak(habit), 2)

    def test_completion_rate(self):
        rate = calculate_completion_rate(
            self.sample_habit,
            start_date="2026-11-01",
            end_date="2026-11-15",
        )
        self.assertAlmostEqual(rate, (5 / 15) * 100.0, places=1)

    def test_completion_rate_zero_days(self):
        rate = calculate_completion_rate(
            self.sample_habit,
            start_date="2026-11-15",
            end_date="2026-11-10",
        )
        self.assertEqual(rate, 0.0)

    def test_weekly_summary(self):
        data = {"habits": [self.sample_habit]}
        res = weekly_summary(data, today=self.today)
        self.assertEqual(res.get("h1"), 5)


if __name__ == "__main__":
    unittest.main()
