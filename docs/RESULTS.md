# Results and interpretation

`results/processed/` contains 13 original CSV exports for ten benchmarks. ToMBench has task, ability and subability tables; PsychoBench has numeric-profile and 16P tables. These are preserved from the original evaluation package without adding measurements or imputing missing scores.

Most tables have 37 model-setting rows. TruthfulQA has 41, retaining four historical Qwen-7B-Chat rows. `Psychobench_16P.csv` has 76 rows because multiple personality outcomes per model are intentional. Explicitly select the intended model panel for comparisons.

`Psychobench.csv` has two header rows (questionnaire and dimension) and repeated questionnaire names. Read positionally or with `pandas.read_csv(path, header=[0, 1])`, not a simple dictionary reader. Do not deduplicate 16P by model name alone.

EQ-Bench retains a historical `FAILED` entry for DeepSeek-V2-Lite unstructured sparsity. `FAILED`, `N/A` and blank cells are not zero. Inline uncertainty has benchmark-specific meanings; do not treat every value as an independent-run standard error.

PsychoBench profiles are not monotonic performance scores. ToMBench task, ability and subability outputs are distinct summaries; rounded cells cannot replace raw predictions. Raw outputs are needed to audit item-level scoring or estimate new uncertainty.

Validation checks file integrity and table structure, not scientific validity of inference that was not rerun during packaging. Datasets, weights, raw responses and runtime logs are not included.
