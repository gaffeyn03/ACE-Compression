#!/usr/bin/env python3
"""Check packaged source paths without importing model backends or running models."""
from __future__ import annotations
import ast
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
HARNESS = Path("paper_benchmarks/00_shared/lm-evaluation-harness")
BACKEND_FILES = (
    "__init__.py", "anthropic_llms.py", "api_models.py", "dummy.py", "gguf.py",
    "hf_audiolm.py", "hf_steered.py", "hf_vlms.py", "huggingface.py", "ibm_watsonx_ai.py",
    "llama_cpp_direct.py", "mamba_lm.py", "nemo_lm.py", "neuron_optimum.py",
    "openai_completions.py", "optimum_ipex.py", "optimum_lm.py", "sglang_causallms.py",
    "sglang_generate_API.py", "textsynth.py", "utils.py", "utils_hf.py",
    "vllm_causallms.py", "vllm_vlms.py",
)
BENCHMARKS = (
    "01_IFEval", "02_gsm8k", "03_human-eval", "04_TruthfulQA", "05_C-eval",
    "06_roleeval", "07_ToM-Bench", "08_eq-bench", "09_CharacterEval", "10_PsychoBench",
)
GENERATORS = (
    "llama3.1-8b/llama31_8b_vllm_generator.py",
    "qwen2.5-7b/qwen25_7b_vllm_generator.py",
)
STALE_BENCHMARK_PATH = re.compile(
    r"paper_benchmarks/\d\d_[^/\s\"']+/(?:benchmark|launchers)(?=[/\"'\s]|$)"
)


def check_backends(root: Path) -> int:
    folder = root / HARNESS / "lm_eval/models"
    for name in BACKEND_FILES:
        if not (folder / name).is_file():
            raise ValueError(f"Missing model-backend SOURCE (not weights): {folder / name}")
    tree = ast.parse((folder / "__init__.py").read_text(encoding="utf-8"))
    mapping = next(ast.literal_eval(node.value) for node in tree.body
                   if isinstance(node, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == "MODEL_MAPPING" for t in node.targets))
    for alias, target in mapping.items():
        module, class_name = target.split(":")
        path = root / HARNESS / (module.replace(".", "/") + ".py")
        if not path.is_file():
            raise ValueError(f"Missing lazy backend {alias}: {path}")
        definitions = ast.parse(path.read_text(encoding="utf-8"))
        if not any(isinstance(n, ast.ClassDef) and n.name == class_name for n in definitions.body):
            raise ValueError(f"Missing backend class: {target}")
    return len(mapping)


def check_generator(path: Path) -> None:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    defaults, calls = [], []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "chat":
            args = node.args.args[-len(node.args.defaults):]
            defaults.extend(value for arg, value in zip(args, node.args.defaults) if arg.arg == "max_tokens")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "chat":
            calls.extend(kw.value for kw in node.keywords if kw.arg == "max_tokens")
    if not defaults or not calls or any(not isinstance(v, ast.Constant) or v.value != 1024 for v in [*defaults, *calls]):
        raise ValueError(f"PsychoBench original max_tokens=1024 changed: {path}")


def check_layout(root: Path = ROOT) -> dict[str, int]:
    mapping_count = check_backends(root)
    for name in BENCHMARKS:
        if not (root / "paper_benchmarks" / name).is_dir():
            raise ValueError(f"Missing benchmark directory: {name}")
    for name in GENERATORS:
        check_generator(root / "paper_benchmarks/10_PsychoBench" / name)
    required = ["COMPUTE_ESTIMATE.md", "docs/SUBMISSION_NOTES.md", "tables/README.md",
                "results/processed/README.md", "paper_benchmarks/09_CharacterEval/compute_score.py",
                "paper_benchmarks/08_eq-bench/data/translate_openai.py",
                "paper_benchmarks/08_eq-bench/data/translate_wmt.py"]
    for name in required:
        if not (root / name).is_file():
            raise ValueError(f"Missing original release file: {name}")
    model_tests = list((root / HARNESS / "tests/models").glob("*.py"))
    if len(model_tests) < 9:
        raise ValueError("Missing upstream model-backend tests")
    checked = 0
    for base in [root / "scripts/report_sync", *[root / "paper_benchmarks" / n for n in BENCHMARKS]]:
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix not in {".py", ".sh", ".cfg", ".yaml"}:
                continue
            text = path.read_text(encoding="utf-8-sig")
            if STALE_BENCHMARK_PATH.search(text):
                raise ValueError(f"Obsolete benchmark/launchers path: {path}")
            if path.parent == root / "scripts/report_sync":
                if 'bcmk_v2' in text or 'ROOT / "benchmarks"' in text or '/ "benchmark"' in text or '/ "launchers"' in text:
                    raise ValueError(f"Obsolete report path: {path}")
                for node in ast.walk(ast.parse(text)):
                    if isinstance(node, ast.Constant) and isinstance(node.value, str):
                        value = node.value
                        if value.endswith(".py") and value.startswith(("paper_benchmarks/", "scripts/")):
                            if not (root / value).is_file():
                                raise ValueError(f"Missing helper entrypoint in {path}: {value}")
            checked += 1
    if (root / "paper_benchmarks/09_CharacterEval/upstream_official").exists():
        raise ValueError("Duplicate CharacterEval upstream tree is outside the original layout")
    return {"model_backend_files": len(BACKEND_FILES), "lazy_backend_mappings": mapping_count,
            "model_backend_tests": len(model_tests), "benchmark_source_paths_checked": checked}


def main() -> int:
    try:
        counts = check_layout()
    except (OSError, ValueError, StopIteration) as error:
        print(f"FAIL: {error}")
        return 1
    for name, count in counts.items():
        print(f"OK {name}: {count}")
    print("PASS: packaged source layout (no GPU/dependency execution)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
