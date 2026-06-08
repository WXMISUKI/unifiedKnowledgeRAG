## 1. Specification And Fixture

- [x] 1.1 Add a stable local business golden-case fixture for `company_profile_2025_trial`
- [x] 1.2 Define report decision and chunk-quality thresholds in implementation code

## 2. Exporter Implementation

- [x] 2.1 Implement a local exporter that evaluates golden cases and chunk-quality diagnostics
- [x] 2.2 Generate JSON and Markdown evidence under `docs/local-run/business-rag-golden-cases/`

## 3. Verification

- [x] 3.1 Add focused tests for `go`, `review`, and `blocked` report decisions
- [x] 3.2 Run focused pytest and `openspec validate --all --strict`

## 4. Documentation And Closure

- [x] 4.1 Update roadmap/progress documentation with the new baseline output and next-decision rule
- [x] 4.2 Mark tasks complete, archive the OpenSpec change, and keep runtime defaults unchanged
