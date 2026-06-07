# local-document-source-onboarding-loop Specification

## Purpose
Provide a single lightweight local operator loop for onboarding markdown business documents as provider-visible local sources.

## Requirements
### Requirement: Local document source onboarding loop can be exported
The system SHALL export a single local onboarding report that chains markdown corpus trial, caller handoff, approved local source registration, and acceptance smoke for a local business document source.

#### Scenario: Local document source onboarding passes
- **WHEN** the configured markdown path exists
- **AND** the business corpus trial returns `decision=go`
- **AND** the caller handoff is `ready_for_caller_review`
- **AND** the approved source registration is `registered`
- **AND** the acceptance smoke returns `decision=go`
- **THEN** the onboarding report has `decision=go`
- **AND** it records source id, query, markdown path, step statuses, artifact paths, registered source path, acceptance summary, and recommended next action

#### Scenario: Local document source onboarding needs review
- **WHEN** no onboarding step is blocked
- **AND** at least one trial or acceptance step returns `review`
- **THEN** the onboarding report has `decision=review`
- **AND** it identifies the review step and recommended recovery action

#### Scenario: Local document source onboarding is blocked
- **WHEN** the markdown file is missing, corpus trial blocks, handoff blocks, registration blocks, or acceptance smoke blocks
- **THEN** the onboarding report has `decision=blocked`
- **AND** it records the blocking step and machine-readable reason code

### Requirement: Local document source onboarding remains lightweight
The local document source onboarding loop SHALL orchestrate existing local provider steps without promoting heavier ingestion or runtime behavior.

#### Scenario: Onboarding loop runs
- **WHEN** the onboarding command runs
- **THEN** it does not parse raw PDFs as supported provider ingestion, start OCR services, create source-to-agent bindings, call MyPrivateAgent, create formal ingestion jobs, promote retrieval backends, call vector databases, mutate `/api/chat`, or execute GraphRAG

#### Scenario: Source is registered locally
- **WHEN** onboarding reaches approved local source registration
- **THEN** registration remains a local reversible provider source registration
- **AND** caller-owned source-to-agent binding decisions remain outside the provider
