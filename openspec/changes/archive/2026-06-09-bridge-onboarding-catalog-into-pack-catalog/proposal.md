## Why

我们已经有 source evaluation pack catalog，也已经有 source onboarding catalog，但两者仍然是分离查看的。现在补一层很小的 evidence-only 桥接，可以让 pack-level 发现入口直接看到 onboarding 成熟度摘要，降低后续 source 接入和复查成本，同时不引入新的平台化状态机。

## What Changes

- 让 `source-evaluation-pack-catalog` 在保留原 pack 语义的前提下，读取并展示 `source-onboarding-catalog` 的轻量摘要。
- 在 pack catalog 中补充 onboarding source 总数、ready/template-only 计数、ready source 列表和 onboarding catalog 是否存在等字段。
- 在 pack catalog Markdown 中增加 onboarding summary section。
- 保持 pack catalog 原有 `decision` 和 pack-level recommended actions 逻辑不被 onboarding 状态劫持。

## Capabilities

### New Capabilities
- `pack-catalog-onboarding-bridge`: 将 source onboarding catalog 的摘要信号轻量映射进 source evaluation pack catalog

### Modified Capabilities
- `local-business-rag-golden-cases`: 增加 pack catalog 可以吸收 onboarding 摘要信号的规格要求，但不改变现有评估 pack 的 decision 规则

## Impact

- Affected code:
  - `app/services/source_evaluation_pack_catalog.py`
- Affected scripts:
  - `scripts/export_source_evaluation_pack_catalog.py`
- Affected tests:
  - `tests/test_source_evaluation_pack_catalog.py`
- Affected artifacts:
  - `docs/local-run/business-rag-golden-cases/source-evaluation-pack-catalog.json`
  - `docs/local-run/business-rag-golden-cases/source-evaluation-pack-catalog.md`
