## Why

当前 Phase 3 基线已覆盖通用客户化问题，但“误召回（false-positive）/漏召回（false-negative）”的客户化评审样例仍偏少。为保持敏捷且轻量，本次仅扩充基准样例并刷新本地证据，不改运行时默认策略。

## What Changes

- 在 `tests/fixtures/retrieval_benchmark_cases.json` 增加最小数量的客户化评审样例：
  - 至少一个 false-negative 风险样例（应命中）
  - 至少一个 false-positive 风险样例（应为空）
- 同步更新相关检索基准测试断言。
- 刷新中文 seed 基线证据（JSON/Markdown），保持证据与基准夹具一致。

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `retrieval-benchmark-harness`: customer-like 基线样例覆盖更完整的误召回/漏召回评审场景。
- `provider-roadmap`: 记录为 Phase 3 证据增强（evaluation-only），不触发运行时默认提升。

## Impact

- Affected fixtures: `tests/fixtures/retrieval_benchmark_cases.json`
- Affected tests: `tests/test_retrieval_benchmark.py`
- Affected evidence: `docs/benchmark/chinese-seed/retrieval-candidates/fixture-chinese-seed-baseline.{json,md}`
- No API contract changes, no runtime default changes
