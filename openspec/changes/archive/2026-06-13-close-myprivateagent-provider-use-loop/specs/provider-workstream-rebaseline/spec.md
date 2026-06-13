## MODIFIED Requirements

### Requirement: Provider publishes post-access workstream rebaseline
The system SHALL publish a read-only workstream rebaseline after MyPrivateAgent access readiness and live trial feedback are closed, while allowing focused evidence refreshes that help a real caller consume the already-available provider without reopening provider feature expansion.

#### Scenario: Access readiness chain is closed
- **WHEN** Phase 24 trial readiness is `go` and Phase 25 live trial feedback reports `no_provider_action_required`
- **THEN** the rebaseline marks the access-readiness workstream as `closed`
- **AND** it recommends not opening another access-readiness phase unless a future real trial exposes a concrete provider issue

#### Scenario: Provider bugfix lane is trigger-driven
- **WHEN** no provider-owned live trial blocker is present
- **THEN** the provider bugfix workstream is `active_if_triggered`
- **AND** its trigger condition is a real caller trial bug or provider failure evidence

#### Scenario: Backend lane remains candidate-only
- **WHEN** retrieval backend promotion evidence remains review-level or candidate-only
- **THEN** the retrieval backend workstream is `candidate_only`
- **AND** runtime defaults remain unchanged

#### Scenario: Parser and GraphRAG lanes remain deferred
- **WHEN** there is no real corpus parser demand and no relationship-heavy graph use case
- **THEN** parser expansion and GraphRAG workstreams are `deferred`
- **AND** the report records the trigger conditions required to activate them

#### Scenario: Local usable run-loop is an explicit local trigger
- **WHEN** the user goal is local service usability rather than deployment
- **THEN** the workstream baseline allows a local run-loop smoke that validates an already-running service
- **AND** it does not reopen access-readiness phases or promote backend candidates

#### Scenario: MyPrivateAgent use-loop closure is an allowed evidence refresh
- **WHEN** the user goal is to confirm an already-running provider can be used by MyPrivateAgent
- **THEN** the workstream baseline allows refreshing local run-loop, deployed smoke, handoff, and caller enablement documentation
- **AND** it does not reopen access-readiness phases, promote runtime retrieval backends, execute GraphRAG, create source bindings, or move caller control-plane ownership into the provider
