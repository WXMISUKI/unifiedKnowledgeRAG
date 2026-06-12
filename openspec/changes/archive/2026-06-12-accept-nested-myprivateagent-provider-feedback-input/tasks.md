## 1. Specification

- [x] 1.1 Create the OpenSpec proposal, design, spec delta, and task list for nested `provider_feedback_input` support.

## 2. Implementation

- [x] 2.1 Normalize Phase 25 trial outcome payloads so nested `provider_feedback_input` is consumed when present.
- [x] 2.2 Preserve the existing flat Phase 25 caller input contract.
- [x] 2.3 Update the caller input contract documentation with the nested compatibility shape.

## 3. Validation And Archive

- [x] 3.1 Add focused tests for nested and flat Phase 25 inputs.
- [x] 3.2 Run focused tests and `openspec validate --all --strict`.
- [x] 3.3 Archive the change.
