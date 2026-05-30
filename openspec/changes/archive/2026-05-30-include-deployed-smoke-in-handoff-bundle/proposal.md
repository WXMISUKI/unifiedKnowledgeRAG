## Why

The deployed HTTP smoke probe now validates a running provider URL, but the handoff bundle still only summarizes local evidence files. MyPrivateAgent and deployment reviewers should be able to inspect one handoff artifact and see whether deployed smoke evidence is missing, reviewable, ready, or blocked.

## What Changes

- Add deployed provider smoke as optional evidence in the provider handoff bundle.
- Preserve local-development usability: missing deployed smoke evidence marks the bundle `review`, not `blocked`.
- Treat present deployed smoke evidence as authoritative: `ready`/`review` are surfaced, while `blocked` blocks the bundle.
- Add operation notes and recommended actions that distinguish optional deployment evidence from required local evidence.
- Keep handoff bundle read-only and avoid running the deployed smoke probe from handoff generation.

## Capabilities

### New Capabilities

### Modified Capabilities

- `knowledge-provider`: Handoff bundle summarizes optional deployed smoke evidence when present or missing.
- `provider-roadmap`: Phase 6 handoff evidence may include optional deployed smoke status without making local development depend on a running external URL.

## Impact

- Updates `provider_handoff_bundle` evidence spec modeling and artifact status handling.
- Updates focused handoff bundle tests and documentation.
- No new HTTP endpoints, no runtime default changes, and no new dependencies.
