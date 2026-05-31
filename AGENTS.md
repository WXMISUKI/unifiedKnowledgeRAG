# Project Agent Instructions

请作为高级开发工程师，用中文协作，并以最佳实践和企业级可维护性为基础推进本项目。

## 长期开发方向

- 按照 `docs/roadmap/lightweight_provider_roadmap.md` 继续完善当前项目。
- 每一步都应跟随已确认的设计方案和 OpenSpec 规格，不偏离路线图。
- 目标是快速、轻量、可用地完善当前 RAG 和知识图谱能力，遵循敏捷开发思维。
- 不要陷入局部无限优化；优先交付小而完整、可验证、可归档的切片。
- 本项目主要作为轻量外部知识提供方，提供检索增强、知识证据、引用、诊断和集成所需数据。
- 不要把调用者或核心运行项目应该承担的职责塞进本项目，例如复杂权限审计、审批流、用户身份策略、最终回答策略、平台控制面治理等。
- 过多的权限审计不必写入本项目；后续应由调用者或核心运行项目的执行接口统一处理。
- 保持整体轻量，避免引入过多要素导致 provider 变成重型平台。

## 工作节奏

- 继续使用“规格 -> 实现 -> 归档”的节奏推进。
- 涉及需求确认或能力边界变化时，先创建或更新 OpenSpec change。
- 每个 OpenSpec change 必须说明推进的 roadmap phase，以及明确非目标。
- 实现时保持最小改动，完成一项任务及时更新 `tasks.md`。
- 验证以聚焦测试和 `openspec validate --all --strict` 为主；除非改动重要，不做过重验证。
- 完成后及时归档 OpenSpec change，保持 active change 列表清爽。

## 项目阅读与排障

- 在阅读、了解和追踪项目结构时，优先使用 CodeGraph 快速获取符号关系、调用链和影响范围。
- 如果项目尚未初始化 CodeGraph，先执行初始化（例如 `codegraph init -i`）再继续分析。
- 对纯文本匹配场景再使用 `rg`，避免仅靠全文检索替代结构化分析。

## 进度台账维护

- 持续维护 `docs/progress/provider-improvement-tracker.md`。
- 每次完成一个切片后，及时更新“已完成 / 未完成 / 下一步”。
- 台账只记录轻量 provider 范围内的工作，不把调用方控制面职责记入本项目待办。

## 边界提醒

- 文档 RAG、混合检索、rerank、LLM answer composition、GraphRAG 执行都应分别作为 evidence-backed gates 推进。
- GraphRAG 仍应保持 use-case-driven，不应默认引入 Neo4j、实体抽取、ontology workflow 或图查询执行。
- source binding 相关能力只提供证据和建议动作，不创建 source-to-agent binding，不承接绑定策略。
- provider 可暴露健康、预检、manifest、capability、handoff、source binding、smoke evidence，但注册、心跳治理、审计策略和最终业务决策属于调用方。
