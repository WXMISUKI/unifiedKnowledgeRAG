# Embedding Candidate Evaluation

## Candidate

| ID | Provider Family | Model | Deployment | Approval Status |
| --- | --- | --- | --- | --- |
| bge-m3-local-candidate | local | bge-m3 | local-or-private-network | candidate |

## Enterprise Criteria

| Criterion | Value | Covered |
| --- | --- | --- |
| Language Profile | chinese-heavy-and-multilingual | true |
| Chinese-heavy Suitable | true | true |
| Private Network Supported | true | true |
| Vector Dimension | 1024 | true |
| Data Residency | private-network-capable | true |
| Operational Complexity | medium-high | true |
| Reranker Compatibility | strong-local-reranker-ecosystem | true |

## Readiness

- Status: review_required

## Decision Notes

- Local route is suitable for private data constraints.
- Dense embedding adapter is available as an opt-in local path.
- Runtime footprint and serving stack still need benchmark evidence.
- This evaluation does not approve or invoke the embedding provider.
