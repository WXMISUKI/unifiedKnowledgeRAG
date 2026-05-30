## Context

`source-document-identifier-coverage-v1` currently proves that multi-chunk aggregation can recover one split-chunk positive case. The same grouping rule can also be too permissive: a source document may contain two identifiers in separate paragraphs even though the user asks for an unsupported relationship between them.

This change adds the next evidence gate for Phase 3 retrieval-quality promotion. It keeps the implementation local and reversible by extending fixtures and reports instead of changing runtime retrieval.

## Goals / Non-Goals

**Goals:**

- Add expected-empty same-document negative controls for multi-chunk aggregation.
- Ensure exported aggregation evidence reports positive recovery and negative-control empty handling in one report.
- Preserve raw citation diagnostics so reviewers can understand why a case passed or failed.
- Keep the benchmark command stable for future additional negative controls.

**Non-Goals:**

- Do not change runtime retrieval behavior, answer behavior, provider capabilities, or HTTP contracts.
- Do not add a reranker, parent-document store, graph relation check, or LLM evidence grader.
- Do not treat passing local negative controls as production approval.

## Decisions

1. Use a separate expected-empty fixture.

   A dedicated fixture keeps split-chunk positives and same-document negatives independently reviewable. The export function already accepts `empty_cases_path`, so the implementation stays small.

2. Model the first negative control as an unsupported relationship, not an unknown source.

   The point is to test over-broad grouping inside a real source document. A missing-source or no-hit case would not exercise the aggregation risk.

3. Let the current aggregation candidate fail if it over-broadly groups evidence.

   If the current candidate returns evidence for the negative control, the report should show that failure honestly. The goal is evidence, not making the metric look good.

## Risks / Trade-offs

- [Risk] The new negative control may expose that the candidate is not promotion-ready. → Mitigation: keep it evaluation-only and document the failure as a useful gate.
- [Risk] One negative fixture is still too small for production confidence. → Mitigation: state that broader customer-like same-document/noisy top-k cases remain required.
- [Risk] Future contributors may confuse local evidence with runtime approval. → Mitigation: update specs and docs to state that passing or failing this report does not change defaults.
