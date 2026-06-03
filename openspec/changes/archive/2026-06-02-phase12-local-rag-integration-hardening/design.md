## Design Overview

We split the slice into five hardening layers. The goal is deterministic local use with zero runtime promotion.

### 1) Contract Layer

Define a local contract that is explicitly consumable by MyPrivateAgent:
- Recommended base URL: `http://127.0.0.1:8020`.
- API mode: local development supports no-key mode by default; when key mode is enabled, both accepted headers are documented and accepted:
  - `Authorization: Bearer <token>`
  - `X-Provider-Api-Key: <token>`
- Mandatory local evidence inputs:
  - manifest capability state,
  - integration readiness profile,
  - source-binding preview,
  - provider contract smoke.

### 2) Consumption Layer

Lock retrieval consumption expectations:
- `answerable` and `insufficient_evidence` remain the only allowed `evidence_pack-v1` states for caller-safe handling.
- `use_only_returned_citations` remains enforced.
- `allowed_citations` must be exactly derivable from returned evidence entries.
- RAG retrieval calls should remain deterministic under local fixture/mock defaults for repeatable local QA.

### 3) Endpoint/Health Layer

Keep provider component access and health checks stable:
- `/health` remains public.
- `/api/*` follows local access-mode policy and does not add new protected routes in this slice.
- No caller-owned policy or orchestration logic is added.

### 4) Evidence Layer

Introduce a hardening export bundle that aggregates existing artifacts:
- phase11 local provider integration contract/profile signal;
- phase10 local consumer readiness/probe signals;
- provider handoff profile;
- phase3 candidate hardening signals required for RAG quality safety.

This layer should provide a single local document summarizing "can we integrate now" and "what remains blocked".

### 5) Smoke Layer

Add one deterministic local hardening smoke that checks:
- manifest/preflight availability,
- retrieval consumption semantics,
- source-binding preview visibility,
- phase3/6 candidate gate visibility required for local production ramp.

## Non-Goals

- No GraphRAG execution changes.
- No parser expansion for PDF/Word/Excel/OCR in this slice.
- No runtime default promotion.
- No registration/heartbeat/audit/governance workflow logic changes.
- No MyPrivateAgent repository changes.

## Implementation Boundaries

This slice is read-only evidence and smoke.
- It adds/updates documentation and exporter wiring only.
- It does not require local index rebuilds or model downloads.
- It preserves caller ownership for final answer policy, approvals, and source-to-agent binding.
