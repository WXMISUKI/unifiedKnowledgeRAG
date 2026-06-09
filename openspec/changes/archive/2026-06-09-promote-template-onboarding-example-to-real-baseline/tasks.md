## 1. Specification

- [x] 1.1 Create the `promote-template-onboarding-example-to-real-baseline` OpenSpec proposal, design, and delta spec with explicit example-only scope and non-goals.

## 2. Implementation

- [x] 2.1 Add a minimal real markdown source for `source_template_example` and expose it through the existing provider visibility path.
- [x] 2.2 Fill a real baseline fixture, export the onboarding validation report, and refresh onboarding/source-evaluation catalog artifacts.
- [x] 2.3 Add focused tests verifying the promoted example passes a minimal baseline and no longer appears as `template_only`.

## 3. Validation And Archive

- [x] 3.1 Run focused pytest coverage for the promoted template example and related onboarding/catalog tests.
- [x] 3.2 Run `openspec validate --all --strict`, update roadmap/progress documentation, and archive the change.
