# Embedding Candidate Evaluation

## Candidate

| ID | Provider Family | Model | Deployment | Approval Status |
| --- | --- | --- | --- | --- |
| qwen-embedding-candidate | hosted | qwen-embedding | public-hosted-or-private-compatible | candidate |

## Enterprise Criteria

| Criterion | Value | Covered |
| --- | --- | --- |
| Language Profile | chinese-heavy | true |
| Chinese-heavy Suitable | true | true |
| Private Network Supported | false | false |
| Vector Dimension | unknown | false |
| Data Residency | depends-on-provider-and-deployment | true |
| Operational Complexity | medium | true |
| Reranker Compatibility | candidate-specific | true |

## Readiness

- Status: review_required

## Decision Notes

- Hosted/public route must be reviewed for data residency.
- Private-network feasibility remains a later implementation decision.
- This evaluation does not approve or invoke the embedding provider.
- Public data egress must be approved before this candidate can be used.
- Vector dimension must be confirmed before Qdrant collection promotion.
