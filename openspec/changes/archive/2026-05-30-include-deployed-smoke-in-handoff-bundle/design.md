## Context

The provider handoff bundle is the intended single review entry point before external binding. Recent work added `deployed-provider-smoke-v1`, but it remains outside the handoff bundle, so reviewers must know to check a separate artifact. At the same time, deployed smoke depends on an already-running URL and should not become mandatory for every local handoff refresh.

## Goals / Non-Goals

**Goals:**

- Include deployed smoke in the handoff bundle as optional Phase 6 evidence.
- Make missing optional deployed smoke a review condition with a clear recommended action.
- Make blocked deployed smoke a hard blocker when the evidence exists.
- Keep existing required evidence behavior unchanged.

**Non-Goals:**

- Do not run `scripts/export_deployed_provider_smoke.py` from bundle generation or refresh.
- Do not require a live HTTP provider during normal local tests.
- Do not add registration, heartbeat, reverse proxy, TLS, or secret-management behavior.

## Decisions

- Extend `HandoffEvidenceSpec` with a `required` flag defaulting to `True`.
  - Rationale: current evidence remains required, while deployed smoke can be optional in local and pre-deployment contexts.
  - Alternative considered: keep all evidence required; rejected because missing deployed smoke would block ordinary local provider handoff.
- Report missing optional evidence as `review`.
  - Rationale: it is meaningful for deployment review but not a broken provider state before deployment.
  - Alternative considered: use a new `optional_missing` status; rejected to avoid widening bundle status vocabulary.
- Keep deployed smoke refresh explicit.
  - Rationale: it needs a caller-selected base URL and optional API key. Handoff bundle should read existing evidence, not guess deployment targets.

## Risks / Trade-offs

- Optional evidence can be overlooked. Mitigation: add a dedicated recommended action and operation note when deployed smoke is missing.
- The bundle may remain `review` more often. Mitigation: this matches current lightweight evidence workflow, where review artifacts guide operator decisions rather than silently approving deployment.
