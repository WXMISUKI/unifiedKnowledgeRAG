## 1. Specification

- [x] 1.1 Create proposal, design, delta specs, and task list for the local business corpus trial loop.
- [x] 1.2 Validate the OpenSpec change before implementation.

## 2. Implementation

- [x] 2.1 Add a local business corpus trial service with overlay writing, markdown validation, chunking, retrieval evidence, cited answer checks, and go/review/blocked reporting.
- [x] 2.2 Add a CLI export script with markdown path, source id, title, query, owner/domain/language/sensitivity, top-k, and output directory parameters.
- [x] 2.3 Add focused tests for go, missing markdown, empty markdown, weak evidence review, and citation allowlist failure.
- [x] 2.4 Update quickstart, README, roadmap, and progress tracker with the local business corpus trial command.

## 3. Verification And Archive

- [x] 3.1 Run focused local business corpus trial tests.
- [x] 3.2 Run `openspec validate add-local-business-corpus-trial-loop --strict`.
- [x] 3.3 Export the real `company_profile_2025_trial.md` local business corpus trial artifact, or record why it could not run.
- [x] 3.4 Run `openspec validate --all --strict`.
- [x] 3.5 Archive the OpenSpec change after specs are synchronized.
