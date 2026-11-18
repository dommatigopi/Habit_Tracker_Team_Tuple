import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import storage

class TestStorageModule(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = Path(self.temp_dir.name) / "test_habits.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_load_data_nonexistent_file(self):       
        data = storage.load_data(self.test_file)
        self.assertEqual(data, {"habits": []})

    def test_save_and_load_roundtrip(self):
       
        sample = {
            "habits": [
                {
                    "id": "habit_1",
                    "name": "Exercise",
                    "description": "Daily 30-minute workout",
                    "created_on": "2026-11-01",
                    "completed_dates": ["2026-11-01", "2026-11-02"]
                }
            ]
        }
        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump(sample, f)

        loaded = storage.load_data(self.test_file)
        self.assertEqual(loaded, sample)

    def test_load_data_invalid_json(self):
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("{invalid_json: true,}")

        with self.assertRaises(ValueError):
            storage.load_data(self.test_file)

    def test_load_data_invalid_schema(self):
      
        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump({"wrong_key": []}, f)

        with self.assertRaises(ValueError):
            storage.load_data(self.test_file)

    def test_save_data_callable(self):
    
        self.assertTrue(callable(storage.save_data))

if __name__ == "__main__":
    unittest.main()
