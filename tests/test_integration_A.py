import tempfile
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import habits
import storage


class TestStorageIntegration(unittest.TestCase):

    def test_habit_creation_and_persistent_storage(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "habits.json"
            data = storage.load_data(path)
            self.assertEqual(data, {"habits": []})

            # Create a habit using habits module
            habits.create_habit(data, "Morning Run", "5km running")
            storage.save_data(data, path)

            # Reload from disk and verify
            reloaded = storage.load_data(path)
            self.assertEqual(len(reloaded["habits"]), 1)
            self.assertEqual(reloaded["habits"][0]["name"], "Morning Run")

    def test_save_handles_nested_directories(self):
        with tempfile.TemporaryDirectory() as folder:
            nested_path = Path(folder) / "sub" / "dir" / "data.json"
            data = {"habits": []}
            self.assertTrue(storage.save_data(data, nested_path))
            self.assertTrue(nested_path.exists())


if __name__ == "__main__":
    unittest.main()

