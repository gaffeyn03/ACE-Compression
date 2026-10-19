# Processed Result Validation Scripts

These scripts validate and summarize the processed benchmark result files included in `results/processed/`. They do not rerun model inference and do not require unprocessed evaluation files. The processed CSV files are the canonical result artifacts used to support the submitted paper's reported benchmark tables.

| Script | Purpose |
| --- | --- |
| `check_processed_results.py` | Checks that all expected processed CSV files exist, prints row/column counts, and verifies obvious key columns without modifying data. |
| `check_source_layout.py` | Checks required source backends, lazy model mappings, benchmark/helper paths and original PsychoBench token settings without importing GPU libraries. |
| `validate_release.py` | Checks original CSV hashes, table structure, source layout and packaging manifest. Use `--skip-manifest` after intentional source edits. |
