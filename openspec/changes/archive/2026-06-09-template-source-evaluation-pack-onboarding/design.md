## Context

我们已经有了 source evaluation 的核心执行能力，但“未来新 source 如何接入”还没有被标准化。当前如果要给一个新 source 建 baseline / failed / confirmation pack，仍然需要参考现有 fixture 和脚本手工拼接，这会带来几个问题：

- 接入成本偏高
- 命名和目录容易漂移
- 不利于通用 provider 的长期维护

`RAG_Techniques` 的经验强调，真正值得沉淀的是一套可重复的 evaluation gate 体系，而不是不断围绕单个具体业务问题做局部修补。

因此，这一切片优先解决“模板化接入”，而不是“自动做更聪明的评估”。

## Goals / Non-Goals

**Goals:**

- 给任意新 source 提供标准 evaluation-pack 模板。
- 固化 pack 目录、文件名和最小字段集合。
- 降低后续 baseline / failed / confirmation pack 的接入成本。
- 保持 provider 边界轻量，只做模板和约定，不做策略推断。

**Non-Goals:**

- 不自动生成真实业务问题。
- 不自动判定 failure class。
- 不改 catalog 为完全动态发现。
- 不改 retrieve/answer runtime behavior。
- 不引入 query rewrite、rerank、hybrid retrieval、GraphRAG。

## Decisions

### 1. 先做模板生成，不做全自动 pack 注册

这一切片先输出统一模板和 onboarding manifest，而不是把 catalog 立即改成对所有未来 source 自动发现。

原因：

- 更小、更稳
- 保持现有 catalog 兼容
- 让团队先有统一模板，再决定是否需要更重的自动注册机制

### 2. 模板输出聚焦最小可编辑结构

每个 pack 模板只提供最小字段和一条示例 case。

原因：

- 避免一开始输出过多伪精细内容
- 保留人工填充真实业务问题的空间
- 更符合“通用 provider”而不是“伪自动业务建模”

### 3. onboarding report 只做脚手架说明

onboarding report 不执行评估，只说明：

- 生成了哪些模板
- 每个模板用于什么
- 下一步应该如何填充和导出

原因：

- 这一步的职责是接入模板化
- 不是重新执行 baseline

## Output Shape

对于给定 `source_id`，helper 应生成：

- `baseline-pack.fixture.template.json`
- `failed-question-pack.fixture.template.json`
- `confirmation-pack.fixture.template.json`
- `source-evaluation-pack-onboarding.json`
- `source-evaluation-pack-onboarding.md`

manifest/report 中至少包含：

- `source_id`
- `output_dir`
- `generated_templates`
- `recommended_next_steps`
- `non_goals`

## Risks / Trade-offs

- [模板过于抽象，团队仍需手工补内容] -> 这是有意为之，当前目标是标准化接入而不是自动生成业务问题。
- [catalog 还不是完全自动接入] -> 当前切片先解决模板化和约定，自动注册可以作为后续小切片。
- [示例 case 被误当成真实评估数据] -> 文件名中明确 `template`，并在 report 中说明其脚手架性质。
