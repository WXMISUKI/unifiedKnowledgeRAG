## ADDED Requirements

### Requirement: Weak lexical overlap does not satisfy negative controls by default
The system SHALL suppress fixture-retriever evidence that only matches weak lexical overlap when real-business local golden cases expect insufficient evidence.

#### Scenario: Weak business-word overlap is filtered for refund-policy negative control
- **WHEN** the fixture retriever evaluates `退款政策里的员工名单有哪些？` against `refund_policy_docs`
- **THEN** weak overlap on generic business terms such as refund/policy wording alone does not produce endorsed evidence
- **AND** the source remains `insufficient_evidence` for that negative control

#### Scenario: Exact-term positive controls remain answerable
- **WHEN** the fixture retriever evaluates exact refund-policy lookups such as `RFD-2026-003 对应哪类退款复核？` or `AF-REFUND-02 表单需要关联哪些付款凭证？`
- **THEN** exact alphanumeric term overlap can still return evidence
- **AND** the existing answerable refund-policy golden cases remain `ready`

#### Scenario: Aggregate baseline returns to go after leakage hardening
- **WHEN** the real-business aggregate baseline is refreshed after negative-control hardening
- **THEN** `refund_policy_docs` no longer records `negative_control_leakage`
- **AND** the aggregate report can return `go` if no other source or chunk-quality review remains
