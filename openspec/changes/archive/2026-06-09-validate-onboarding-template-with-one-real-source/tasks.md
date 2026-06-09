## 1. Specification

- [x] 1.1 Create the `validate-onboarding-template-with-one-real-source` OpenSpec proposal, design, and delta spec with explicit source-selection rules, success signal, and non-goals.

## 2. Implementation

- [x] 2.1 Add the minimum provider visibility needed for `split_refund_policy_docs` so it can participate in local baseline evaluation without changing runtime strategy defaults.
- [x] 2.2 Generate onboarding templates for `split_refund_policy_docs`, fill a minimal real baseline fixture, and export a validation report.
- [x] 2.3 Add focused tests that verify the new source can pass a minimal baseline through the standard evaluation path.

## 3. Validation And Evidence Refresh

- [x] 3.1 Run focused pytest coverage for the new source validation and related onboarding/catalog tests.
- [x] 3.2 Run `openspec validate --all --strict`, refresh the new source onboarding artifacts, and update roadmap/progress documentation.
