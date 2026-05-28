## Context

Benchmark metrics currently exist only as Python dataclasses returned from tests or service calls. That is not enough for decision review. We need stable artifacts that can be attached to future OpenSpec changes when comparing retrieval adapters.

## Goals / Non-Goals

**Goals:**

- Export benchmark reports to JSON.
- Export benchmark reports to Markdown.
- Keep output deterministic enough for review.
- Include aggregate metrics, category metrics, and case-level evidence.

**Non-Goals:**

- No CLI command in this slice.
- No API endpoint.
- No chart rendering.
- No external reporting dependency.

## Decisions

1. Keep export helpers in the benchmark service.

   The benchmark service already owns the report dataclasses and can serialize them without another module.

2. Use dataclass serialization for JSON.

   This keeps the JSON shape close to the in-memory report shape and easy to compare.

3. Use a compact Markdown table.

   Markdown is enough for review in docs, PRs, and OpenSpec changes without adding rendering dependencies.

## Risks / Trade-offs

- Markdown tables can become wide as metrics grow -> acceptable for the current metric set.
- No CLI means users need Python/test entrypoints -> fine for this slice; CLI can be added later.
- JSON timestamps are not included yet -> reports are deterministic; run metadata can come later.

## Migration Plan

1. Add report serialization helpers.
2. Add file export helpers.
3. Add tests.
4. Update docs.
5. Validate and archive.
