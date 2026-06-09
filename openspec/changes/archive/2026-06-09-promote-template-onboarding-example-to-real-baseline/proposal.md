## Why

当前 `source_template_example` 仍然停留在 `template_only` 状态。为了把通用 onboarding 路径从“有模板”推进到“有可复制的最小真实示例”，现在最合适的下一步是把这个模板样本补成一个真实但极小的 baseline 示例，而不是继续打磨 catalog 或过早进入高级 RAG 策略。

## What Changes

- 将 `source_template_example` 从模板态提升为真实最小 baseline 示例。
- 为该示例 source 提供最小 provider 可见性和最小 markdown 文档内容。
- 生成真实 baseline fixture 和 validation report。
- 刷新 source onboarding catalog 与 source evaluation pack catalog，使其反映该样本不再是 `template_only`。

## Capabilities

### New Capabilities
- `real-template-onboarding-example`: 将模板 onboarding 示例提升为真实最小 baseline 示例

### Modified Capabilities
- `local-business-rag-golden-cases`: 增加模板 onboarding 示例可以通过最小真实 baseline 验证的规格要求，但不改变 aggregate baseline 或 runtime strategy semantics

## Impact

- Affected code:
  - `app/data/sources/source_template_example.md`
  - `app/services/source_catalog.py`
  - `app/services/source_package.py`
  - `app/services/source_document_manifest.py`
  - `app/services/document_retriever.py`
- Affected scripts:
  - `scripts/export_source_template_onboarding_validation.py`
- Affected tests:
  - `tests/test_source_template_onboarding_validation.py`
- Affected artifacts:
  - `docs/local-run/business-rag-golden-cases/onboarding/source_template_example/baseline-pack.fixture.json`
  - `docs/local-run/business-rag-golden-cases/onboarding/source_template_example/source-template-local-business-rag-golden-cases.json`
  - `docs/local-run/business-rag-golden-cases/onboarding/source-template-local-business-rag-golden-cases.md`
