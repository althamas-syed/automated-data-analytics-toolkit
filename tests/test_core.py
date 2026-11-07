import tempfile
import unittest
from pathlib import Path
from analytics_toolkit.core import profile_csv

class AnalyticsTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)/"sample.csv"
    def test_profile_and_missing(self):
        self.path.write_text("id,amount,group\n1,10,A\n1,10,A\n2,,B\n3,100,B\n",encoding="utf-8")
        report=profile_csv(self.path)
        self.assertEqual(report["row_count"],4); self.assertEqual(report["duplicate_rows"],1)
        self.assertEqual(report["columns"]["amount"]["missing"],1)
    def test_empty_file(self):
        self.path.write_text("",encoding="utf-8")
        with self.assertRaises(ValueError): profile_csv(self.path)
    def test_malformed_row(self):
        self.path.write_text("a,b\n1,2,3\n",encoding="utf-8")
        with self.assertRaises(ValueError): profile_csv(self.path)
    def test_categorical_counts(self):
        self.path.write_text("region\nSouth\nNorth\nSouth\n",encoding="utf-8")
        self.assertEqual(profile_csv(self.path)["columns"]["region"]["top_values"][0]["count"],2)
    def test_outlier(self):
        self.path.write_text("amount\n10\n11\n12\n13\n1000\n",encoding="utf-8")
        self.assertEqual(profile_csv(self.path)["columns"]["amount"]["iqr_outliers"],1)

if __name__=="__main__": unittest.main()
