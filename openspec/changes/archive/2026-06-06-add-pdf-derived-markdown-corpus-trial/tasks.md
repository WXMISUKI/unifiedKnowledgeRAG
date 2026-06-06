## 1. Specification

- [x] 1.1 Create proposal, design, delta specs, and task list for the PDF-derived markdown corpus trial.
- [x] 1.2 Validate the OpenSpec change before implementation.

## 2. Implementation

- [x] 2.1 Add a local PDF-derived markdown trial service with page-range extraction, markdown artifact writing, chunk evidence, and go/review/blocked reporting.
- [x] 2.2 Add a CLI export script with PDF path, source id, query, max pages, output directory, and optional extractor parameters.
- [x] 2.3 Add focused tests for successful markdown trial, missing PDF, unavailable extractor, weak evidence review, and citation allowlist failure.
- [x] 2.4 Update quickstart, README, roadmap, and progress tracker with the local PDF-derived markdown trial path.

## 3. Verification And Archive

- [x] 3.1 Run focused PDF-derived markdown trial tests.
- [x] 3.2 Run `openspec validate add-pdf-derived-markdown-corpus-trial --strict`.
- [x] 3.3 Export the real first-five-page PDF trial artifact for the provided company profile PDF, or record why it could not run.
- [x] 3.4 Run `openspec validate --all --strict`.
- [x] 3.5 Archive the OpenSpec change after specs are synchronized.
