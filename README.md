# ACE-Compression

Public code package for **ACE-Compression: An Ability-Centric Evaluation of Compressed Large Language Models**, based on the original anonymous release. It includes benchmark evaluation code, compression/pruning scripts, model serving templates, configuration documentation, processed results, helper scripts, and asset/license documentation. Model weights, tokenizer caches, benchmark datasets and raw evaluation logs are not included.

The original release's file coverage and evaluation settings are retained, with directory-path fixes for the included layout. The shared harness includes its model-backend source and upstream tests; directories named `lm_eval/models/` or `tests/models/` contain code, not checkpoint weights. See [release notes](docs/RELEASE_NOTES.md) for the changes and [validation scope](docs/VALIDATION.md) for what was checked.

## Package Purpose

This package provides the code and processed results needed to understand and verify the ACE-Compression paper's experiments, which evaluate how different compression methods (quantization, pruning, sparsity) affect LLM performance across 10 benchmarks spanning four ability dimensions.

## Folder Structure

```
ACE-Compression/
├── README.md                    # This file
├── WORKFLOW.md                  # Detailed workflow documentation
├── REPRODUCIBILITY.md           # Reproducibility scope and notes
├── ASSETS.md                    # Third-party asset and license summary
├── LICENSE                      # MIT license (applies to supplementary code/docs)
├── requirements.txt             # Python dependencies
├── configs/                     # Configuration documentation
│   ├── models.yaml              # Model checkpoint sources and variants
│   ├── compression_methods.yaml # Compression methods and tooling
│   └── benchmarks.yaml          # Benchmark sources and metric columns
├── paper_benchmarks/            # Benchmark evaluation code
│   ├── 00_shared/               # Shared lm-evaluation-harness
│   ├── 01_IFEval/               # IFEval launchers
│   ├── 02_gsm8k/                # GSM8K launchers
│   ├── 03_human-eval/           # HumanEval benchmark code
│   ├── 04_TruthfulQA/           # TruthfulQA launchers
│   ├── 05_C-eval/               # C-Eval launchers
│   ├── 06_roleeval/             # RoleEval benchmark code & launchers
│   ├── 07_ToM-Bench/            # ToM-Bench benchmark code
│   ├── 08_eq-bench/             # EQ-Bench benchmark code
│   ├── 09_CharacterEval/        # CharacterEval benchmark code
│   └── 10_PsychoBench/          # PsychoBench benchmark code
├── compression/                 # Compression / pruning code
│   └── pruning_scripts/         # SparseGPT pruning scripts per model
├── serving/                     # vLLM model serving startup scripts
├── results/processed/           # Canonical processed result CSV files
├── scripts/                     # Helper and report-sync utilities
│   ├── prepare_results/         # Processed-result validation
│   └── report_sync/             # Report aggregation utilities
├── docs/                        # Supplementary documentation
└── tables/                      # Reserved for table exports
```

## Setup

Use Python 3.10+. `requirements.txt` is the inherited dependency inventory, not a tested lockfile. Inference, pruning, reward-model scoring and individual benchmarks may need separate compatible environments. Review each template's checkpoint paths, ports, GPU IDs and Conda activation before running. HumanEval executes generated code: use a disposable, isolated environment.

```bash
cd ACE-Compression
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The included validation script uses only the Python standard library.

For benchmark execution, additionally install:

```bash
pip install -e ./paper_benchmarks/00_shared/lm-evaluation-harness
```

For pruning, additionally install llmcompressor and the TransformerCompression package:

```bash
pip install llmcompressor
pip install -e ./compression/pruning_scripts/TransformerCompression[experiment]
```

## Inspecting the Workflow

See [WORKFLOW.md](WORKFLOW.md) for a detailed description of:
- Where benchmark evaluation code lives
- Where compression/pruning/quantization code lives
- Where configs and processed results live
- How processed CSV files are produced
- What external assets users need to obtain
- Which scripts are directly runnable vs. command templates

## Validating Processed Results

```bash
python3 scripts/prepare_results/check_processed_results.py
python3 scripts/prepare_results/check_source_layout.py
python3 scripts/prepare_results/validate_release.py
python3 -m unittest discover -s tests -v
```

This command checks that all canonical processed result files are present, prints row and column counts, and reports obvious required-column warnings without modifying data.

## Where Things Are

### Benchmark Evaluation Code

Located in `paper_benchmarks/`, organized by benchmark number:
- **Category A** (direct lm-eval): IFEval, GSM8K, HumanEval, TruthfulQA, C-Eval
- **RoleEval**: benchmark-specific model runners
- **Category B** (requires vLLM service): ToM-Bench, EQ-Bench, CharacterEval, PsychoBench

### Compression Code

Located in `compression/pruning_scripts/`:
- Per-model SparseGPT pruning scripts (2:4 structured and unstructured sparsity)
- TransformerCompression (SliceGPT) framework
- Environment setup and usage guides

### Model Serving Templates

Located in `serving/`, organized by model family. These are vLLM startup scripts for each compression variant.

### Processed Results

Located in `results/processed/`:
- 13 canonical CSV files covering all 10 benchmarks

These CSVs are byte-identical to the original anonymous release. `Psychobench.csv` uses two header rows, and `Psychobench_16P.csv` has multiple personality outcomes per model. Failed or missing values are not zero scores. New report conversions write to `results/generated/`, leaving the packaged original tables unchanged. See [results](docs/RESULTS.md).

### Report Sync Utilities

Located in `scripts/report_sync/`:
- Scripts for aggregating raw benchmark outputs into processed summary CSV files
- Scripts for validating and repairing result files

## What Is Included

- Benchmark evaluation code and launcher scripts under `paper_benchmarks/`
- Compression/pruning scripts under `compression/`
- vLLM serving startup templates under `serving/`
- Processed benchmark result files under `results/processed/`
- Configuration summaries under `configs/`
- Helper and validation scripts under `scripts/`
- Asset, license, and third-party notice documentation

## What Is Not Included

- Model weights and tokenizer files
- Original benchmark datasets (must be obtained from their sources)


## License and Third-Party Assets

The MIT license in `LICENSE` applies only to ACE-Compression-authored supplementary scripts and documentation. Third-party models, benchmarks, datasets, and software remain under their original licenses or terms, summarized in `ASSETS.md` and `THIRD_PARTY_NOTICES.md`.

This package does not redistribute model weights or original benchmark datasets. Processed evaluation outputs are included only for research verification of the submitted paper and do not relicense third-party assets.
