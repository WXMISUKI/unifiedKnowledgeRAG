## 1. Specification

- [x] 1.1 Create proposal, design, delta specs, and tasks for approved local corpus live HTTP smoke.
- [x] 1.2 Validate the OpenSpec change before implementation.

## 2. Implementation

- [x] 2.1 Add a live HTTP smoke service that validates catalog, manifest, retrieve, answer, citations, negative-control behavior, and transport failures.
- [x] 2.2 Add a CLI export script with base URL, source id, top-k, optional case file, output directory, timeout, and provider API key support.
- [x] 2.3 Add focused tests for go, unreachable/HTTP blocked, invalid citation, secret redaction, and review behavior.
- [x] 2.4 Update quickstart, README, roadmap, and progress tracker with the live HTTP command and boundaries.

## 3. Verification And Archive

- [x] 3.1 Run focused live HTTP smoke tests.
- [x] 3.2 Run `openspec validate add-approved-local-corpus-live-http-smoke --strict`.
- [x] 3.3 Export the real `company_profile_2025_trial` live HTTP smoke against `http://127.0.0.1:8020`.
- [x] 3.4 Run `openspec validate --all --strict`.
- [x] 3.5 Archive the OpenSpec change after specs are synchronized.
