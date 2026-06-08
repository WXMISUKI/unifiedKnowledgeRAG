## Context

The aggregate real-business golden-case baseline now has two real sources. `company_profile_2025_trial` remains `go`, while `refund_policy_docs` is `review`. The observed issues are different in nature: one case leaks evidence for an expected-empty question, and the same source also fails chunk-quality review because markdown fixtures do not expose page ids. If we jump straight into retrieval or chunking changes, we risk mixing a negative-control issue with a provenance-diagnostics issue and overfitting the provider to one local source.

## Goals / Non-Goals

**Goals:**

- Make the `refund_policy_docs` review outcome easier to interpret.
- Separate negative-control leakage from markdown provenance mismatch in report-level evidence.
- Keep the next recommended action tied to classified evidence instead of generic optimization.
- Preserve current runtime behavior and current aggregate fixture structure.

**Non-Goals:**

- No query rewrite, rerank, hybrid retrieval, RAPTOR, Self/Corrective RAG, or GraphRAG work.
- No Qdrant, pgvector, BGE-M3, parser-engine, or source-binding changes.
- No public HTTP API changes.
- No attempt to force the aggregate report back to `go` in this slice.

## Decisions

1. **Add report-level classification, not runtime diagnosis.**
   - Rationale: The existing report already carries enough observable evidence to classify current review signals into smaller categories. This keeps the slice lightweight and avoids pretending the provider can infer root cause automatically at runtime.
   - Alternative considered: Add new retrieval-time heuristics or score tracing. That would expand scope into runtime behavior rather than report interpretation.

2. **Treat markdown provenance mismatch as a separate review class from chunk-quality degradation.**
   - Rationale: `page_coverage_missing` on a markdown fixture is not the same kind of signal as tiny/noisy chunk degradation on OCR-derived corpora. The report should make that distinction explicit so we do not trigger the wrong next change.
   - Alternative considered: Keep both under a single chunking bucket. That would blur whether the next gate is chunk restructuring or diagnostics alignment.

3. **Keep aggregate decision rules conservative.**
   - Rationale: Even after classification, a reviewed source should still keep the aggregate report in `review`. This slice improves decision quality, not promotion thresholds.
   - Alternative considered: Downgrade markdown provenance mismatch to `go`. That would hide a real diagnostics mismatch before we explicitly decide how to treat it.

## Risks / Trade-offs

- **Risk: Classification labels may look more precise than they really are.** -> Mitigation: Keep them phrased as observed review classes and continue using explicit non-goals and recommendation boundaries.
- **Risk: Additional report fields increase maintenance cost.** -> Mitigation: Reuse existing case and chunk diagnostics, and add only compact summary fields and recommendation branching.
- **Risk: The next step may still remain ambiguous after classification.** -> Mitigation: Keep recommendations narrow and map them to one of a few concrete gates: negative-control hardening or markdown diagnostics alignment.
