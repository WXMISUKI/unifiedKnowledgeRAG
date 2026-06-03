## Why

Short-term work should remove friction for MyPrivateAgent local RAG integration before any backend migration.

Current local integration evidence is in good shape for readiness and proof, but it is still review-oriented and not yet a hardened local operating slice:
- provider contract, preflight, and retrieve semantics are present;
- access-key assumptions vary by operator;
- local URL and evidence linkage assumptions are not yet fully consolidated for repeated developer/operator execution.

To keep the project lightweight, this slice should tighten the local consumption path as deterministic operations, not runtime promotion.

## What Changes

- Add a local RAG integration hardening contract focused on MyPrivateAgent local usage.
- Add a local hardening profile and hardening readiness artifact bundle, scoped to:
  - manifest discoverability,
  - integration smoke,
  - source-binding preview,
  - retrieval consumption/fail-closed behavior.
- Clarify and freeze local endpoint/auth assumptions for short-term local-only validation.
- Keep all outputs read-only and evidence-only.
- Keep runtime defaults unchanged.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: add explicit short-term local integration hardening acceptance gates inside the open-source strategy flow.
- `knowledge-provider`: keep local integration assumptions explicit and exportable for MyPrivateAgent local RAG integration.

## Impact

- Adds local hardening documentation and evidence export artifacts under `docs/integration/myprivateagent-local-rag-integration-hardening/` and `docs/smoke/myprivateagent-local-rag-integration-hardening/`.
- Adds small delta requirements to `provider-roadmap` and `knowledge-provider` to keep this slice bounded and reviewable.
- No runtime default promotion and no control-plane responsibilities are moved into this provider.
- No runtime behavior changes are required in this slice.
