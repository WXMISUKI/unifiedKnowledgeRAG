## 1. Specification

- [x] 1.1 Create proposal, design, delta specs, and task list for the local corpus caller handoff.
- [x] 1.2 Validate the OpenSpec change before implementation.

## 2. Implementation

- [x] 2.1 Add a local corpus caller handoff service that reads a business corpus trial report and exports ready/review/blocked handoff data.
- [x] 2.2 Add a CLI export script with trial report path and output directory parameters.
- [x] 2.3 Add focused tests for go, review, blocked, missing report, and missing artifact pointers.
- [x] 2.4 Update quickstart, README, roadmap, and progress tracker with the caller handoff command.

## 3. Verification And Archive

- [x] 3.1 Run focused caller handoff tests.
- [x] 3.2 Run `openspec validate add-local-corpus-caller-handoff --strict`.
- [x] 3.3 Export the real caller handoff from `docs/local-run/business-corpus-trial/local-business-corpus-trial.json`.
- [x] 3.4 Run `openspec validate --all --strict`.
- [x] 3.5 Archive the OpenSpec change after specs are synchronized.
