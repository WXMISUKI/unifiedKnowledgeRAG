## Design Overview

This change adds a read-only Phase 7 release-readiness report that aggregates cross-phase evidence signals.

Core required signals:

1. Phase 7 acceptance contract
2. provider integration probe
3. provider contract smoke
4. source binding summary

Optional review signals:

- representative Phase 2/3/4/5/6 readiness and smoke artifacts

## Decisions

- `ready_for_local_provider_handoff` is true only when all required signals are ready.
- `ready_for_runtime_default_promotion` remains conservative and requires promotion-facing Phase 3/Phase 6 signals to be fully ready.
- Report status can be `review` even when local handoff is ready, because runtime promotion is separately gated.

## Boundaries

- No runtime default promotion
- No new API endpoint
- No ingestion/retrieval/graph execution changes
