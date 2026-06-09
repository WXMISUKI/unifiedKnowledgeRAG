## Context

当前 post-closure 的推进顺序已经明确，但阶段2还偏“概念正确”，不够“执行友好”。

如果没有一份 task pack，调用方在开始 trial 时仍然容易出现：

- 不确定 trial 最小目标是什么
- 不确定哪些前置项只是 review，哪些是真 blocker
- 不确定应回传哪些结果
- 不确定 outcome 之外还要记录什么辅助证据

因此最合适的下一步，是把阶段2整理成一份任务包。

## Goals / Non-Goals

**Goals**

- 明确阶段2的前置检查项。
- 明确调用方 trial 最小执行目标。
- 明确应保留的输出与回传材料。
- 让 provider 侧后续消费反馈更顺滑。

**Non-Goals**

- 不在本仓库执行调用方代码。
- 不新增 provider runtime 能力。
- 不编写跨仓库自动化。
- 不展开高级 RAG 策略工作。

## Decisions

- task pack 按“before / during / after”结构编写：
  - Before trial
  - During trial
  - After trial

- 输出里同时保留：
  - 必需 outcome JSON
  - 建议的辅助记录项

- 只把 provider 侧真正关心的信息列为 required，避免变成重型试运行协议。

## Risks / Trade-offs

- 如果写太细，会越界到调用方设计 -> 保持为 provider 视角下的 trial task pack。
- 如果写太粗，执行价值不足 -> 用 checklist、expected outputs、done criteria 保证实用性。
