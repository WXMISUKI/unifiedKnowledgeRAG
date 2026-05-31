## Why

Phase 3 already has a lot of candidate evidence, but the promotion decision is still spread across separate benchmark, aggregation, grading, and handoff artifacts. We need one compact review artifact that compares the current gates side by side so reviewers can see what is still missing before any runtime default changes are considered.

## What Changes

- Add a read-only Phase 3 retrieval promotion gap matrix under `docs/benchmark/chinese-seed/retrieval-promotion-readiness/`.
- Summarize current evidence gaps for Qdrant, BGE-M3, hybrid retrieval, hybrid gating, multi-chunk aggregation, relation-aware grading, and deployed smoke.
- Keep the matrix lightweight and review-oriented. It should help reviewers decide what to do next, not decide promotion automatically.
- Do not change runtime retrieval defaults, provider HTTP contracts, or promotion gates.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `retrieval-benchmark-harness`: benchmark evidence is organized into a single Phase 3 promotion gap matrix for review.
- `provider-roadmap`: records the gap matrix as lightweight Phase 3 evidence review work, not runtime promotion.

## Impact

- Affected docs: `docs/benchmark/chinese-seed/retrieval-promotion-readiness/phase3-retrieval-promotion-gap-matrix.md`
- Affected roadmap docs: `docs/roadmap/lightweight_provider_roadmap.md`
- Affected progress notes: `docs/progress/provider-improvement-tracker.md`
- No runtime behavior changes, no new HTTP API, no new dependencies
