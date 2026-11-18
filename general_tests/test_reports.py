import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

import reports
from reports import (
    ChartStrategy,
    ImageChartStrategy,
    TextChartStrategy,
    build_report,
    parse_date,
    save_chart_image,
    save_report,
    text_chart,
)



class TestReportsModule(unittest.TestCase):

    def setUp(self):
        self.today = date(2026, 11, 15)
        self.sample_data = {
            "habits": [
                {
                    "id": "h1",
                    "name": "Exercise",
                    "description": "30 mins workout",
                    "created_on": "2026-11-01",
                    "completed_dates": [
                        "2026-11-09",
                        "2026-11-14",
                        "2026-11-15",
                        "2026-11-15",  # Duplicate
                        "2026-11-20",  # Future date (after 2026-11-15)
                        "invalid-date",
                    ],
                },
                {
                    "id": "h2",
                    "name": "Exercise",  # Same name
                    "description": "Another habit with same name",
                    "created_on": "2026-11-05",
                    "completed_dates": ["2026-11-15"],
                },
            ]
        }

    def test_chart_strategy_base_class(self):
        self.assertTrue(issubclass(TextChartStrategy, ChartStrategy))
        self.assertTrue(issubclass(ImageChartStrategy, ChartStrategy))

    def test_text_chart_returns_string(self):
        res = text_chart({"Reading": 5, "Yoga": 3})
        self.assertIsInstance(res, str)
        self.assertIn("Reading", res)
        self.assertIn("Yoga", res)

    def test_text_chart_empty_input(self):
        res = text_chart({})
        self.assertIn("No data to display", res)

    def test_text_chart_bar_scaling(self):
        res = text_chart({"Habit A": 10, "Habit B": 1})
        self.assertIn("#", res)
        lines = res.strip().split("\n")
        self.assertEqual(len(lines), 2)
        # Value above 0 gets at least one '#'
        self.assertIn("#", lines[1])

    def test_text_chart_all_zeros(self):
        res = text_chart({"Habit A": 0, "Habit B": 0})
        self.assertIsInstance(res, str)

    def test_save_chart_image_creates_png(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "test_chart.png"
            res = save_chart_image({"Habit": 4}, str(out_file))
            self.assertTrue(res)
            self.assertTrue(out_file.exists())
            self.assertGreater(out_file.stat().st_size, 0)

    def test_save_chart_image_missing_folder(self):
        non_existent = "C:/non_existent_folder_xyz_123/chart.png"
        res = save_chart_image({"Habit": 4}, non_existent)
        self.assertFalse(res)

    def test_build_report_structure(self):
        rep = build_report(self.sample_data, today=self.today)
        self.assertIsInstance(rep, str)
        self.assertIn("Exercise", rep)
        self.assertIn("h1", rep)
        self.assertIn("h2", rep)

    def test_build_report_filters_invalid_and_future_dates(self):
        """build_report ignores duplicates, invalid strings and future dates.

        For h1 (Exercise):
        Valid dates <= 2026-11-15 are 2026-11-09, 2026-11-14, 2026-11-15 (total 3).
        In the last 7 days (2026-11-09 to 2026-11-15): 3 days.
        """
        rep = build_report(self.sample_data, today=self.today)
        self.assertIn("3 days in total", rep)

    def test_build_report_empty_data(self):
        rep = build_report({"habits": []})
        self.assertIn("No habits tracked", rep)

    def test_save_report_utf8(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "report.txt"
            sample_text = "Report with umlauts: äöü, and symbols: ✓ ✗"
            res = save_report(sample_text, str(file_path))
            self.assertTrue(res)
            content = file_path.read_text(encoding="utf-8")
            self.assertEqual(content, sample_text)


if __name__ == "__main__":
    unittest.main()