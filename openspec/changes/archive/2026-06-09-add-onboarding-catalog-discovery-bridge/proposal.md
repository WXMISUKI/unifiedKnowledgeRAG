## Why

我们已经证明 source onboarding 模板链路可以在多个不同类型的真实 source 上跑通，但当前这些结果仍分散在各自目录里，缺少一个统一、轻量、证据优先的 discovery 入口。现在补上这层桥接，能降低后续新 source 的接入和复查成本，同时避免过早进入 source-specific hardening 或高级 RAG 策略优化。

## What Changes

- 新增一个轻量的 source onboarding catalog/discovery 视图，用于扫描现有 onboarding 目录并汇总每个 source 的 onboarding 证据状态。
- 为每个 source 暴露模板、真实 baseline fixture、validation report、validation decision 和建议下一步等统一字段。
- 提供单独的 JSON/Markdown 导出产物，作为 evidence-only 发现入口。
- 保持与现有 source evaluation pack catalog 分离，不自动注册 source、不自动并入 aggregate baseline。

## Capabilities

### New Capabilities
- `source-onboarding-catalog`: 统一暴露 source onboarding 模板和真实验证产物的轻量 discovery 视图

### Modified Capabilities
- `local-business-rag-golden-cases`: 增加 source onboarding discovery bridge 的规格要求，但不改变现有 baseline / failed-pack / confirmation 评估语义

## Impact

- Affected code:
  - `app/services/source_onboarding_catalog.py`
- Affected scripts:
  - `scripts/export_source_onboarding_catalog.py`
- Affected tests:
  - `tests/test_source_onboarding_catalog.py`
- Affected artifacts:
  - `docs/local-run/business-rag-golden-cases/source-onboarding-catalog.json`
  - `docs/local-run/business-rag-golden-cases/source-onboarding-catalog.md`
