## Why

Phase 12b through Phase 12f already give us enough evidence to see the current candidate-backend posture, but they also show a clear anti-pattern risk: the work can keep drifting into pgvector-local detail while the broader provider goal stays under-served.

We need one global checkpoint that answers the next practical question:

- Should we keep digging into pgvector, or pause that spike for now?
- What is the next small slice that best serves the provider as a lightweight external knowledge component?
- How do we keep the answer visible through the same handoff and refresh chain used by the rest of the project?

This change keeps the project provider-first and evidence-driven. It does not promote runtime defaults, and it does not start a new backend benchmark loop.

## What Changes

- Add a Phase 13 provider-roadmap decision checkpoint that consolidates the current Phase 12b to Phase 12f evidence chain into one review artifact.
- Make the checkpoint explicit about the next recommended focus so we do not continue an unbounded pgvector-local optimization loop by default.
- Surface the checkpoint through provider handoff bundle and handoff refresh as optional review evidence.
- Keep the checkpoint read-only, local, and outside runtime promotion.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `provider-roadmap`: add a global decision checkpoint that chooses the next slice from evidence instead of local tuning momentum.
- `retrieval-benchmark-harness`: keep candidate evaluation evidence comparable, but do not let the checkpoint imply backend promotion.

## Impact

- Adds `docs/operations/provider-roadmap-decision-checkpoint/` evidence files.
- Adds a checkpoint service and export script under `app/services/` and `scripts/`.
- Adds optional handoff bundle and refresh visibility for the new checkpoint.
- Updates roadmap and progress documentation so the next phase is described as a deliberate global decision, not a local backend spiral.
