# Public release alignment

This release follows the actual original anonymous package, retaining its benchmark code, model backends, upstream tests and examples, configurations, serving/pruning templates, compute estimate and thirteen processed tables. It does not add later supplemental experiments or their results.

Changes relative to that package are limited to release maintenance and path corrections:

- Remove obsolete `benchmark/` and `launchers/` components to match the existing flattened tree.
- Resolve report utilities from the repository root, fix their local helper paths, and place newly consolidated reports in `results/generated/` instead of overwriting the published tables.
- Correct the Llama70B RoleEval directory alias and seven upstream lazy-import targets to the class names actually defined in the bundled backend modules. These are entrypoint fixes, not changes to model implementations or evaluation settings.
- Keep CharacterEval's original root-level upstream code and `data/` convention rather than a duplicate `upstream_official/` tree.
- Retain the anonymous package's `max_tokens=1024` defaults and explicit calls in the Llama3.1-8B/Qwen2.5-7B PsychoBench generators.
- Add source-layout, original-result-hash and offline regression checks, a file manifest, GitHub CI and public-release documentation. Correct outdated documentation without claiming new measurements.

The model-backend directory `lm_eval/models/` and upstream `tests/models/` are software source, not model checkpoints. They must not be removed by weight-exclusion rules. All thirteen original CSVs are unchanged byte-for-byte. Offline checks do not replace GPU evaluation or audit historical raw responses.
