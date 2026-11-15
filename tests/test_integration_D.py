import unittest
import reports



class  testReports(unittest.Testcase):

    def test_sumaary_report_exists(self):
        self.assertTrue(callable(reports.generate_summary_report))
    
    def test_chart_function_exists(self):
        self.assertTrue(callable(reports.generate_chart))


if __name__ == "__main__":
    unittest.main()