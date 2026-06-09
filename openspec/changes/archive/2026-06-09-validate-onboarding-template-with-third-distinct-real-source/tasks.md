## 1. Specification

- [x] 1.1 Create the `validate-onboarding-template-with-third-distinct-real-source` OpenSpec proposal, design, and delta spec with explicit source-selection rules, success signal, and non-goals.

## 2. Implementation

- [x] 2.1 Add a lightweight third distinct real source with the minimum provider visibility needed for local baseline evaluation.
- [x] 2.2 Generate onboarding templates for the new source, fill a minimal real baseline fixture, and export a validation report.
- [x] 2.3 Add focused tests that verify the third distinct source can pass a minimal baseline through the standard evaluation path.

## 3. Validation And Evidence Refresh

- [x] 3.1 Run focused pytest coverage for the third-source validation and related onboarding/catalog tests.
- [x] 3.2 Run `openspec validate --all --strict`, refresh the new source onboarding artifacts, and update roadmap/progress documentation.
