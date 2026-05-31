# Provider Improvement Tracker

## Scope

- Project: `unifiedKnowledgeRAG`
- Roadmap: `docs/roadmap/lightweight_provider_roadmap.md`
- Mode: lightweight, agile, evidence-driven
- Rhythm: specification -> implementation -> archive

## Completed

- Phase 0 baseline contracts: health, manifest, capabilities, preflight, integration probe, contract smoke.
- Phase 2 diagnostics baseline: source manifest, fingerprint drift, ingestion preflight, chunk manifest, source package metadata.
- Phase 4 evidence packaging baseline: `evidence_pack-v1` and insufficient-evidence fail-closed behavior.
- Phase 5 boundary-only graph evidence: graph schema discovery in preflight/contract smoke; graph query remains planned boundary.
- Phase 6 operations baseline: deployment readiness, reindex readiness, handoff bundle, handoff refresh, handoff API.
- Phase 6 optional live-url evidence: deployed provider smoke and source-binding checks.
- Source binding compact summary and aggregate count reuse in handoff/deployed-smoke evidence.
- Phase 3 customer-like benchmark expansion completed (`2026-05-31-expand-phase3-customer-like-benchmark-cases`), with baseline fixture expanded to 24 cases.
- Phase 3 handoff evidence summary completed and archived (`2026-05-31-add-phase3-evidence-summary-to-handoff`), adding optional baseline metric rollup to provider handoff bundle.
- Phase 3 false-positive/false-negative customer-like extension completed and archived (`2026-05-31-expand-phase3-fp-fn-customer-like-cases`), with baseline fixture expanded to 26 cases and one expected-empty false-positive risk explicitly exposed.

## In Progress

- Keep local evidence artifacts aligned with current code/spec state after each accepted slice.

## Benchmark Fixture Scope

- Baseline retrieval fixture `tests/fixtures/retrieval_benchmark_cases.json` is expanded to 26 cases.
- Customer-like additions in this round:
  - one nuanced high-value refund review case (`policy-nuance`)
  - two cross-domain expected-empty trap cases (`empty`)
- Current empty-case count in baseline fixture: 10.

## Phase 3 Evidence Refresh

- Refresh changes:
  - `refresh-phase3-seed-evidence-after-fixture-expansion`
  - `2026-05-31-expand-phase3-fp-fn-customer-like-cases` follow-up refresh
- Refreshed artifact:
  - `docs/benchmark/chinese-seed/retrieval-candidates/fixture-chinese-seed-baseline.json`
  - `docs/benchmark/chinese-seed/retrieval-candidates/fixture-chinese-seed-baseline.md`
- Refreshed baseline summary:
  - `total_cases=26`
  - `hit_rate=0.9615`
  - `citation_match_rate=0.9615`
  - `empty_handling_rate=0.9000`
  - `empty.total_cases=10`
  - `policy-nuance.total_cases=2`

## Pending

- Keep deployment readiness review notes actionable until non-mock embedding/retrieval candidates are promoted by evidence.
- Continue Phase 3 retrieval-quality promotion only with customer-like benchmark evidence; do not promote defaults by single-metric wins.
- Keep GraphRAG execution deferred until relationship-heavy use cases and operations ownership are explicitly approved.
- Keep parser expansion (PDF/Word/Excel/OCR) deferred until real corpus demand and separate evidence-backed changes.
- Continue next smallest Phase 3 slice on false-positive/false-negative customer-like benchmark coverage (evidence only, no runtime default promotion).

## Next Step Plan

1. Create the next smallest OpenSpec change that advances Phase 3 evidence (without changing runtime defaults).
2. Add customer-like benchmark fixtures focused on false-positive/false-negative review.
3. Export updated candidate evidence and compare category-level metrics.
4. Promote nothing by default unless gate evidence clearly passes.

## Latest Refresh

- Run time: `2026-05-31T06:51:27Z`
- Command: `python scripts/export_provider_handoff_refresh.py`
- Refresh status: `review`
- Step summary:
  - `provider_integration_probe`: `ready`
  - `provider_contract_smoke`: `ready` (`9/9` checks)
  - `deployment_readiness`: `review`
  - `reindex_readiness`: `ready`
  - `source_binding_summary`: `ready`
  - `provider_handoff_bundle`: `review`

## Current Gaps To Close

- Deployment readiness remains `review` because embedding is still `mock`, retrieval backend is still `fixture`, model artifacts are not configured, and provider API key is not configured.
- Handoff bundle remains `review` because deployment readiness is `review` and optional deployed smoke evidence is not present for a live URL.
- Runtime promotion gates remain open for Phase 3 and GraphRAG execution; current evidence is candidate-level, not production approval.
