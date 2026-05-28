# Qdrant BGE-M3 Threshold Recommendation

## Recommendation

| Selected Threshold | Approval Status | Source Sweep |
| ---: | --- | --- |
| 0.7000 | local_seed_recommendation | docs\benchmark\chinese-seed\retrieval-candidates\qdrant-bge-m3-threshold-sweep.json |

## Gates

| Min Hit Rate | Min Citation Match Rate | Min Empty Handling Rate |
| ---: | ---: | ---: |
| 1.0000 | 1.0000 | 1.0000 |

## Selected Metrics

| Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| ---: | ---: | ---: | ---: |
| 21 | 1.0000 | 1.0000 | 1.0000 |

## Caveats

- This recommendation is based on local Chinese seed evidence only.
- It does not change the runtime RAG_SCORE_THRESHOLD default.
- Regenerate the recommendation after adding customer-specific cases or changing chunking.
