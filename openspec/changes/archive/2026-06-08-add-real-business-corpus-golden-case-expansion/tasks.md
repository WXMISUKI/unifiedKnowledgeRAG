## 1. Fixture And Model

- [x] 1.1 Add an aggregate real-business golden-case fixture with source id, failure mode, and risk level fields
- [x] 1.2 Define aggregate report models and conservative decision rules

## 2. Aggregate Exporter

- [x] 2.1 Implement an aggregate exporter that groups cases by source and reuses the existing local business baseline
- [x] 2.2 Generate aggregate JSON and Markdown evidence under `docs/local-run/business-rag-golden-cases/`

## 3. Verification

- [x] 3.1 Add focused tests for aggregate `go`, `review`, and `blocked` paths
- [x] 3.2 Run focused pytest and `openspec validate --all --strict`

## 4. Documentation And Closure

- [x] 4.1 Update roadmap/progress documentation with the aggregate baseline direction
- [x] 4.2 Sync main specs, archive the OpenSpec change, and keep runtime defaults unchanged
