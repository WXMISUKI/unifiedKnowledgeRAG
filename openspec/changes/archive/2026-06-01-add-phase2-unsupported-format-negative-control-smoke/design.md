## Design Overview

This change adds a small smoke layer over the Phase 2 readiness export:

- Input: `docs/operations/source-format-demand/phase2-source-format-demand-readiness.json`
- Output: `docs/smoke/source-format-demand/phase2-unsupported-format-negative-control-smoke.{json,md}`

The smoke checks:

1. readiness report presence
2. markdown positive control (`parser_ready_documents > 0`)
3. unsupported-format negative control (`unsupported_documents == 0`)
4. non-markdown source negative control (`non_markdown_sources == 0`)
5. decision alignment (`keep_markdown_baseline` + no demand signal)

## Status Rules

- `blocked`: readiness input missing.
- `review`: readiness exists but one or more controls fail.
- `ready`: all controls pass.

## Boundaries

- No parser runtime changes.
- No ingestion/reindex execution.
- No retrieval/default promotion.
- No control-plane ownership changes.
