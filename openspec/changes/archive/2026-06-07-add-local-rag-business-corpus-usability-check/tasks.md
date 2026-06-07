## 1. Specification

- [x] 1.1 Create proposal, design, delta spec, and tasks for the lightweight usability check.
- [x] 1.2 Validate the OpenSpec change before implementation.

## 2. Implementation

- [x] 2.1 Add a small usability check service that reuses existing local corpus trial and approved corpus smoke services.
- [x] 2.2 Add a CLI with local-only default and explicit live HTTP option.
- [x] 2.3 Keep outputs compact and write JSON/Markdown only under `docs/local-run/rag-business-corpus-usability`.

## 3. Verification And Archive

- [x] 3.1 Add focused tests for go, review, blocked, live HTTP optional boundary, and CLI exit codes.
- [x] 3.2 Run focused tests.
- [x] 3.3 Run usability CLI in local-only mode.
- [x] 3.4 Run `openspec validate --all --strict`.
- [x] 3.5 Sync canonical spec and archive the OpenSpec change.
