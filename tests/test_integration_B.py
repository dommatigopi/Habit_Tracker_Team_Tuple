import unittest
import habits

class TestHabits(unittest.TestCase):
   
    def test_create_habit_exist(self):
        self.assertTure(callable(habits.create_habit))
    
    def test_mark_completed_exists(self):
        self.assertTrue(callable(habits.mark_completed))
            
            
if __name__ == "__main__":
    unittest.main()