# Design

## Fixture Boundary

The exact-term cases live in a dedicated fixture:

```text
tests/fixtures/exact_term_identifier_cases.json
```

The existing baseline benchmark remains unchanged. This keeps historical threshold, chunking, query rewrite, and evidence grading reports comparable.

## Source Anchors

The local fixture source corpus gains explicit exact-term anchors:

| Anchor Type | Example | Source |
| --- | --- | --- |
| policy code | `RFD-2026-003` | refund policy |
| form name | `AF-REFUND-02` | refund policy |
| workflow acronym | `LST-BATCH-OPS` | logistics FAQ |
| order-like id | `ORD-ZS-2026-0007` | logistics FAQ |

These anchors are local test content only. Production identifiers still require customer-specific benchmark data.

## Evidence

Exact-term evidence is exported separately:

```text
docs/benchmark/chinese-seed/exact-term-candidates/exact-term-fixture-baseline.json
docs/benchmark/chinese-seed/exact-term-candidates/exact-term-fixture-baseline.md
```

## Runtime Boundary

This change only adds local fixtures, source anchors, tests, and evidence. It does not add sparse vectors, BM25, hybrid query fusion, reranking, or runtime API behavior.
