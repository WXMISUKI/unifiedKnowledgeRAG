# Design

## Boundary

Evidence grading is implemented as a benchmark/evidence workflow, not as runtime retrieval behavior.

The first implementation remains deterministic and local:

- It reuses existing retrieval benchmark cases.
- It runs retrieval through the selected backend, defaulting to the fixture backend for deterministic evidence.
- It grades each case using returned citations and expected citation/source metadata.
- It exports local JSON and Markdown reports.

## Candidate Model

`EvidenceGradingCandidate` records:

- `id`
- `description`
- `implementation_status`
- `grading_policy`
- `risk_notes`

Initial candidates:

| Candidate | Policy | Purpose |
| --- | --- | --- |
| `citation-match-grader-v1` | `citation_match` | strict local grader: answer-bearing only when expected citation is returned |
| `source-match-grader-v1` | `source_match` | looser local grader: answer-bearing when expected source is returned |

Both are local evidence candidates. Neither is a production answer gate.

## Grading Labels

Per-case grading uses stable labels:

- `answer_bearing`: expected evidence was found according to candidate policy.
- `related_insufficient`: source-level evidence was present but citation-level evidence was not sufficient.
- `missing_evidence`: no acceptable evidence was returned for a non-empty expected case.
- `no_evidence_expected`: expected-empty case returned no documents.
- `unexpected_evidence`: expected-empty case returned documents.

## Metrics

Each candidate result reports:

- total cases
- answer-bearing rate
- related-insufficient count
- missing-evidence count
- unexpected-evidence count
- expected-empty pass rate
- backend benchmark summary
- per-case grading labels and citations

## Runtime Safety

Evidence grading does not:

- call hosted providers
- call local LLMs
- mutate indexes
- filter public API results
- change the retrieval benchmark expectations

Future runtime adoption must reference this evidence and explicitly review false-negative and false-positive risks.
