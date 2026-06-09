## 1. Specification

- [x] 1.1 Create the `bridge-onboarding-catalog-into-pack-catalog` OpenSpec proposal, design, and delta spec with explicit evidence-only bridge boundaries and non-goals.

## 2. Implementation

- [x] 2.1 Update the source evaluation pack catalog service to absorb lightweight summary signals from `source-onboarding-catalog.json` when present.
- [x] 2.2 Refresh the source evaluation pack catalog export so JSON/Markdown artifacts expose onboarding summary without changing pack decision semantics.
- [x] 2.3 Add focused tests covering onboarding-catalog-present and onboarding-catalog-missing behavior.

## 3. Validation And Archive

- [x] 3.1 Run focused pytest coverage for the pack-catalog bridge and related catalog tests.
- [x] 3.2 Run `openspec validate --all --strict`, refresh catalog artifacts, update roadmap/progress docs, and archive the change.
