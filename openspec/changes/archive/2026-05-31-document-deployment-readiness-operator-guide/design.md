## Context

The deployment readiness export is intentionally conservative and currently reports `review`. The operator guide should turn the evidence into a practical pre-deployment checklist without expanding runtime responsibilities.

## Goals / Non-Goals

**Goals**

- Explain current readiness signals in plain operational terms.
- Preserve the boundary between local development, deployment preparation, and external control-plane ownership.
- Keep the guide aligned with existing export commands.

**Non-Goals**

- No runtime default changes.
- No new deployment automation.
- No new access control or governance features.

## Decisions

- Write the guide as a local operator playbook under `docs/operations/deployment-readiness/`.
- Keep the guide anchored to current evidence fields and existing export commands.
- Explicitly call out that deployed smoke remains optional until a live base URL exists.

## Risks / Trade-offs

- The guide can drift if evidence fields change; mitigation is to keep it descriptive and tied to the exported report fields.
- Too much detail could make it feel like a policy document; keep it action-oriented and short.
