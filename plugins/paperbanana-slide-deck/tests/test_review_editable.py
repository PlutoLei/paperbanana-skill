import importlib.util
import pathlib
import unittest

MODULE = pathlib.Path(__file__).parents[1] / "scripts/editable/review-editable.py"
SPEC = importlib.util.spec_from_file_location("review_editable", MODULE)
review = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(review)

class MappingTest(unittest.TestCase):
    def test_unmapped_critic_text_is_fail_closed(self):
        got = review.map_suggestions("slide-02", ["title-text", "native-chart"],
                                     ["native-chart: labels overlap", "reduce clutter"])
        self.assertEqual(got[0], "slide-02/native-chart: labels overlap")
        self.assertEqual(got[1], "slide-02/unmapped: reduce clutter")

if __name__ == "__main__":
    unittest.main()
