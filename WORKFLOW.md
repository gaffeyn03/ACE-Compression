# Evaluation workflow

Run commands from the repository root after reading [REPRODUCIBILITY.md](REPRODUCIBILITY.md).

## 1. Prepare checkpoints

Use the original dense/quantized checkpoints and model mappings in `configs/`. Per-family templates under `compression/pruning_scripts/` document the original structured/unstructured pruning setup. Inspect model paths, dependencies, GPUs and output directories before running them. The bundled TransformerCompression source retains its upstream license.

## 2. Select the benchmark runner

`paper_benchmarks/` has ten numbered directories; scripts are located directly in those directories or their model subdirectories. The shared harness is under `00_shared/lm-evaluation-harness/`.

IFEval, GSM8K, HumanEval, TruthfulQA and C-Eval use harness/task-based evaluation. RoleEval has model-specific runners. ToMBench, EQ-Bench, CharacterEval and PsychoBench include benchmark-specific API/evaluation pipelines. Use matching `serving/` templates when an OpenAI-compatible vLLM endpoint is needed.

Set checkpoint paths, endpoint/port and GPU selection; obtain external inputs and inspect output paths. Do not assign one GPU/port to concurrent processes. HumanEval executes generated code: isolate it from credentials and valuable files.

## 3. Convert reports

`scripts/report_sync/` contains per-benchmark report converters and repair helpers. Read its README and each selected script first. They require real raw outputs and matching metadata; packaged CSVs cannot regenerate predictions.

Converters write to `results/generated/`. Compare new summaries with `results/processed/` without silently overwriting distributed results. Preserve failed/missing values and benchmark-specific headers and aggregation conventions.

## 4. Check packaged results

```bash
python3 scripts/prepare_results/check_processed_results.py
python3 scripts/prepare_results/validate_release.py
python3 -m unittest discover -s tests -v
```

After intentional source edits, `validate_release.py --skip-manifest` skips packaging hashes, not table structure or release-scope checks.
