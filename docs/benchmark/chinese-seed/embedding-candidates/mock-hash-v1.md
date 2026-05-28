# Embedding Candidate Evaluation

## Candidate

| ID | Provider Family | Model | Deployment | Approval Status |
| --- | --- | --- | --- | --- |
| mock-hash-v1 | mock | mock-hash-v1 | local-deterministic-test | baseline |

## Enterprise Criteria

| Criterion | Value | Covered |
| --- | --- | --- |
| Language Profile | contract-only | true |
| Chinese-heavy Suitable | false | false |
| Private Network Supported | true | true |
| Vector Dimension | unknown | false |
| Data Residency | local-only | true |
| Operational Complexity | low | true |
| Reranker Compatibility | not-applicable | true |

## Readiness

- Status: baseline

## Decision Notes

- Deterministic contract baseline only.
- Not a semantic embedding model.
- This evaluation does not approve or invoke the embedding provider.
- Vector dimension must be confirmed before Qdrant collection promotion.
