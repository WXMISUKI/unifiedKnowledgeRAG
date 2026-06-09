## Why

我们已经完成了：

- source evaluation pack catalog
- source evaluation pack onboarding 模板
- 一个新增真实 source 的模板链路验证

但如果要更有把握地证明这套方法对“不同类型 source”同样成立，就还需要第三类 source 的验证证据。否则我们仍然可能停留在“这套模板对当前少数文档族可用”的阶段。

当前仓库没有现成足够不同的新 source 候选，因此本次 change 选择新增一个轻量、规则型、markdown 形式的新 source，用来验证：

- onboarding 模板链路是否对规则/制度类 source 同样成立
- provider 只需要最小可见性补充即可承载它的 baseline
- 不需要引入新 parser、GraphRAG 或高级 retrieval strategy

## What Changes

- 新增一个轻量规则型 source：`invoice_policy_faq`
- 为该 source 提供最小 provider 可见性
- 用 onboarding helper 为该 source 生成模板，并填充一份最小真实 baseline fixture
- 导出该 source 的 baseline 验证报告
- 保持 runtime defaults 和高级检索策略完全不变

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `local-business-rag-golden-cases`: 进一步证明 onboarding 模板链路可以扩展到第三类不同 source，而不需要围绕现有 source 做局部 hardening。

## Impact

- Affected code:
  - `app/services/source_catalog.py`
  - `app/services/source_document_manifest.py`
  - `app/services/document_retriever.py`
- Affected scripts:
  - `scripts/export_invoice_policy_onboarding_validation.py`
- Affected tests:
  - `tests/test_invoice_policy_onboarding_validation.py`
- Affected artifacts:
  - `app/data/sources/invoice_policy_faq.md`
  - `docs/local-run/business-rag-golden-cases/onboarding/invoice_policy_faq/baseline-pack.fixture.json`
  - `docs/local-run/business-rag-golden-cases/onboarding/invoice_policy_faq/invoice-policy-local-business-rag-golden-cases.json`
  - `docs/local-run/business-rag-golden-cases/onboarding/invoice_policy_faq/invoice-policy-local-business-rag-golden-cases.md`
