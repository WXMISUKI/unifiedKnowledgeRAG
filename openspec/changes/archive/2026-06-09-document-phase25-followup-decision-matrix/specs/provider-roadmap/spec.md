## ADDED Requirements

### Requirement: Stage-3 Phase 25 follow-up uses a documented decision matrix
The project SHALL provide a documented Phase 25 follow-up decision matrix so real caller trial feedback can map to default next actions without reopening provider feature work by ad hoc discussion.

#### Scenario: Decision matrix maps Phase 25 actions to next steps
- **WHEN** Phase 25 returns `no_provider_action_required`, `provider_review_required`, or `provider_blocked`
- **THEN** the project provides a matrix that explains the default next action, whether provider reopen is justified, and what evidence should be reviewed next

#### Scenario: Review result does not reopen provider automatically
- **WHEN** the decision matrix is used for a `provider_review_required` result
- **THEN** the default action is to classify whether the issue is provider-owned, caller-owned, or corpus-owned first
- **AND** the project does not reopen provider-side feature work automatically
