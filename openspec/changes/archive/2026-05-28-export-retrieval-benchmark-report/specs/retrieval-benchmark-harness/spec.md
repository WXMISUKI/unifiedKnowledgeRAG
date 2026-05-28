## ADDED Requirements

### Requirement: Retrieval benchmark reports can be exported

The system SHALL export retrieval benchmark reports as durable local evidence files.

#### Scenario: JSON report is exported

- **WHEN** a benchmark report is exported as JSON
- **THEN** the output includes summary metrics, category summaries, and per-case results

#### Scenario: Markdown report is exported

- **WHEN** a benchmark report is exported as Markdown
- **THEN** the output includes a human-readable summary table and per-case result table

#### Scenario: Report export remains local

- **WHEN** benchmark report export is used
- **THEN** the system writes local files without exposing a new public HTTP API

## MODIFIED Requirements

### Requirement: Retrieval benchmark reports comparable metrics

The system SHALL run benchmark cases against a selected retrieval backend and return structured aggregate and category-level metrics that can be exported as local evidence.

#### Scenario: Expected evidence is found

- **WHEN** a retrieval backend returns the expected source and citation within top-k
- **THEN** the benchmark case result reports `hit_at_k=true` and `citation_match=true`

#### Scenario: Expected empty retrieval is respected

- **WHEN** a benchmark case expects empty retrieval and the backend returns no documents
- **THEN** the benchmark case result reports `empty_query_handling=true`

#### Scenario: Benchmark summary is reported

- **WHEN** benchmark execution completes
- **THEN** the report includes backend name, total cases, hit rate, citation match rate, empty handling rate, category summaries, and per-case latency
