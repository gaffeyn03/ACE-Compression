# Ordered Benchmarks

This is the canonical benchmark organization for the paper artifact.

Benchmarks are grouped into a single folder and ordered according to the paper's benchmark sequence:

1. `01_IFEval`
2. `02_gsm8k`
3. `03_human-eval`
4. `04_TruthfulQA`
5. `05_C-eval`
6. `06_roleeval`
7. `07_ToM-Bench`
8. `08_eq-bench`
9. `09_CharacterEval`
10. `10_PsychoBench`

## Shared Dependency

`00_shared/lm-evaluation-harness` contains the shared evaluation harness used by several benchmarks.

## Folder Convention

Source and model-specific scripts are located directly in each numbered directory or its model subdirectories. Some benchmarks also have `lm_eval_tasks/`. Use paths in the included tree rather than adding obsolete `benchmark/` or `launchers/` components.

## Source Mapping

- `01_IFEval`: IFEval launchers
- `02_gsm8k`: GSM8K launchers
- `03_human-eval`: HumanEval benchmark code and runners
- `04_TruthfulQA`: TruthfulQA launchers
- `05_C-eval`: C-Eval launchers
- `06_roleeval`: RoleEval benchmark code, launchers, and custom lm-eval tasks
- `07_ToM-Bench`: ToM-Bench benchmark code
- `08_eq-bench`: EQ-Bench benchmark code
- `09_CharacterEval`: CharacterEval benchmark code
- `10_PsychoBench`: PsychoBench benchmark code

## Compatibility

Use this `paper_benchmarks/` directory as the only benchmark entrypoint in the artifact.
