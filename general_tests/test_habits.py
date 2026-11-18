import unittest
from datetime import date, timedelta
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import habits
from habits import (
    HabitObserver,
    create_habit,
    delete_habit,
    find_habit_by_name,
    get_all_habits,
    get_habit,
    get_habit_subject,
    mark_completed,
)


class MockObserver(HabitObserver):

    def __init__(self) -> None:
        self.events: list[tuple[str, dict]] = []

    def update(self, event_type: str, habit: dict) -> None:
        self.events.append((event_type, habit))


class TestHabitsModule(unittest.TestCase):

    def setUp(self):
        self.data = {"habits": []}
        self.mock_observer = MockObserver()
        get_habit_subject().register_observer(self.mock_observer)

    def tearDown(self):
        get_habit_subject().remove_observer(self.mock_observer)

    def test_create_habit(self):
        habit = create_habit(self.data, "Meditation", "Daily 10m", date(2026, 11, 1))
        self.assertTrue(habit["id"].startswith("h_"))
        self.assertEqual(habit["name"], "Meditation")
        self.assertEqual(habit["description"], "Daily 10m")
        self.assertEqual(habit["created_on"], "2026-11-01")
        self.assertEqual(habit["completed_dates"], [])
        self.assertEqual(len(self.data["habits"]), 1)
        # Verify observer was notified
        self.assertTrue(any(e[0] == "habit_created" for e in self.mock_observer.events))

    def test_get_all_habits(self):
        create_habit(self.data, "Habit 1")
        create_habit(self.data, "Habit 2")
        all_habits = get_all_habits(self.data)
        self.assertEqual(len(all_habits), 2)

    def test_get_habit_by_id(self):
        habit = create_habit(self.data, "Drink Water")
        found = get_habit(self.data, habit["id"])
        self.assertIsNotNone(found)
        self.assertEqual(found["name"], "Drink Water")
        self.assertIsNone(get_habit(self.data, "non_existent_id"))

    def test_find_habit_by_name(self):
        create_habit(self.data, "Read Book")
        found = find_habit_by_name(self.data, "read book")
        self.assertIsNotNone(found)
        self.assertIsNone(find_habit_by_name(self.data, "Non existent"))

    def test_mark_completed_and_duplicate_prevention(self):
        habit = create_habit(self.data, "Workout")
        today_str = date.today().strftime("%Y-%m-%d")

        # First completion succeeds
        success = mark_completed(self.data, habit["id"], date.today())
        self.assertTrue(success)
        self.assertIn(today_str, habit["completed_dates"])

        # Second completion on same date returns False
        duplicate_success = mark_completed(self.data, habit["id"], date.today())
        self.assertFalse(duplicate_success)
        self.assertEqual(habit["completed_dates"].count(today_str), 1)

    def test_mark_completed_future_date_rejected(self):
        habit = create_habit(self.data, "Journaling")
        future_date = date.today() + timedelta(days=2)
        success = mark_completed(self.data, habit["id"], future_date)
        self.assertFalse(success)

    def test_delete_habit(self):
        habit = create_habit(self.data, "Floss")
        self.assertTrue(delete_habit(self.data, habit["id"]))
        self.assertEqual(len(self.data["habits"]), 0)
        self.assertFalse(delete_habit(self.data, "unknown_id"))

if __name__ == "__main__":
    unittest.main()