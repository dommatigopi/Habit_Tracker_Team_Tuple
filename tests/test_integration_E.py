import unittest
import main
import utils

class TestMain(unittest.TestCase):

  def test_main_function_exists(self):
    self.assertTrue(callable(main.run_app))

  def test_menu_function_exists(self):
    self.assertTrue(callable(utils.display_menu))

if__name__=="__main__":
    unittest.main()