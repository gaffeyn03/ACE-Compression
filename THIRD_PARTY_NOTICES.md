# Third-party notices

This repository includes upstream and adapted research source. The root MIT license does not replace upstream licenses, dataset terms or model licenses. Preserve their notices when redistributing source or adaptations. `ASSETS.md` records the inherited source/terms inventory; exact historical upstream revisions were not logged.

| Included component | Upstream source | Included license file |
|---|---|---|
| lm-evaluation-harness | https://github.com/EleutherAI/lm-evaluation-harness | `paper_benchmarks/00_shared/lm-evaluation-harness/LICENSE.md` |
| HumanEval | https://github.com/openai/human-eval | `paper_benchmarks/03_human-eval/LICENSE` |
| ToMBench | https://github.com/zhchen18/ToMBench | `paper_benchmarks/07_ToM-Bench/LICENSE` |
| EQ-Bench | https://github.com/EQ-bench/EQ-Bench | `paper_benchmarks/08_eq-bench/LICENSE` |
| CharacterEval | https://github.com/morecry/CharacterEval | `paper_benchmarks/09_CharacterEval/LICENSE` and `upstream_official/LICENSE` |
| PsychoBench | https://github.com/CUHK-ARISE/PsychoBench | `paper_benchmarks/10_PsychoBench/LICENSE` (GPL-3.0) |
| TransformerCompression / SliceGPT | Source and attribution in the included upstream README | `compression/pruning_scripts/TransformerCompression/LICENSE` |

Upstream citations, copyright headers, task definitions, prompt templates, and applicable license texts remain with their source. Packaging changes include local path corrections and removal of runtime/data assets; included copies are not claimed to be unmodified or pinned upstream releases.

Other benchmark wrappers depend on externally obtained IFEval, GSM8K, TruthfulQA, C-Eval and RoleEval assets. Model weights, standalone benchmark datasets and raw generated answers are not included. Dataset/checkpoint access, commercial-use restrictions and any additional model/provider terms must be checked at the original source before running or redistributing those assets. In particular, benchmark code licenses do not automatically license the datasets or reward-model weights.
