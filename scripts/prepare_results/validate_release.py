#!/usr/bin/env python3
"""Read-only standard-library checks for the original evaluation release."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
from check_processed_results import EXPECTED_CSVS
from check_source_layout import check_layout

ROOT = Path(__file__).resolve().parents[2]
EXPECTED_ROWS = {name: 37 for name in EXPECTED_CSVS}
EXPECTED_ROWS.update({"TruthfulQA.csv": 41, "Psychobench_16P.csv": 76})
EXCLUDED_PATHS = (
    "experiments", "analysis", "results/retention", "requirements-analysis.txt",
    "docs/EXPERIMENTS.md", "compression/pruning_scripts/run_unstructured.py",
    "compression/pruning_scripts/run_bnb8.py", "compression/pruning_scripts/run_wanda.py",
    "compression/pruning_scripts/run_calibration.py",
)


def table(path: Path) -> list[list[str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.reader(handle))


def check_table(name: str, rows: list[list[str]]) -> int:
    start = 2 if name == "Psychobench.csv" else 1
    if len(rows) <= start:
        raise ValueError(f"Empty score table: {name}")
    if not set(EXPECTED_CSVS[name]).issubset(rows[0]):
        raise ValueError(f"Missing columns: {name}")
    if any(len(row) != len(rows[0]) for row in rows):
        raise ValueError(f"Ragged CSV: {name}")
    models = [row[0].strip() for row in rows[start:]]
    if not all(models):
        raise ValueError(f"Blank model: {name}")
    if name != "Psychobench_16P.csv" and len(models) != len(set(models)):
        raise ValueError(f"Duplicate model: {name}")
    if len(models) != EXPECTED_ROWS[name]:
        raise ValueError(f"Unexpected release row count: {name}: {len(models)}")
    return len(models)


def validate_manifest(root: Path) -> int:
    manifest = json.loads((root / "RELEASE_MANIFEST.json").read_text(encoding="utf-8"))
    root = root.resolve()
    seen = set()
    for entry in manifest["files"]:
        relative = Path(entry["path"])
        if relative.is_absolute() or ".." in relative.parts or entry["path"] in seen:
            raise ValueError(f"Invalid/duplicate manifest path: {relative}")
        path = root / relative
        if not path.resolve().is_relative_to(root) or path.is_symlink() or not path.is_file():
            raise ValueError(f"Missing/nonregular file: {relative}")
        content = path.read_bytes()
        if len(content) != entry["bytes"] or hashlib.sha256(content).hexdigest() != entry["sha256"]:
            raise ValueError(f"Changed file: {relative}")
        seen.add(entry["path"])
    return len(seen)


def validate(root: Path = ROOT, check_manifest: bool = True) -> dict[str, int]:
    for relative in EXCLUDED_PATHS:
        if (root / relative).exists():
            raise ValueError(f"Outside original evaluation release scope: {relative}")
    counts = {name: check_table(name, table(root / "results/processed" / name))
              for name in EXPECTED_CSVS}
    expected = json.loads((root / "scripts/prepare_results/original_result_hashes.json").read_text(encoding="utf-8"))
    for name in EXPECTED_CSVS:
        digest = hashlib.sha256((root / "results/processed" / name).read_bytes()).hexdigest()
        if digest != expected["csv_sha256"][name]:
            raise ValueError(f"Original anonymous result changed: {name}")
    check_layout(root)
    if check_manifest:
        counts["manifest_files_verified"] = validate_manifest(root)
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-manifest", action="store_true", help="Check structure after intentional source edits")
    args = parser.parse_args()
    try:
        counts = validate(check_manifest=not args.skip_manifest)
    except (OSError, ValueError, KeyError) as error:
        print(f"FAIL: {error}")
        return 1
    for name, count in counts.items():
        print(f"OK {name}: {count}")
    print("PASS: original evaluation tables and distributed-file checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
