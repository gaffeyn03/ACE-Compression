"""Offline release tests: no models, network or third-party dependencies."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts/prepare_results"))
from validate_release import check_table, table, validate, validate_manifest


class ReleaseTests(unittest.TestCase):
    def test_original_tables(self):
        self.assertEqual(len(validate(ROOT, check_manifest=False)), 13)

    def test_psychobench_two_headers(self):
        self.assertEqual(check_table("Psychobench.csv", table(ROOT / "results/processed/Psychobench.csv")), 37)

    def test_multiple_personality_outcomes(self):
        self.assertEqual(check_table("Psychobench_16P.csv", table(ROOT / "results/processed/Psychobench_16P.csv")), 76)

    def test_failed_values_preserved(self):
        rows = table(ROOT / "results/processed/eq-bench.csv")
        self.assertTrue(any("FAILED" in row for row in rows[1:]))
        self.assertEqual(check_table("eq-bench.csv", rows), 37)

    def test_reject_ragged_duplicate_blank_or_extra(self):
        original = table(ROOT / "results/processed/IFEval.csv")
        bad = []
        rows = copy.deepcopy(original); rows[1].pop(); bad.append(rows)
        rows = copy.deepcopy(original); rows[1][0] = rows[2][0]; bad.append(rows)
        rows = copy.deepcopy(original); rows[1][0] = ""; bad.append(rows)
        rows = copy.deepcopy(original); rows.append(["new-setting"] + rows[1][1:]); bad.append(rows)
        for rows in bad:
            with self.subTest(rows=len(rows)), self.assertRaises(ValueError):
                check_table("IFEval.csv", rows)

    def test_reject_missing_file(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(FileNotFoundError):
                validate(Path(folder), check_manifest=False)

    def test_manifest_tampering_and_path_escape(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            data = b"example\n"
            (root / "sample.txt").write_bytes(data)
            entry = {"path": "sample.txt", "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
            def write_manifest(item):
                (root / "RELEASE_MANIFEST.json").write_text(json.dumps({"files": [item]}))
            write_manifest(entry)
            self.assertEqual(validate_manifest(root), 1)
            (root / "sample.txt").write_bytes(b"tampered")
            with self.assertRaises(ValueError):
                validate_manifest(root)
            write_manifest({**entry, "path": "../sample.txt"})
            with self.assertRaises(ValueError):
                validate_manifest(root)


if __name__ == "__main__":
    unittest.main()
