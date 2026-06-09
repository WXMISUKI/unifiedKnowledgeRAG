## 1. Specification

- [x] 1.1 Create the `add-onboarding-catalog-discovery-bridge` OpenSpec proposal, design, and delta spec with explicit evidence-only discovery boundaries and non-goals.

## 2. Implementation

- [x] 2.1 Add a lightweight source onboarding catalog service that scans onboarding artifact directories and summarizes per-source status.
- [x] 2.2 Add a dedicated export script and generate source onboarding catalog JSON/Markdown artifacts under `docs/local-run/business-rag-golden-cases/`.
- [x] 2.3 Add focused tests covering ready/template-only/missing onboarding states and conservative next-step recommendations.

## 3. Validation And Archive

- [x] 3.1 Run focused pytest coverage for the onboarding catalog bridge and related onboarding/catalog tests.
- [x] 3.2 Run `openspec validate --all --strict`, update roadmap/progress documentation, and archive the change.
