# ACE-Compression

English | [简体中文](README_zh-CN.md)

Code and evaluation results for **ACE-Compression: An Ability-Centric Evaluation of Compressed Large Language Models**.

ACE-Compression evaluates how quantization and pruning affect different abilities of large language models. It organizes ten benchmarks into four ability dimensions and provides model-specific evaluation scripts, compression tools, serving templates and processed results.

## Evaluation coverage

| Ability dimension | Benchmarks |
|---|---|
| Procedural reasoning | IFEval, GSM8K, HumanEval |
| Knowledge grounding | TruthfulQA, C-Eval, RoleEval |
| Social cognition | ToMBench, EQ-Bench |
| Persona fidelity | CharacterEval, PsychoBench |

The model panel includes Qwen2.5-7B/14B/32B, Llama3.1-8B/70B and DeepSeek-V2-Lite-16B. Evaluated settings include FP16, bitsandbytes 4-bit, AWQ, GPTQ-INT4/INT8, 2:4 structured sparsity, unstructured sparsity and model-specific trimming. Available settings vary by model; see [model configurations](configs/models.yaml) and [compression settings](configs/compression_methods.yaml).

## Repository structure

```text
paper_benchmarks/             Ten benchmark pipelines and shared lm-eval source
compression/pruning_scripts/  Per-model pruning scripts and compression toolkit
serving/                      Model-specific vLLM startup templates
configs/                      Models, compression methods and benchmark settings
results/processed/            Thirteen benchmark result CSVs
scripts/report_sync/          Raw-output aggregation and report utilities
scripts/prepare_results/      Result integrity and source-layout checks
tests/                        Offline regression tests
docs/                         Reproducibility, result and validation notes
```

## Setup

Use Python 3.10 or newer. GPU evaluation requires a compatible NVIDIA/CUDA, PyTorch and vLLM environment. `requirements.txt` lists dependencies with version bounds; it is not a tested lockfile. Pruning, inference and reward-model scoring may require separate environments.

```bash
git clone https://github.com/gaffeyn03/ACE-Compression.git
cd ACE-Compression
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e ./paper_benchmarks/00_shared/lm-evaluation-harness
```

For the pruning tools, install the relevant dependencies in a compatible environment:

```bash
pip install llmcompressor
pip install -e './compression/pruning_scripts/TransformerCompression[experiment]'
```

Model checkpoints, tokenizer files, full benchmark datasets and reward-model weights must be obtained separately. Sources and applicable terms are listed in [ASSETS.md](ASSETS.md).

## Running evaluations

1. Obtain the checkpoints and benchmark inputs, then review [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for expected data locations and environment requirements.
2. Configure checkpoint paths, GPU IDs, ports and environments in the selected model scripts.
3. Run the appropriate pipeline under `paper_benchmarks/`. Start a matching `serving/` template when an OpenAI-compatible vLLM endpoint is required.
4. Use `scripts/report_sync/` to aggregate matching raw outputs. New consolidated summaries are written to `results/generated/`; the distributed CSVs remain unchanged.

IFEval, GSM8K, HumanEval, TruthfulQA and C-Eval use the shared evaluation harness. RoleEval has benchmark-specific model runners. ToMBench, EQ-Bench, CharacterEval and PsychoBench include their own API/evaluation pipelines. See [WORKFLOW.md](WORKFLOW.md) for entrypoints and the evaluation sequence.

**HumanEval executes generated code. Run it in a disposable, isolated environment without credentials or access to valuable files.**

## Results

`results/processed/` contains thirteen CSV files covering all ten benchmarks. ToMBench provides task, ability and subability summaries; PsychoBench provides numeric-profile and 16P results.

- `Psychobench.csv` has two header rows. Use a positional CSV reader or `pandas.read_csv(path, header=[0, 1])`.
- `Psychobench_16P.csv` can contain multiple personality outcomes for one model; do not deduplicate by model name alone.
- Missing values and `FAILED` entries are not zero scores. Psychometric profile values are not uniformly higher-is-better performance measures.

Read [result definitions and limitations](docs/RESULTS.md) before comparing scores. Raw generations and runtime logs are not distributed.

## Offline checks

These commands require only the Python standard library; no checkpoints, GPU or network access are needed:

```bash
python3 scripts/prepare_results/check_processed_results.py
python3 scripts/prepare_results/check_source_layout.py
python3 scripts/prepare_results/validate_release.py
python3 -m unittest discover -s tests -v
```

The checks cover table structure, result hashes, required source files, helper paths and regression cases. They do not run model inference. After intentional source edits, use `validate_release.py --skip-manifest` to skip the packaging snapshot hashes. See [validation scope](docs/VALIDATION.md).

## Documentation

- [Evaluation workflow](WORKFLOW.md)
- [Reproducibility and external inputs](REPRODUCIBILITY.md)
- [Compute estimate and assumptions](COMPUTE_ESTIMATE.md)
- [Assets and licenses](ASSETS.md)

## License

The root [MIT license](LICENSE) applies to ACE-Compression-authored scripts and documentation. Bundled third-party source retains its own license, including PsychoBench's GPL-3.0 license. Dataset and model terms remain separate; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and [ASSETS.md](ASSETS.md).
