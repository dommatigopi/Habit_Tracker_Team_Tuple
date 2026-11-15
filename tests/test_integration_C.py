import unittest
import analytics

class TestAnalytics(unitest.TestCase):

    def test_current_streak_exists(self):
        self.assertTrue(callable(analytics.calculate_current_streak))

    def test_longest_streak_exists(self):
        self.assertTrue(callable(analytics.calculate_longest_streak))

if __name__ == "__main__":
    unittest.main()
