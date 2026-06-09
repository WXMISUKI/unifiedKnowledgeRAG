## 1. Specification

- [x] 1.1 Create the `confirm-refund-organization-negative-control-variant` OpenSpec proposal, design, and delta spec with explicit scope, verdict rules, roadmap phase, and non-goals.

## 2. Implementation

- [x] 2.1 Add a dedicated refund organization negative-control confirmation fixture, exporter, and confirmation report on top of the existing aggregate evaluation engine.
- [x] 2.2 Add focused tests that verify the confirmation baseline can distinguish `confirmed_negative_control_variant`, `confirmed_query_mismatch_variant`, and conservative next-gate recommendations.

## 3. Validation And Evidence Refresh

- [x] 3.1 Run focused pytest coverage for the new confirmation baseline and related golden-case tests.
- [x] 3.2 Run `openspec validate --all --strict`, refresh the confirmation artifacts, and update roadmap/progress documentation with the confirmed verdict.
