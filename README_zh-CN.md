# ACE-Compression

[English](README.md) | 简体中文

论文 **ACE-Compression: An Ability-Centric Evaluation of Compressed Large Language Models** 的代码与评测结果。

ACE-Compression 从能力维度评估量化、剪枝对大语言模型的影响。项目将十个评测基准组织为四类能力，提供各模型的评测脚本、压缩工具、模型服务模板和整理后的评测结果。

## 评测范围

| 能力维度 | 评测基准 |
|---|---|
| 过程推理 | IFEval、GSM8K、HumanEval |
| 知识基础 | TruthfulQA、C-Eval、RoleEval |
| 社会认知 | ToMBench、EQ-Bench |
| 人格一致性 | CharacterEval、PsychoBench |

模型包括 Qwen2.5-7B/14B/32B、Llama3.1-8B/70B 和 DeepSeek-V2-Lite-16B。评测设置涵盖 FP16、bitsandbytes 4-bit、AWQ、GPTQ-INT4/INT8、2:4 结构化稀疏、非结构化稀疏及部分模型的裁剪变体。不同模型采用的设置有所区别，详见[模型配置](configs/models.yaml)和[压缩设置](configs/compression_methods.yaml)。

## 仓库结构

```text
paper_benchmarks/             十个基准的评测流程及共享 lm-eval 源码
compression/pruning_scripts/  各模型的剪枝脚本与压缩工具
serving/                      各模型的 vLLM 服务启动模板
configs/                      模型、压缩方法与评测设置
results/processed/            十三份评测结果 CSV
scripts/report_sync/          原始输出汇总与报告工具
scripts/prepare_results/      结果完整性与源码路径检查
tests/                        离线回归测试
docs/                         复现、结果解读与检查范围说明
```

## 环境准备

使用 Python 3.10 或更新版本。GPU 评测需要相互兼容的 NVIDIA/CUDA、PyTorch 和 vLLM 环境。`requirements.txt` 列出带有版本约束的依赖，并非经过完整验证的锁定环境；剪枝、推理和奖励模型打分可能需要分别配置环境。

```bash
git clone https://github.com/gaffeyn03/ACE-Compression.git
cd ACE-Compression
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e ./paper_benchmarks/00_shared/lm-evaluation-harness
```

使用剪枝工具时，在兼容的环境中另行安装相关依赖：

```bash
pip install llmcompressor
pip install -e './compression/pruning_scripts/TransformerCompression[experiment]'
```

模型权重、分词器文件、完整评测数据集和奖励模型权重需要自行获取。来源与使用条款见 [ASSETS.md](ASSETS.md)。

## 运行评测

1. 获取模型和评测输入，按照 [REPRODUCIBILITY.md](REPRODUCIBILITY.md) 确认数据目录及环境要求。
2. 在所选模型脚本中配置权重路径、GPU 编号、服务端口和运行环境。
3. 运行 `paper_benchmarks/` 中对应的评测流程。需要 OpenAI 兼容接口时，先使用匹配的 `serving/` 模板启动 vLLM 服务。
4. 使用 `scripts/report_sync/` 汇总匹配的原始输出。新生成的综合结果写入 `results/generated/`，不会覆盖仓库内提供的结果 CSV。

IFEval、GSM8K、HumanEval、TruthfulQA 和 C-Eval 使用共享评测框架；RoleEval 使用专门的模型运行脚本；ToMBench、EQ-Bench、CharacterEval 和 PsychoBench 包含各自的 API 调用或评测流程。具体入口与执行顺序见 [WORKFLOW.md](WORKFLOW.md)。

**HumanEval 会执行模型生成的代码。请在一次性的隔离环境中运行，不要让该环境接触凭据或重要文件。**

## 结果说明

`results/processed/` 包含覆盖十个基准的十三份 CSV。ToMBench 分别提供任务、能力和子能力汇总；PsychoBench 提供数值画像与 16P 结果。

- `Psychobench.csv` 使用两行表头，应按列位置读取，或使用 `pandas.read_csv(path, header=[0, 1])`。
- `Psychobench_16P.csv` 中同一模型可以有多个性格类型结果，不能仅按模型名去重。
- 缺失值和 `FAILED` 不代表零分；心理测量画像也不能统一解释为“越高越好”的性能指标。

比较分数前，请阅读[结果定义与限制](docs/RESULTS.md)。仓库不提供原始生成回答和运行日志。

## 离线检查

以下命令仅依赖 Python 标准库，不需要模型权重、GPU 或网络：

```bash
python3 scripts/prepare_results/check_processed_results.py
python3 scripts/prepare_results/check_source_layout.py
python3 scripts/prepare_results/validate_release.py
python3 -m unittest discover -s tests -v
```

检查内容包括表格结构、结果哈希、必要源码、辅助脚本路径及回归测试，不会运行模型推理。主动修改源码后，可使用 `validate_release.py --skip-manifest` 跳过打包快照的文件哈希检查。详见[检查范围](docs/VALIDATION.md)。

## 相关文档

- [评测工作流程](WORKFLOW.md)
- [复现说明与外部输入](REPRODUCIBILITY.md)
- [算力估计及假设](COMPUTE_ESTIMATE.md)
- [外部资源与许可](ASSETS.md)

## 许可

仓库根目录的 [MIT 许可](LICENSE) 适用于 ACE-Compression 作者编写的脚本和文档。第三方源码保留其各自许可，其中 PsychoBench 使用 GPL-3.0。数据集和模型的使用条款独立适用，详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) 和 [ASSETS.md](ASSETS.md)。
