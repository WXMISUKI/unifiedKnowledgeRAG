## Why

当前我们已经把 customer-like 误召回/漏召回样例纳入基线，但评审时仍需人工从完整 benchmark 明细里二次识别 FP/FN。为了保持敏捷与轻量，本次只增加一个本地导出视图，帮助快速审阅风险，不修改任何运行时默认行为。

## What Changes

- 新增 Phase 3 FP/FN 评审导出：
  - 输入现有基线 benchmark JSON（默认 `fixture-chinese-seed-baseline.json`）
  - 输出误召回（false-positive）与漏召回（false-negative）汇总及 case 列表
- 新增对应 JSON/Markdown 导出能力和轻量脚本入口。
- 保持 evaluation-only，不改变检索策略、阈值和 provider API。

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `retrieval-benchmark-harness`: 新增基于现有 benchmark 证据的 FP/FN 评审导出能力。
- `provider-roadmap`: 记录为 Phase 3 证据可审阅性增强，不触发运行时提升。

## Impact

- Affected code: `app/services/phase3_fp_fn_review.py` (new), `scripts/export_phase3_fp_fn_review.py` (new)
- Affected tests: `tests/test_phase3_fp_fn_review.py` (new)
- No runtime default changes, no public API changes
