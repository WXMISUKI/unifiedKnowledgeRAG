## 1. Specification

- [x] 1.1 Create proposal, design, delta specs, and task list for the local usable run-loop.
- [x] 1.2 Validate the OpenSpec change before implementation.

## 2. Implementation

- [x] 2.1 Add a local usable run-loop service that checks local probes, discovery, preflight, retrieve, and answer.
- [x] 2.2 Add a CLI export script with base URL, query, source id, top-k, timeout, and optional API key parameters.
- [x] 2.3 Add focused tests for go, unreachable service, insufficient evidence, and citation allowlist failure.
- [x] 2.4 Update `quickstart.md` and README local run instructions with the run-loop command.

## 3. Verification And Archive

- [x] 3.1 Run focused local run-loop tests.
- [x] 3.2 Run `openspec validate add-local-usable-run-loop --strict`.
- [x] 3.3 Export the local usable run-loop artifact if a local service is reachable, or record why it was not run live.
- [x] 3.4 Run `openspec validate --all --strict`.
- [x] 3.5 Archive the OpenSpec change after specs are synchronized.
