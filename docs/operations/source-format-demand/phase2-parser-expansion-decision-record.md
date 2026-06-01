# Phase 2 Parser Expansion Decision Record

- Decision ID: `phase2-parser-expansion-decision-record-v1`
- Decision Date: `2026-06-01`
- Scope: `Phase 2 parser expansion readiness review`
- Decision: `keep_markdown_baseline`
- Status: `approved-for-current-slice`

## Current Baseline Snapshot

| Item | Current Value |
|---|---|
| Runtime parser baseline | `markdown` |
| Deferred parser families | `pdf`, `word`, `excel`, `ocr`, `table-structure` |
| Source-format demand readiness | `ready` |
| Unsupported-format negative-control smoke | `ready` |

## Evidence Basis

| Evidence | Current Status | Key Signal |
|---|---|---|
| `phase2-parser-expansion-demand-contract` | `ready` | expansion remains evidence-gated |
| `phase2-source-format-demand-readiness` | `ready` | `non_markdown_sources=0`, `unsupported_documents=0`, `open_gate_count=0` |
| `phase2-unsupported-format-negative-control-smoke` | `ready` | `passed_checks=5/5` |

## Open Gates For Future Parser Expansion

1. 出现真实客户语料的非 Markdown 格式需求与稳定分布证据。
2. 补齐候选 parser 的 FP/FN 复核与跨场景质量评估。
3. 补齐 parser 侧延迟/资源与部署所有权评估。
4. 通过单独的 parser 扩展 OpenSpec change 进入实现，而不是在当前评审切片直接切换默认。

## Decision Outcome

本轮 Phase 2 结论是维持 Markdown 作为运行时轻量基线，不推进 PDF/Word/Excel/OCR/table 的默认 parser 扩展。当前切片目标已经达到：我们补齐了 contract、readiness、smoke、decision record，使 parser 扩展决策具备可追踪、可复核、可归档的证据链。

## Boundary Reminder

This record is documentation-only governance evidence. It does not enable parser runtime changes, does not execute ingestion/reindex actions, and does not shift control-plane ownership into this provider.
