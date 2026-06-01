# Phase 10 MyPrivateAgent Local Consumer Decision Record

## Decision

Current verdict: `ready_for_local_myprivateagent_consumer_probe_review`

The provider has enough read-only local evidence for a MyPrivateAgent-shaped consumer probe against the recommended local endpoint, while runtime promotion remains explicitly out of scope.

## Evidence

- Contract: `docs/integration/myprivateagent-local-consumer-verification/phase10-myprivateagent-local-consumer-verification-contract.md`
- Readiness: `docs/integration/myprivateagent-local-consumer-verification/phase10-myprivateagent-local-consumer-readiness.json`
- Probe: `docs/smoke/myprivateagent-local-consumer-verification/phase10-myprivateagent-local-consumer-probe.json`
- Handoff bundle: `docs/integration/provider-handoff/provider-handoff-bundle.json`

## Local Posture

- Recommended local URL: `http://127.0.0.1:8020`
- Local API key mode: `not_configured_local_dev` is acceptable for local testing.
- Protected mode remains available when `PROVIDER_API_KEY` is configured for internal or online deployment.

## Boundaries Preserved

- Keep Qdrant, BGE-M3, hybrid retrieval, aggregation, and relation-aware grading behind evidence-backed runtime promotion gates.
- Keep GraphRAG query execution planned, not implemented.
- Keep source-to-agent binding decisions in MyPrivateAgent or another caller.
- Keep registration, heartbeat governance, audit policy, approval workflow, and final answer policy outside this provider.

## Next Gate

The next gate is either:

1. run a real MyPrivateAgent repository integration against the local provider, or
2. wait for an internal/online deployment target and then run protected-mode or private-network validation.

Neither gate is required to keep this provider-side Phase 10 evidence complete.
