## Design Overview

This change introduces a Phase 11 local provider integration dry-run layer that sits above Phase 10 local consumer verification. It stays provider-side and read-only, but models the exact evidence checkpoints a MyPrivateAgent local integration would consume.

The Phase 11 dry-run has four executable outputs:

1. local integration profile export,
2. provider discovery smoke,
3. RAG retrieve consumption smoke,
4. source-binding preview smoke.

These outputs are accompanied by a contract and a decision record.

## Inputs

Required local evidence:

1. Phase 10 local consumer contract/readiness/probe
2. provider integration probe
3. provider contract smoke
4. provider handoff bundle
5. source binding summary

Supporting local evidence:

1. deployed provider smoke (optional)
2. Phase 4 evidence-pack readiness and caller-consumption smoke

## Output Files

1. `docs/integration/myprivateagent-local-provider-integration/phase11-local-provider-integration-contract.md`
2. `docs/integration/myprivateagent-local-provider-integration/phase11-local-provider-integration-profile.json`
3. `docs/integration/myprivateagent-local-provider-integration/phase11-local-provider-integration-profile.md`
4. `docs/smoke/myprivateagent-local-provider-integration/phase11-provider-discovery-smoke.json`
5. `docs/smoke/myprivateagent-local-provider-integration/phase11-provider-discovery-smoke.md`
6. `docs/smoke/myprivateagent-local-provider-integration/phase11-rag-retrieve-consumption-smoke.json`
7. `docs/smoke/myprivateagent-local-provider-integration/phase11-rag-retrieve-consumption-smoke.md`
8. `docs/smoke/myprivateagent-local-provider-integration/phase11-source-binding-preview-smoke.json`
9. `docs/smoke/myprivateagent-local-provider-integration/phase11-source-binding-preview-smoke.md`
10. `docs/integration/myprivateagent-local-provider-integration/phase11-local-provider-integration-decision-record.md`

## Boundaries

- No MyPrivateAgent repository modifications.
- No runtime default promotion.
- No GraphRAG execution implementation.
- No source-to-agent binding mutation.
- No provider registration, heartbeat governance, audit policy, or final answer policy ownership.
