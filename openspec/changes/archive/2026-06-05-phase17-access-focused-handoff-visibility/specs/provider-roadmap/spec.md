## Added Requirements

### Requirement: Phase 17 access-focused handoff visibility stays lightweight
The project SHALL expose an access-focused handoff visibility view that helps MyPrivateAgent judge repo-side trial readiness without turning the full provider handoff bundle into a false blocker for unrelated review-only evidence.

#### Scenario: Access-focused visibility is derived from the MyPrivateAgent access chain
- **WHEN** the provider handoff bundle or refresh is exported
- **THEN** it includes an access-focused visibility summary derived from the Phase 10, Phase 11, Phase 13, Phase 14, Phase 15, and Phase 16 access path

#### Scenario: Access-focused visibility does not rewrite the full bundle posture
- **WHEN** unrelated Phase 3, Phase 6, Phase 7, Phase 8, or Phase 12 evidence remains in review
- **THEN** the full handoff bundle and refresh reports may still be `review`
- **AND** the access-focused visibility view still reports the MyPrivateAgent access path separately

### Requirement: Phase 17 access-focused visibility remains read-only
The project SHALL keep access-focused handoff visibility read-only and local.

#### Scenario: Access-focused visibility preserves provider boundaries
- **WHEN** the access-focused summary is published
- **THEN** it does not create source-to-agent binding
- **AND** it does not execute a repo-side trial
- **AND** it does not change runtime defaults

### Requirement: Phase 17 access-focused visibility feeds downstream blocker classification
The project SHALL let Phase 14, Phase 15, and Phase 16 classify handoff visibility blockers from the access-focused visibility view rather than from unrelated review-only evidence in the full handoff bundle.

#### Scenario: Access-focused visibility is the blocker source of truth
- **WHEN** Phase 14, Phase 15, or Phase 16 evaluates handoff visibility
- **THEN** it uses the access-focused visibility summary to decide whether the blocker is handoff visibility
- **AND** unrelated review-only evidence outside the MyPrivateAgent access chain does not by itself keep those phases in a handoff visibility blocker state

#### Scenario: Downstream access reports stay conservative
- **WHEN** the access-focused visibility view is not ready
- **THEN** Phase 14, Phase 15, and Phase 16 still report the blocker explicitly
- **AND** they keep the next recommended action obvious
