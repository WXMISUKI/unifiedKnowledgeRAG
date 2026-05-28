# Design: export-chinese-seed-evaluation-evidence

## Approach

Extend `app.services.retrieval_benchmark` with a small evidence bundle helper:

- load benchmark cases from `tests/fixtures/retrieval_benchmark_cases.json`
- evaluate a named fixture retrieval baseline
- export retrieval candidate JSON/Markdown evidence
- export embedding candidate JSON/Markdown evidence

The default output directory is caller-provided so tests can use temporary directories and docs can use `docs/benchmark`.

## Output Layout

The helper writes:

- `retrieval-candidates/<candidate-id>.json`
- `retrieval-candidates/<candidate-id>.md`
- `embedding-candidates/<candidate-id>.json`
- `embedding-candidates/<candidate-id>.md`

The initial retrieval candidate is `fixture-chinese-seed-baseline`. It is a contract baseline, not a semantic retrieval quality claim.

## Safety

The helper remains service-only and local-file based. It does not create public APIs, contact networks, start Qdrant, or instantiate real embedding providers.
