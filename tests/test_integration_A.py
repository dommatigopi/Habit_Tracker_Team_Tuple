import unittest
import storage 
import tempfile
from pathlib import Path


class TestStorage(unittest.TestCase):

    def test_load_data(self):
        with tempfile.TemporarayDirectory() as folder:
            path = Path(folder) / "habits.json"
            data = storage.load_data(path)
            self.assertEqual(data, {"habits":[]})

    def test_save_function_exists(self):
        self.assertTrue(callable(storage.save_data))


if __name__ == "__main__":
    unittest.main()