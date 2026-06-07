## 1. Specification

- [x] 1.1 Create proposal, design, delta spec, and tasks for the local document source onboarding loop.
- [x] 1.2 Validate the OpenSpec change before implementation.

## 2. Implementation

- [x] 2.1 Add an onboarding orchestration service that chains business corpus trial, caller handoff, approved source registration, and acceptance smoke.
- [x] 2.2 Add a CLI export script with markdown path, source id, title, query, top-k, and output directory options.
- [x] 2.3 Ensure the onboarding summary records per-step artifact paths, final decision, non-goals, and recommended actions.
- [x] 2.4 Update roadmap/local-run documentation with the single command and boundaries.

## 3. Verification And Archive

- [x] 3.1 Add focused tests for go, blocked markdown, blocked registration/handoff propagation, and acceptance review propagation.
- [x] 3.2 Run focused onboarding tests.
- [x] 3.3 Run `openspec validate add-local-document-source-onboarding-loop --strict`.
- [x] 3.4 Run the real company-profile onboarding loop.
- [x] 3.5 Run `openspec validate --all --strict`.
- [x] 3.6 Archive the OpenSpec change after specs are synchronized.
