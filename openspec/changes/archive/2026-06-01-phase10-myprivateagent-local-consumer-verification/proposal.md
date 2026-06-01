## Why

Phase 9 translated provider-side readiness into a MyPrivateAgent local-consumption contract, but there is still no caller-shaped verification slice that exercises the local provider from the perspective of a MyPrivateAgent consumer.

We need a lightweight, read-only Phase 10 slice that turns the Phase 9 handoff posture into a repeatable local consumer verification artifact before any MyPrivateAgent repository integration, protected-mode deployment, or runtime promotion work.

## What Changes

- Add a Phase 10 MyPrivateAgent local consumer verification contract document.
- Add a Phase 10 local consumer readiness export service, script, and focused tests.
- Add a Phase 10 local consumer probe smoke service, script, and focused tests.
- Wire Phase 10 readiness/probe evidence into provider handoff bundle and handoff refresh as optional evidence.
- Add a Phase 10 local consumer verification decision record.
- Update roadmap and provider improvement tracker with Phase 10 artifacts.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: Record Phase 10 as read-only MyPrivateAgent local consumer verification evidence that preserves runtime-default, source-binding, and GraphRAG boundaries.
- `knowledge-provider`: Allow provider handoff and refresh workflows to summarize optional Phase 10 MyPrivateAgent local consumer verification evidence.

## Impact

- Adds local documentation and evidence exports under `docs/integration/myprivateagent-local-consumer-verification/` and `docs/smoke/myprivateagent-local-consumer-verification/`.
- Adds focused export services and scripts for Phase 10 readiness and probe evidence.
- Extends existing handoff bundle and refresh aggregation with optional Phase 10 rows.
- Does not change public HTTP contracts, runtime defaults, retrieval behavior, embedding behavior, GraphRAG execution, source-to-agent binding, or MyPrivateAgent control-plane responsibilities.

## Non-Goals

- No MyPrivateAgent repository changes.
- No runtime default promotion for Qdrant/BGE-M3/hybrid.
- No GraphRAG query execution implementation.
- No source-to-agent binding mutation.
- No provider registration, heartbeat, audit, approval, or final-answer policy ownership.
