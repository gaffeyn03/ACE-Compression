"""Offline release tests: no models, network or third-party dependencies."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts/prepare_results"))
from validate_release import check_table, table, validate, validate_manifest
from check_source_layout import check_backends, check_generator, check_layout, GENERATORS, HARNESS


def load_helper(name):
    module_name = "ace_test_" + name
    spec = importlib.util.spec_from_file_location(module_name, ROOT / "scripts/report_sync" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    previous_path = sys.path[:]
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = previous_path
    return module


class ReleaseTests(unittest.TestCase):
    def test_model_backends_and_layout(self):
        counts = check_layout(ROOT)
        self.assertEqual(counts["model_backend_files"], 24)
        self.assertEqual(counts["model_backend_tests"], 9)
        self.assertGreaterEqual(counts["lazy_backend_mappings"], 24)

    def test_missing_model_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            destination = root / HARNESS / "lm_eval/models"
            shutil.copytree(ROOT / HARNESS / "lm_eval/models", destination)
            (destination / "vllm_causallms.py").unlink()
            with self.assertRaisesRegex(ValueError, "model-backend SOURCE"):
                check_backends(root)

    def test_original_psychobench_token_budget(self):
        for name in GENERATORS:
            check_generator(ROOT / "paper_benchmarks/10_PsychoBench" / name)

    def test_changed_psychobench_token_budget_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "generator.py"
            path.write_text("class Generator:\n    def chat(self, messages, max_tokens=512):\n        pass\ngenerator.chat([], max_tokens=512)\n")
            with self.assertRaisesRegex(ValueError, "1024"):
                check_generator(path)

    def test_report_modules_import_and_resolve_roots(self):
        names = ("fix_tombench_result_language_fields", "rerun_psychobench_queue",
                 "sync_charactereval_reports", "sync_eq_tom_reports", "sync_gsm8k_reports",
                 "sync_numeric_reports", "sync_psychobench_reports", "validate_psychobench_summary")
        directory_names = ("GSM8K_ROOT", "CHAR_ROOT", "EQ_ROOT", "TOM_ROOT", "PSYCHO_ROOT", "PB_ROOT", "TOMBENCH_ROOT")
        for name in names:
            with self.subTest(name=name):
                module = load_helper(name)
                self.assertEqual(module.ROOT.resolve(), ROOT.resolve())
                for attribute in directory_names:
                    if hasattr(module, attribute):
                        self.assertTrue(getattr(module, attribute).is_dir(), attribute)
                if hasattr(module, "REPORT_SUMMARY_ROOT"):
                    self.assertEqual(module.REPORT_SUMMARY_ROOT, ROOT / "results/generated")

    def test_numeric_collectors_use_original_benchmark_directories(self):
        module = load_helper("sync_numeric_reports")
        checks = (("build_humaneval_rows", "collect_humaneval_file", "03_human-eval", "key", True),
                  ("build_ceval_rows", "collect_ceval_json", "05_C-eval", "ceval_dir", False),
                  ("build_roleeval_rows", "collect_roleeval_json", "06_roleeval", "roleeval_dir", True))
        for config in module.GROUPS:
            for builder, collector, benchmark, attribute, result_subdir in checks:
                expected = ROOT / "paper_benchmarks" / benchmark / getattr(config, attribute)
                self.assertTrue(expected.is_dir(), str(expected))
                if result_subdir:
                    expected = expected / "results"
                with patch.object(module, collector, return_value=None) as mocked:
                    self.assertEqual(getattr(module, builder)(config), [])
                    self.assertTrue(mocked.called)
                    self.assertTrue(all(call.args[0] == expected for call in mocked.call_args_list))

    def test_gsm8k_converter_on_synthetic_output(self):
        module = load_helper("sync_gsm8k_reports")
        config = module.GROUPS[0]
        variant = config.variants[0]
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            benchmark_root = root / "paper_benchmarks/02_gsm8k"
            result_dir = benchmark_root / config.benchmark_dir / "results"
            result_dir.mkdir(parents=True)
            result = {"exact_match,strict-match":0.5, "exact_match_stderr,strict-match":0.1,
                      "exact_match,flexible-extract":0.75, "exact_match_stderr,flexible-extract":0.05}
            (result_dir / ("gsm8k_cot_" + variant.aliases[0] + ".json")).write_text(json.dumps({"results":{"gsm8k_cot":result}}))
            with patch.object(module, "GSM8K_ROOT", benchmark_root), patch.object(module, "REPORT_ROOT", root / "report"):
                rows = module.sync_group(config)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[1][1:], ["0.5000", "0.1000", "0.7500", "0.0500"])
            self.assertTrue((benchmark_root / config.benchmark_dir / "gsm8k_results_summary.csv").is_file())

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
