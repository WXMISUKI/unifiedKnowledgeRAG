## 1. Specification

- [x] 1.1 Create proposal, design, delta specs, and tasks for approved local corpus acceptance smoke.
- [x] 1.2 Validate the OpenSpec change before implementation.

## 2. Implementation

- [x] 2.1 Add an approved local corpus acceptance smoke service with catalog, manifest, retrieve, answer, citation, and negative-control checks.
- [x] 2.2 Add a CLI export script with source id, output directory, and optional case file parameters.
- [x] 2.3 Add focused tests for go, review, blocked missing source, invalid citations, and negative-control behavior.
- [x] 2.4 Update quickstart, README, roadmap, and progress tracker with the acceptance smoke command and boundaries.

## 3. Verification And Archive

- [x] 3.1 Run focused approved local corpus acceptance smoke tests.
- [x] 3.2 Run `openspec validate add-approved-local-corpus-acceptance-smoke --strict`.
- [x] 3.3 Export the real `company_profile_2025_trial` acceptance smoke.
- [x] 3.4 Run `openspec validate --all --strict`.
- [x] 3.5 Archive the OpenSpec change after specs are synchronized.
