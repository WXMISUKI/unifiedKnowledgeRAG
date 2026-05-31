# Phase 4 Evidence Pack Consumption Contract

- Report: `phase4-evidence-pack-consumption-contract-v1`
- Status: `review`
- Scope: `evidence_pack-v1`
- Generated At: `2026-05-31`

## Purpose

This contract describes how callers should consume `metadata.evidence_pack` from document RAG retrieve and answer envelopes.
It is intentionally read-only and caller-facing. The provider remains the evidence source, not the final answer policy owner.

## Contract Summary

| Field | Meaning | Caller Use |
| --- | --- | --- |
| `pack_id` | Stable fingerprint of the evidence pack payload | Correlate logs and compare pack revisions |
| `version` | Evidence pack contract version | Require `evidence-pack-v1` for current consumers |
| `status` | `answerable` or `insufficient_evidence` | Branch on answerable vs. no-answer flow |
| `reason` | `documents_returned` or `no_documents` | Explain why the pack is answerable or empty |
| `citation_policy` | Current citation policy string | Treat as authoritative for cited answers |
| `allowed_citations` | Endorsed citations for the current answerable evidence set | Use as the only answer citation allowlist |
| `evidence_count` | Number of evidence entries in the pack | Diagnostic and gating signal only |
| `score_summary` | Min/max evidence score summary | Diagnostic only, not an answer policy |
| `retrieval_backend` | Backend that produced the pack | Diagnostic and traceability only |
| `requested_source_ids` | Source ids requested by the caller | Diagnostic and traceability only |
| `filter_context` | Request filter metadata echoed from retrieval | Diagnostic and traceability only |
| `evidence[]` | Compact evidence entries returned by the provider | Use for grounded answer construction and tracing |

## Caller Rules

1. When `status=answerable`, callers may treat `allowed_citations` as the authoritative allowlist for composing or validating a cited answer.
2. When `status=insufficient_evidence`, callers must not infer endorsed citations from the raw `documents` shape and should keep the no-answer branch caller-owned.
3. `pack_id`, `score_summary`, `retrieval_backend`, `requested_source_ids`, and `filter_context` are diagnostics. They help trace the retrieval decision, but they are not a separate answer policy.
4. `evidence[].provenance` is traceability metadata. It helps operators and callers understand where evidence came from, but it does not expand the citation allowlist.
5. The provider may fail closed with `insufficient_evidence` when no supporting documents are returned. That is a valid contract outcome, not a contract failure.

## Evidence Entry Shape

Each `evidence[]` entry is expected to carry compact, caller-visible fields:

- `source_id`
- `document_id`
- `title`
- `citation`
- `score`
- `snippet`
- optional `provenance`

When available, `provenance` includes:

- `source_path`
- `chunk_id`
- `chunking_strategy`
- `citation_anchor`

## Non-Goals

- Final answer policy
- Refusal policy
- User-facing tone or workflow decisions
- Source-to-agent binding
- Retrieval promotion
- Graph execution

## Current Evidence

- `tests/test_evidence_pack.py`
- `tests/test_provider_contract.py`
- `tests/test_provider_contract_smoke.py`
- `docs/smoke/provider-contract/provider-contract-smoke.md`
- `docs/benchmark/chinese-seed/evidence-pack-readiness/phase4-evidence-pack-readiness.md`
- `docs/smoke/evidence-pack-consumption/phase4-caller-consumption-smoke.md`

## Notes

- `answerable` means the pack has endorsed evidence, not that the provider owns final answer policy.
- `insufficient_evidence` means the provider failed closed with a machine-readable diagnostic envelope.
- The contract is intentionally stable so later export and smoke evidence can reference the same semantics.
