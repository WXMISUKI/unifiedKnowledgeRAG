## 1. Specification

- [x] 1.1 Create the `add-real-failed-question-pack-baseline` OpenSpec proposal, design, and delta spec with clear failure-driven scope and non-goals.

## 2. Implementation

- [x] 2.1 Extend aggregate case metadata and add a dedicated real failed-question-pack fixture and exporter.
- [x] 2.2 Add focused tests that prove the failed-question pack can independently return `review` while reusing the aggregate evaluation engine.

## 3. Validation And Evidence Refresh

- [x] 3.1 Run focused pytest coverage for the failed-question pack, aggregate golden cases, and related local baseline tests.
- [x] 3.2 Run `openspec validate --all --strict`, refresh the failed-question-pack artifacts, and update roadmap/progress documentation.
