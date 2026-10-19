# Report Sync Utilities

These scripts document the original raw-report aggregation workflow. New consolidated summaries are written to `results/generated/`, leaving the original CSVs in `results/processed/` unchanged. Matching raw outputs and official metadata are required; source release files alone cannot recreate generated responses.

These scripts parse the specific output format of each benchmark's raw result files and may require adaptation for different benchmark versions or output formats.

| Script | Benchmarks covered | Description |
|---|---|---|
| `sync_numeric_reports.py` | IFEval, C-Eval, TruthfulQA | Aggregates numeric metrics from raw lm-eval outputs |
| `sync_gsm8k_reports.py` | GSM8K | Aggregates GSM8K strict/flexible match scores |
| `sync_charactereval_reports.py` | CharacterEval | Aggregates CharacterEval dimension scores |
| `sync_eq_tom_reports.py` | EQ-Bench, ToM-Bench | Aggregates EQ-Bench scores and ToM-Bench ability/task breakdowns |
| `sync_psychobench_reports.py` | PsychoBench | Aggregates PsychoBench questionnaire and 16P results |
| `validate_psychobench_summary.py` | PsychoBench | Validates PsychoBench summary consistency |
| `fix_tombench_result_language_fields.py` | ToM-Bench | Fixes language field labels in ToM-Bench results |
| `repair_psychobench_from_responses.py` | PsychoBench | Repairs PsychoBench results from raw responses |
| `rerun_psychobench_queue.py` | PsychoBench | Queue-based rerun utility for PsychoBench |

## Usage Notes

These scripts were designed for a specific directory layout and raw output format. They are provided as reference for understanding the result aggregation pipeline. Running them requires:

- Raw benchmark output files (not included in this package)
- The specific directory structure used during evaluation
- Python dependencies (numpy, pandas, etc.)

They are not intended as a general-purpose tool and may need modification for different setups.
