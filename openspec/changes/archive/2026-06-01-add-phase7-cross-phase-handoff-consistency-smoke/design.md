## Design Overview

This change adds a read-only cross-phase consistency smoke artifact.

Input anchor:

1. Phase 7 provider release-readiness export

Alignment checks:

1. Phase 2 decision record keeps Markdown baseline
2. Phase 3 decision record keeps runtime defaults
3. Phase 4 caller-consumption smoke remains ready
4. Phase 5 graph boundary remains ready/planned
5. Phase 6 deployed field-validation remains review/ready with valid state

Output:

- `phase7-cross-phase-handoff-consistency-smoke.{json,md}`

## Status Rules

- `blocked`: release-readiness input missing.
- `review`: input exists but one or more alignment checks fail.
- `ready`: all alignment checks pass.

## Boundaries

- No runtime promotion
- No API changes
- No graph execution rollout
- No parser/runtime behavior changes
