## ADDED Requirements

### Requirement: Provider publishes MyPrivateAgent local use closure evidence
The provider SHALL publish a local MyPrivateAgent use-loop closure that distinguishes local caller usability from production deployment promotion.

#### Scenario: Local provider use is closed
- **WHEN** the local usable run-loop reports `decision=go`
- **THEN** the closure evidence identifies the provider base URL, ready checks, RAG retrieve evidence status, RAG answer status, and boundary fields that keep runtime defaults unchanged

#### Scenario: Deployment review does not block local caller use
- **WHEN** deployed provider smoke reports `status=review` only because handoff or deployment readiness remains review-level
- **THEN** the closure evidence explains that MyPrivateAgent local use can still proceed if health, manifest, preflight, source bindings, and local run-loop checks are ready

#### Scenario: Closure preserves provider boundaries
- **WHEN** provider use-loop closure is documented
- **THEN** it states that the provider does not create source-to-agent bindings, write MyPrivateAgent configuration, promote retrieval defaults, execute GraphRAG, or own caller answer policy

### Requirement: Provider documents MyPrivateAgent enablement handoff
The provider SHALL document the minimal caller-facing sequence for MyPrivateAgent to enable and verify the external provider.

#### Scenario: Caller handoff lists required MyPrivateAgent settings
- **WHEN** a maintainer reads the provider-use runbook
- **THEN** it lists the MyPrivateAgent configuration keys needed to enable the knowledge provider and the expected local base URL

#### Scenario: Caller handoff lists verification commands
- **WHEN** a maintainer reads the provider-use runbook
- **THEN** it identifies the provider-side evidence commands and the MyPrivateAgent-side caller verification step without requiring provider code changes

#### Scenario: Caller handoff preserves GraphRAG boundary
- **WHEN** the runbook documents capability ids
- **THEN** it identifies document RAG retrieval as usable and keeps GraphRAG execution as planned or separately gated

### Requirement: Provider keeps OpenSpec work queue clean after closure
The provider SHALL keep active OpenSpec changes aligned with real implementation work.

#### Scenario: Empty stale change is removed or documented
- **WHEN** an active OpenSpec change has no proposal, design, tasks, or spec delta
- **THEN** the closure work either removes it from the active queue or records why it remains active

#### Scenario: Future provider work remains trigger-driven
- **WHEN** the closure is complete
- **THEN** the repository still requires future provider changes to declare a concrete trigger such as real caller feedback, provider-owned gap, repeated cross-source failure class, deployment-owner request, or runtime strategy evaluation
