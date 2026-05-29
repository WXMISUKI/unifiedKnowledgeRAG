# Design

## Fixture Boundary

The stress cases live in a new fixture file:

```text
tests/fixtures/evidence_grading_stress_cases.json
```

The existing `tests/fixtures/retrieval_benchmark_cases.json` remains the baseline seed for retrieval, threshold, chunking, and query rewrite comparisons.

## Stress Case Types

The first stress fixture targets three labels:

| Label | How it is produced | Purpose |
| --- | --- | --- |
| `related_insufficient` | Expected source is returned but expected citation is intentionally different | Tests strict citation grading versus loose source grading |
| `missing_evidence` | Non-empty expected case points to a valid source/citation but query uses unrelated vocabulary that fixture retrieval cannot match | Tests visible retrieval miss handling |
| `unexpected_evidence` | Expected-empty case uses unsupported intent but overlaps with existing local documents | Tests over-retrieval risk |

## Export Location

Stress evidence is exported separately:

```text
docs/benchmark/chinese-seed/evidence-grading-stress/evidence-grading-candidates.json
docs/benchmark/chinese-seed/evidence-grading-stress/evidence-grading-candidates.md
```

This keeps baseline evidence and stress evidence both available for review.

## Runtime Boundary

This change only adds local benchmark fixtures and evidence. It does not change retrieval defaults, score thresholds, chunking, API behavior, or answer generation.
