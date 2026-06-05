## ADDED Requirements

### Requirement: Phase 18 MyPrivateAgent access gate stays primitive and non-circular
The project SHALL expose a simplified MyPrivateAgent access gate that decides repo-side trial readiness from provider-owned primitive access evidence rather than downstream handoff reports.

#### Scenario: Primitive access signals are the gate source of truth
- **WHEN** access-focused visibility or Phase 14/15/16 access reports classify MyPrivateAgent repo-side trial readiness
- **THEN** they use provider contract smoke, Phase 10 local consumer probe, Phase 11 provider discovery smoke, Phase 11 retrieve-consumption smoke, and Phase 11 source-binding preview smoke as the primitive gate inputs
- **AND** they do not require Phase 14, Phase 15, Phase 16, full handoff bundle, or handoff refresh to be `ready` before the primitive access gate can be `ready`

#### Scenario: Review context remains visible but non-blocking
- **WHEN** Phase 10 readiness, Phase 11 profile, Phase 13 checkpoint, Phase 14 acceptance, Phase 15 dispatch, Phase 16 access loop, full handoff bundle, or handoff refresh is still in `review`
- **THEN** access reports surface those items as review context
- **AND** they do not classify them as primitive blockers unless a required primitive access signal is missing or blocked

### Requirement: Phase 18 preserves provider-only boundaries
The project SHALL keep the simplified MyPrivateAgent access gate read-only and provider-first.

#### Scenario: Access gate does not execute the repo-side trial
- **WHEN** the Phase 18 access gate is generated or consumed
- **THEN** it does not execute MyPrivateAgent repository code
- **AND** it does not create source-to-agent binding
- **AND** it does not promote runtime defaults
- **AND** it does not move caller control-plane ownership into this provider

#### Scenario: Broader handoff review remains separate
- **WHEN** broader deployment, backend candidate, live URL, or promotion evidence remains in `review`
- **THEN** the full provider handoff bundle and refresh reports may remain `review`
- **AND** the access-focused gate still reports the minimal MyPrivateAgent access posture separately
