## Context

`company_profile_2025_trial` and `refund_policy_docs` currently go through the same chunk-quality diagnostics, but they do not expose the same provenance shape. The company-profile source comes from page-oriented material and naturally carries `page-*` provenance in chunk previews. `refund_policy_docs` is a markdown fixture with section/exact-term style citations instead of page ids. Requiring page coverage for both shapes makes the markdown source look like a chunk-quality problem, even though the real source-specific failure is currently negative-control leakage.

## Goals / Non-Goals

**Goals:**

- Separate page-based provenance expectations from generic markdown provenance expectations.
- Keep chunk-quality review meaningful for paged sources like `company_profile_2025_trial`.
- Stop treating non-page markdown provenance as a chunk-quality review trigger by itself.
- Refresh real evidence so the next follow-up gate is clearer.

**Non-Goals:**

- No retrieval behavior changes.
- No query rewrite, rerank, hybrid retrieval, RAPTOR, Self/Corrective RAG, or GraphRAG work.
- No negative-control hardening in this slice.
- No parser-engine or public HTTP API changes.

## Decisions

1. **Infer provenance expectation from observed citation shape instead of source-specific allowlists.**
   - Rationale: The diagnostics logic should stay lightweight and generic. If chunk citations or anchors clearly use `#page-*`, then page coverage is expected. Otherwise the source should be treated as non-page provenance.
   - Alternative considered: Hard-code markdown source ids such as `refund_policy_docs`. That would not scale and would make the diagnostics brittle.

2. **Keep provenance information visible, but remove page-coverage review for non-page sources.**
   - Rationale: We still want evidence about provenance shape, but non-page markdown sources should not be marked `review` solely for missing page ids.
   - Alternative considered: Keep the review and only reword the reason. That would preserve an unhelpful blocker and keep the next-step recommendations noisy.

3. **Leave aggregate review conservative and let remaining real issues drive the next gate.**
   - Rationale: After alignment, `refund_policy_docs` may still stay in `review` because of negative-control leakage. That is the correct next signal.
   - Alternative considered: Bundle negative-control hardening into the same slice. That would blur the boundary and reintroduce local optimization pressure.

## Risks / Trade-offs

- **Risk: Provenance inference could misclassify an unusual source.** -> Mitigation: Base the rule on observed citation anchors and chunk citations, and keep the behavior narrow: it only affects whether page coverage is required.
- **Risk: Removing a review signal could hide quality issues.** -> Mitigation: Only remove the page-coverage trigger for non-page provenance; citation coverage, chunk count, and tiny/noisy chunk checks still apply.
- **Risk: The aggregate report may remain `review` after alignment.** -> Mitigation: That is expected and useful because it isolates the remaining real issue instead of masking it.
