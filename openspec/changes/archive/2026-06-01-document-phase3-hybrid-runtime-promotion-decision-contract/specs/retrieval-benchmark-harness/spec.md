## ADDED Requirements

### Requirement: Hybrid runtime promotion SHALL be contract-reviewed against evidence chain completeness

The retrieval benchmark harness documentation SHALL define a contract that maps hybrid runtime promotion decisions to required local evidence artifacts and open-gate handling.

#### Scenario: Contract specifies required hybrid promotion evidence classes

- **WHEN** hybrid runtime promotion is reviewed
- **THEN** the contract references promotion readiness, runtime diagnostics, latency/resource diagnostics, hybrid calibration, cross-case FP/FN smoke, and aggregation/relation negative-control smoke

#### Scenario: Contract keeps candidate evidence from implying automatic promotion

- **WHEN** candidate-level retrieval artifacts show partial wins but production gates remain open
- **THEN** the contract requires `keep_runtime_defaults` until deployed smoke and deployment sign-off gates are explicitly closed
