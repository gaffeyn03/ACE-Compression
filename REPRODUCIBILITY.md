# Reproducibility

## Offline checks

The release includes 13 original processed benchmark tables. Standard-library checks validate required columns, row shapes, model names, release row counts and file hashes. They do not independently establish the correctness of scores or reconstruct inference from raw responses.

```bash
python3 scripts/prepare_results/check_processed_results.py
python3 scripts/prepare_results/validate_release.py
python3 -m unittest discover -s tests -v
```

`RELEASE_MANIFEST.json` records packaged files. After intentional source edits, use `validate_release.py --skip-manifest` for structural checks. CI skips packaging hashes so ordinary source edits can be tested. The manifest is not an inference audit.

## GPU evaluation

Use Linux, NVIDIA GPUs and Python 3.10+. Prepare a CUDA-compatible PyTorch/vLLM stack and benchmark-specific dependencies. Install the bundled harness where required:

```bash
pip install -e ./paper_benchmarks/00_shared/lm-evaluation-harness
```

`requirements.txt` is an inherited dependency inventory with lower bounds, not a tested lockfile. Quantization, pruning, reward-model and inference packages may require separate environments. Historical checkpoint revisions and software commits were not systematically logged; record exact versions for new runs.

Model-specific launchers are templates. Review checkpoint paths, GPU IDs, ports, Conda activation and output directories before execution. See `configs/` and `WORKFLOW.md`. HumanEval executes generated code: use an isolated, disposable environment.

## External inputs

Obtain assets from the links in `ASSETS.md`. Processed score CSVs are not benchmark input data.

| Benchmark | Expected local inputs |
|---|---|
| IFEval, GSM8K, HumanEval, TruthfulQA, C-Eval | Dataset/cache required by the included task definitions |
| RoleEval | `paper_benchmarks/06_roleeval/upstream/{en,zh}/{chinese,global}/{dev,test}/*.csv` |
| ToMBench | Official JSONL task files under `paper_benchmarks/07_ToM-Bench/data/` |
| EQ-Bench | `paper_benchmarks/08_eq-bench/data/eq_bench_v2_questions_171.json` |
| CharacterEval | Official `upstream_official/data/` and separately downloaded BaichuanCharRM code, tokenizer and weights |
| PsychoBench | Official `questionnaires.json` under `paper_benchmarks/10_PsychoBench/` |

Pruning templates specify their own dependencies and calibration inputs; obtain them separately. Report converters require matching raw outputs and may need adaptation for another output format. Generated summaries go to `results/generated/`, leaving the distributed tables unchanged.

## Limits

No full environment installation, checkpoint pruning, inference or external API evaluation was rerun for this release. Weights, datasets, raw responses and logs are omitted. Third-party software, datasets and APIs can change; templates and processed scores do not alone guarantee exact reproduction.
