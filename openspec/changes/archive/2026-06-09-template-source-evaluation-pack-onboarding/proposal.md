## Why

当前 provider 已经具备：

- baseline pack
- failed-question pack
- confirmation pack
- source evaluation pack catalog

但这些能力还主要服务于当前已落地的 source。对于一个通用 RAG provider，下一阶段更需要的是把“如何让一个新 source 进入评估闭环”模板化，而不是继续围绕已有 source 的个别 review case 做专项优化。

结合 `RAG_Techniques` 的经验，企业级复用更看重：

- baseline 先行
- golden questions 和 failed questions 可复用
- 策略候选之前先有统一 evaluation gate

所以这一切片的重点，是提供一个统一 onboarding helper，让未来任意 source 都能低成本生成 baseline / failed / confirmation 三类模板，并进入 catalog 所依赖的标准命名与路径约定。

## What Changes

- 新增 source evaluation pack onboarding helper。
- 为新 source 统一生成：
  - baseline fixture template
  - failed-question fixture template
  - confirmation fixture template
  - onboarding manifest/report
- 把三类 pack 的命名规则、目录规则和最小字段约束固化下来。
- 保持现有运行时检索行为、catalog 逻辑和独立 pack 逻辑不变。

## Capabilities

### New Capabilities

- `local-business-rag-golden-cases`: provider 可以为未来 source 生成标准化的 evaluation-pack onboarding 模板，而不需要每次手工复制现有 fixture。

### Modified Capabilities

- None.

## Impact

- Affected code: `app/services/source_evaluation_pack_onboarding.py`
- Affected scripts: `scripts/export_source_evaluation_pack_onboarding.py`
- Affected tests: `tests/test_source_evaluation_pack_onboarding.py`
- Affected artifacts:
  - `docs/local-run/business-rag-golden-cases/onboarding/<source_id>/baseline-pack.fixture.template.json`
  - `docs/local-run/business-rag-golden-cases/onboarding/<source_id>/failed-question-pack.fixture.template.json`
  - `docs/local-run/business-rag-golden-cases/onboarding/<source_id>/confirmation-pack.fixture.template.json`
  - `docs/local-run/business-rag-golden-cases/onboarding/<source_id>/source-evaluation-pack-onboarding.json`
  - `docs/local-run/business-rag-golden-cases/onboarding/<source_id>/source-evaluation-pack-onboarding.md`
