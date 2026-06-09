## ADDED Requirements

### Requirement: Stage-2 caller trial execution task pack is documented after the runbook
The project SHALL provide a stage-2 caller trial execution task pack after the post-closure runbook so teams can turn the ordered workflow into concrete execution tasks.

#### Scenario: Task pack turns the workflow into execution tasks
- **WHEN** the caller trial feedback runbook already defines the ordered post-closure sequence
- **THEN** the project may add a stage-2 task pack that names pre-trial checks, trial goals, required outputs, and provider feedback handoff expectations

#### Scenario: Task pack stays boundary-safe
- **WHEN** the task pack is used
- **THEN** it helps a caller prepare and report a real trial
- **AND** it does not execute the caller, create source bindings, mutate runtime defaults, or reopen provider-side feature work by itself
