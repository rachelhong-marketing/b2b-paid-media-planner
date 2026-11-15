import csv
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from launch_checker import checks, files, cli

ROOT = Path(__file__).resolve().parent.parent
SAMPLE = ROOT / "sample-data" / "utm-tracker-sample.csv"
SF = ROOT / "sample-data" / "salesforce-campaigns-sample.csv"
RULES = checks.load_rules()


def run(tracker=SAMPLE, sf=SF):
    rows, _, _, missing = files.read_tracker(tracker)
    assert not missing
    results, notes = checks.check_tracker(rows, RULES, files.read_salesforce(sf) if sf else None)
    return {r["row"]: r for r in results}, notes


def errors(result):
    return [(f, m) for level, f, m in result["issues"] if level == checks.ERROR]


def warns(result):
    return [(f, m) for level, f, m in result["issues"] if level == checks.WARN]


class Values(unittest.TestCase):
    def test_suggest(self):
        self.assertEqual(checks.suggest(" Carousel CMO_v2 "), "carousel-cmo-v2")

    def test_build_keeps_existing_query(self):
        url = checks.build_url("https://a.example/p?ref=nav", {"utm_source": "linkedin", "utm_medium": "paid-social",
                                                                "utm_campaign": "2026-q3-x"})
        self.assertEqual(url, "https://a.example/p?ref=nav&utm_source=linkedin&utm_medium=paid-social&utm_campaign=2026-q3-x")

    def test_clean_values_pass(self):
        p = {"utm_source": "google", "utm_medium": "paid-search", "utm_campaign": "2026-q3-brand", "utm_term": "b2b-attribution"}
        self.assertEqual(checks.check_values(p, RULES), [])


class SampleTracker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r, cls.notes = run()

    def test_clean_rows(self):
        self.assertEqual(self.r[2]["issues"], [])
        self.assertEqual(self.r[6]["issues"], [])

    def test_planted_errors(self):
        r = self.r
        self.assertIn("utm_content", [f for f, _ in errors(r[3])])          # duplicate test version
        self.assertEqual(len(errors(r[4])), 2)                               # capitals + space
        self.assertIn("utm_medium", [f for f, _ in errors(r[5])])           # linkedin + paid-search
        self.assertIn("Full Tagged URL", [f for f, _ in errors(r[8])])      # link doesn't match columns
        self.assertIn("linkedin", errors(r[9])[0][1])                        # typo suggestion
        self.assertEqual(len(errors(r[12])), 2)                              # space + http
        self.assertIn("Salesforce", [f for f, _ in errors(r[13])])          # no Salesforce campaign

    def test_planted_warnings(self):
        r = self.r
        self.assertEqual({f for f, _ in warns(r[7])}, {"utm_content", "Salesforce"})
        self.assertIn("utm_campaign", [f for f, _ in warns(r[10])])         # no year
        self.assertIn("2026-q4", warns(r[11])[0][1])                         # launches in another quarter
        self.assertEqual({f for f, _ in warns(r[14])}, {"utm_term", "Salesforce"})
        self.assertIn("Completed", warns(r[15])[0][1])

    def test_gclid_note(self):
        self.assertTrue(any("GCLID" in n for n in self.notes))


class FixedCopy(unittest.TestCase):
    def test_format_fixes_clear_format_errors(self):
        out = Path(tempfile.mkdtemp()) / "fixed.csv"
        _, mapping, _, _ = files.read_tracker(SAMPLE)
        files.write_fixed(SAMPLE, out, mapping)
        r, _ = run(out)
        self.assertEqual(errors(r[4]), [])                                   # capitals and space fixed
        self.assertEqual(errors(r[8]), [])                                   # link rebuilt from the columns
        self.assertIn("utm_medium", [f for f, _ in errors(r[5])])           # judgment calls are left alone


class Commands(unittest.TestCase):
    def test_build_refuses_bad_value(self):
        with redirect_stdout(io.StringIO()) as out:
            code = cli.main(["build", "--url", "https://a.example", "--source", "linkedin", "--medium", "paid-social",
                             "--campaign", "2026-q3-x", "--content", "Video CFO"])
        self.assertEqual(code, 1)
        self.assertIn("video-cfo", out.getvalue())

    def test_template_is_clean(self):
        with redirect_stdout(io.StringIO()):
            code = cli.main(["check", str(ROOT / "templates" / "utm-tracker-template.csv")])
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
