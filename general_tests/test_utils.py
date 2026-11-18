import unittest
from datetime import date
from io import StringIO
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import utils
from utils import (
    clear_screen,
    confirm,
    display_header,
    display_menu,
    get_date_input,
    get_menu_choice,
    get_non_empty_input,
    get_optional_input,
    parse_date,
    validate_date,
)


class TestUtilsModule(unittest.TestCase):

    def test_display_header(self):
        """display_header prints centered title enclosed in '='."""
        captured = StringIO()
        sys.stdout = captured
        try:
            display_header("TITLE")
        finally:
            sys.stdout = sys.__stdout__
        out = captured.getvalue()
        self.assertIn("TITLE", out)
        self.assertIn("=", out)

    def test_display_menu(self):
        """display_menu prints formatted options."""
        captured = StringIO()
        sys.stdout = captured
        try:
            display_menu(["Option 1", "Option 2"])
        finally:
            sys.stdout = sys.__stdout__
        out = captured.getvalue()
        self.assertIn("[1] Option 1", out)
        self.assertIn("[2] Option 2", out)

    def test_validate_date(self):
        """validate_date correctly validates YYYY-MM-DD."""
        self.assertTrue(validate_date("2026-11-18"))
        self.assertFalse(validate_date("18-11-2026"))
        self.assertFalse(validate_date("invalid"))

    def test_parse_date(self):
        """parse_date parses valid date strings and date objects."""
        self.assertEqual(parse_date("2026-11-18"), date(2026, 11, 18))
        self.assertEqual(parse_date(date(2026, 11, 18)), date(2026, 11, 18))
        self.assertIsNone(parse_date("not-a-date"))

    def test_get_non_empty_input(self):
        """get_non_empty_input skips empty inputs until valid."""
        inputs = iter(["", "  ", "Valid"])
        res = get_non_empty_input(input_func=lambda _: next(inputs))
        self.assertEqual(res, "Valid")

    def test_get_optional_input(self):
        """get_optional_input returns default when empty."""
        res_empty = get_optional_input(default="def", input_func=lambda _: "")
        self.assertEqual(res_empty, "def")
        res_filled = get_optional_input(default="def", input_func=lambda _: "value")
        self.assertEqual(res_filled, "value")

    def test_get_menu_choice(self):
        """get_menu_choice accepts valid choice and rejects out-of-bounds."""
        inputs = iter(["0", "5", "abc", "2"])
        choice = get_menu_choice(3, input_func=lambda _: next(inputs))
        self.assertEqual(choice, 2)

    def test_confirm(self):
        """confirm returns True for 'y'/'yes' and False otherwise."""
        self.assertTrue(confirm(input_func=lambda _: "y"))
        self.assertTrue(confirm(input_func=lambda _: "yes"))
        self.assertFalse(confirm(input_func=lambda _: "n"))
        self.assertFalse(confirm(input_func=lambda _: "no"))


if __name__ == "__main__":
    unittest.main()