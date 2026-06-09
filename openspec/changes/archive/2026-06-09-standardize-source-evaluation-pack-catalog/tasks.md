## 1. Specification

- [x] 1.1 Create the `standardize-source-evaluation-pack-catalog` OpenSpec proposal, design, and delta spec with explicit provider-level scope and non-goals.

## 2. Implementation

- [x] 2.1 Add a unified source evaluation pack catalog service and exporter that projects existing baseline, failed-question, and confirmation artifacts into a common summary shape.
- [x] 2.2 Add focused tests that verify the catalog summarizes pack type, scope, decision, case count, and recommended next gate conservatively.

## 3. Validation And Evidence Refresh

- [x] 3.1 Run focused pytest coverage for the new catalog and related business-rag evaluation tests.
- [x] 3.2 Run `openspec validate --all --strict`, refresh the catalog artifacts, and update roadmap/progress documentation.
