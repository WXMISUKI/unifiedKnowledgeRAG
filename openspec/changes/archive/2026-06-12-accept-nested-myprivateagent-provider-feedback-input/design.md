## Context

Phase 25 feedback originally defined a compact flat caller input contract. MyPrivateAgent later added a compatible payload under `provider_feedback_input` so its repo-side trial outcome can remain useful locally while still carrying provider feedback fields.

The intended operational path is now to pass the MyPrivateAgent trial outcome artifact directly into Phase 25. Without nested payload support, operators would need to manually extract or rewrite JSON, which weakens the closure loop.

## Goals / Non-Goals

**Goals:**

- Accept the nested MyPrivateAgent `provider_feedback_input` payload when present.
- Preserve the original flat input contract.
- Keep invalid or incomplete nested payloads fail-closed through the existing critical field checks.

**Non-Goals:**

- Do not change provider follow-up classification rules.
- Do not execute MyPrivateAgent or call provider HTTP endpoints.
- Do not add retrieval enhancements or provider runtime behavior.

## Decisions

- Normalize the payload immediately after JSON loading:
  - if `provider_feedback_input` is a JSON object, use it as the payload consumed by existing evidence logic
  - otherwise keep the original payload
- Reuse existing missing-field detection and classification logic after normalization.
- Do not introduce a second contract parser; the nested shape is just a transport wrapper around the same Phase 25 payload.

## Risks / Trade-offs

- [Risk] A caller artifact could contain both flat fields and nested fields with different values -> Mitigation: prefer the explicit `provider_feedback_input` object because it is the caller-declared Phase 25 payload.
- [Risk] A malformed nested object could hide useful top-level fields -> Mitigation: keep fail-closed behavior and report missing critical fields rather than trying to merge partial shapes.
