## Design Overview

This change adds a read-only Phase 9 MyPrivateAgent local-consumption evidence slice that converts existing provider-side readiness into caller-consumable local handoff context.

Core required signals:

1. Phase 9 local-consumption contract document
2. Phase 7 provider release readiness
3. Phase 8 live URL validation readiness

Optional supporting signals:

1. deployed provider smoke
2. provider source-binding summary
3. Phase 4 evidence-pack readiness and caller-consumption smoke

## Decisions

- Phase 9 is local-consumption review evidence and does not promote runtime defaults.
- Local development can keep `PROVIDER_API_KEY` unset; if configured later, component-level access headers are reused.
- Readiness and smoke remain read-only artifacts generated from existing evidence.
- Phase 9 readiness/smoke are optional rows in provider handoff bundle and refresh chain.

## Boundaries

- No runtime default promotion for Qdrant/BGE-M3/hybrid.
- No GraphRAG query execution implementation.
- No source-to-agent binding mutation.
- No caller control-plane governance ownership changes.
