import tempfile
import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import analytics
import reports


class TestReportsIntegration(unittest.TestCase):

    def setUp(self):
        self.today = date.today()
        self.sample_data = {
            "habits": [
                {
                    "id": "h_test",
                    "name": "Integration Habit",
                    "description": "Testing reports with analytics",
                    "created_on": self.today.isoformat(),
                    "completed_dates": [self.today.isoformat()],
                }
            ]
        }

    def test_summary_and_chart_generation(self):
        rep = reports.build_report(self.sample_data, today=self.today)
        self.assertIn("Integration Habit", rep)
        self.assertIn("1 days in total", rep)

        with tempfile.TemporaryDirectory() as tmpdir:
            chart_file = Path(tmpdir) / "chart.png"
            success = reports.save_chart_image(
                self.sample_data["habits"], str(chart_file)
            )
            self.assertTrue(success)
            self.assertTrue(chart_file.exists())

    def test_reports_weekly_matches_analytics_weekly(self):
        analytics_weekly = analytics.weekly_summary(
            self.sample_data, today=self.today
        )
        h_count = analytics_weekly.get("h_test", 0)

        # Check build_report output line matches
        rep = reports.build_report(self.sample_data, today=self.today)
        expected_fragment = f"{h_count} in the last 7 days"
        self.assertIn(expected_fragment, rep)


if __name__ == "__main__":
    unittest.main()