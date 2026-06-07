## 1. Specification

- [x] 1.1 Create proposal, design, and delta specs for the local PDF parser provider bridge.
- [x] 1.2 Validate the OpenSpec change before implementation.

## 2. Implementation

- [x] 2.1 Implement a lightweight PDF parser provider bridge service with injectable HTTP transport and normalized artifact output.
- [x] 2.2 Add a CLI exporter that runs the bridge and writes JSON/Markdown local-run reports.
- [x] 2.3 Reuse the existing parser artifact local ingestion loop as the downstream ingestion step.
- [x] 2.4 Keep provider execution external and preserve non-goals in the generated report.

## 3. Verification

- [x] 3.1 Add focused tests for successful provider normalization, unreachable provider blocking, no-text blocking, and downstream review/blocking behavior.
- [x] 3.2 Run focused pytest coverage for the bridge and related parser artifact loops.
- [x] 3.3 Run `openspec validate --all --strict`.

## 4. Archive

- [x] 4.1 Refresh local run artifacts for the PDF bridge.
- [x] 4.2 Update roadmap/progress notes with the bridge decision and next action.
- [x] 4.3 Archive the OpenSpec change after tasks and validation pass.
