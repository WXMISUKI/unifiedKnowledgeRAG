## Design Overview

This change adds a read-only Phase 10 MyPrivateAgent local consumer verification slice. It consumes the Phase 9 local-consumption posture and existing provider evidence to produce a caller-shaped verification contract, readiness export, probe smoke, and decision record.

The slice verifies that a local MyPrivateAgent consumer can reason about:

1. recommended local base URL and access mode,
2. provider identity and manifest access,
3. provider preflight and source-binding review reachability,
4. provider handoff evidence availability,
5. Phase 4 evidence-pack caller-consumption readiness,
6. graph planned-boundary preservation,
7. runtime-promotion boundary preservation.

## Inputs

Required local evidence:

1. Phase 9 local-consumption contract
2. Phase 9 local-consumption readiness
3. Phase 9 local-consumption smoke
4. Provider handoff bundle

Supporting evidence:

1. deployed provider smoke when available for `http://127.0.0.1:8020`
2. Phase 4 evidence-pack readiness and caller-consumption smoke
3. provider integration probe and provider contract smoke through existing handoff evidence

## Outputs

1. `docs/integration/myprivateagent-local-consumer-verification/phase10-myprivateagent-local-consumer-verification-contract.md`
2. `docs/integration/myprivateagent-local-consumer-verification/phase10-myprivateagent-local-consumer-readiness.json`
3. `docs/integration/myprivateagent-local-consumer-verification/phase10-myprivateagent-local-consumer-readiness.md`
4. `docs/smoke/myprivateagent-local-consumer-verification/phase10-myprivateagent-local-consumer-probe.json`
5. `docs/smoke/myprivateagent-local-consumer-verification/phase10-myprivateagent-local-consumer-probe.md`
6. `docs/integration/myprivateagent-local-consumer-verification/phase10-myprivateagent-local-consumer-decision-record.md`

## Decisions

- Phase 10 is provider-side verification evidence, not a MyPrivateAgent integration change.
- The recommended local base URL remains `http://127.0.0.1:8020`.
- Local development may keep `PROVIDER_API_KEY` unset; protected mode remains optional and documented for later internal or online deployment.
- The consumer probe is read-only and report-oriented. It must not create source bindings, run ingestion, rebuild indexes, call embedding models, call vector databases, execute GraphRAG, or compose final user-facing answers beyond existing evidence-pack validation summaries.
- Phase 10 readiness/probe artifacts are optional rows in provider handoff bundle and refresh chain, so missing evidence remains reviewable rather than blocking unrelated provider readiness.

## Boundaries

- No runtime default promotion for Qdrant/BGE-M3/hybrid.
- No GraphRAG query execution implementation.
- No source-to-agent binding mutation.
- No caller control-plane governance ownership changes.
- No requirement to run a long-lived local server during normal test execution.
