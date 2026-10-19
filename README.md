# ACE-Compression

Evaluation code and processed results for **ACE-Compression: An Ability-Centric Evaluation of Compressed Large Language Models**.

Ten benchmarks cover instruction following, reasoning, knowledge, social cognition and psychometric profiles: IFEval, GSM8K, HumanEval, TruthfulQA, C-Eval, RoleEval, ToMBench, EQ-Bench, CharacterEval and PsychoBench. The original model panel includes Qwen2.5 (7B/14B/32B), Llama3.1 (8B/70B) and DeepSeek-V2-Lite (16B), with dense and compressed settings recorded in the result tables.

## Quick checks

These offline commands use only the Python standard library:

```bash
python3 scripts/prepare_results/check_processed_results.py
python3 scripts/prepare_results/validate_release.py
python3 -m unittest discover -s tests -v
```

Use Python 3.10+. This is a research artifact, not a one-command reproduction environment. GPU evaluation requires separately prepared models, benchmark data and compatible dependencies.

## Repository layout

```text
paper_benchmarks/            Ten benchmark pipelines and shared lm-eval source
configs/                     Model, compression and benchmark configuration notes
serving/                     Per-model vLLM serving templates
compression/pruning_scripts/  Original per-model pruning templates and toolkit
results/processed/           Thirteen original benchmark result CSVs
scripts/                    Raw-report aggregation and offline validation
tests/                      Offline release-integrity tests
```

## Running the evaluation

1. Obtain checkpoints and benchmark assets listed in [ASSETS.md](ASSETS.md), respecting their terms.
2. Prepare compatible environments following [REPRODUCIBILITY.md](REPRODUCIBILITY.md).
3. Follow [WORKFLOW.md](WORKFLOW.md) to select model-specific serving, evaluation and report-conversion templates.

Read [result definitions](docs/RESULTS.md) before interpreting CSVs. `Psychobench.csv` has two header rows; `Psychobench_16P.csv` has multiple rows per model. Failed/missing scores are not zero, and psychometric profiles are not higher-is-better performance scores.

Model weights, full benchmark datasets, raw generations, logs and private working records are not distributed. Task definitions and prompt templates are included where present. No GPU evaluation was rerun during packaging. See [validation scope](docs/VALIDATION.md).

## License

The root [MIT license](LICENSE) applies to ACE-authored scripts and documentation, not all bundled third-party code or datasets. Upstream licenses remain in their directories; PsychoBench retains GPL-3.0. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and [ASSETS.md](ASSETS.md).
