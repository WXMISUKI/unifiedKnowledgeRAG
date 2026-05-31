## Context

`evidence_pack-v1` is already implemented and covered by contract smoke. The remaining gap is not retrieval behavior itself; it is the caller contract around what can be trusted, what must be treated as diagnostic, and what remains caller-owned.

## Goals / Non-Goals

**Goals**

- Describe the evidence pack as a caller-consumable contract.
- Make the allowed citation and insufficient-evidence semantics obvious.
- Keep the contract aligned with the current retrieval and answer envelopes.

**Non-Goals**

- Changing retrieval logic, answer finalization logic, or default runtime behavior.
- Moving final answer policy into the provider.
- Adding a new retrieval backend or reranker.

## Decisions

- Keep the contract read-only and local.
  The first Phase 4 slice should be documentation and contract language, not new orchestration.

- Treat `allowed_citations` as the authoritative caller-side allowlist.
  The caller should not infer endorsements from `documents` beyond what the pack permits.

- Treat `insufficient_evidence` as diagnostic, not a failure of the provider contract.
  It is a valid, fail-closed envelope that callers can branch on.

## Risks / Trade-offs

- A purely documentary slice can drift if later code changes alter the pack shape.
  Mitigation: the next two Phase 4 slices will add exportable readiness and smoke coverage.

- If the contract is too broad, it can sound like answer-policy ownership.
  Mitigation: explicitly state the caller still owns final answer style and workflow decisions.
