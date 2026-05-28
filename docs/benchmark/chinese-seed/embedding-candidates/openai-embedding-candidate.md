# Embedding Candidate Evaluation

## Candidate

| ID | Provider Family | Model | Deployment | Approval Status |
| --- | --- | --- | --- | --- |
| openai-embedding-candidate | hosted | openai-embedding | public-hosted | candidate |

## Enterprise Criteria

| Criterion | Value | Covered |
| --- | --- | --- |
| Language Profile | multilingual | true |
| Chinese-heavy Suitable | true | true |
| Private Network Supported | false | false |
| Vector Dimension | unknown | false |
| Data Residency | public-provider-dependent | true |
| Operational Complexity | low-medium | true |
| Reranker Compatibility | candidate-specific | true |

## Readiness

- Status: review_required

## Decision Notes

- Useful as hosted multilingual quality baseline.
- Public data egress must be explicitly approved before use.
- This evaluation does not approve or invoke the embedding provider.
- Public data egress must be approved before this candidate can be used.
- Vector dimension must be confirmed before Qdrant collection promotion.
