## 1. Specification

- [x] 1.1 Create proposal, design, and spec delta for parser-derived insufficient-evidence guard.
- [x] 1.2 Validate the OpenSpec change before implementation.

## 2. Implementation

- [x] 2.1 Locate retrieve/answer document filtering path and add a lightweight parser-derived insufficient-evidence guard.
- [x] 2.2 Keep positive parser-derived company-profile cases answerable.
- [x] 2.3 Ensure expected-empty negative controls return no retrieve documents and no answer citations.

## 3. Verification

- [x] 3.1 Add focused unit tests for the guard and parser-derived quality negative controls.
- [x] 3.2 Run focused pytest for retrieval/quality behavior.
- [x] 3.3 Refresh parser-derived corpus retrieval quality baseline artifacts.
- [x] 3.4 Run `openspec validate --all --strict`.

## 4. Archive

- [x] 4.1 Update roadmap/progress notes with the quality guard result.
- [x] 4.2 Archive the OpenSpec change after implementation and validation.
