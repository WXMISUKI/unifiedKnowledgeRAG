## MODIFIED Requirements

### Requirement: Retrieval benchmark cases are structured

The system SHALL define local benchmark cases that describe retrieval input, expected evidence outcomes, and evaluation metadata.

#### Scenario: Benchmark case has expected citation

- **WHEN** a benchmark case expects a specific citation
- **THEN** the case includes query, knowledge base ids, top-k, expected source id, expected citation, category, and difficulty

#### Scenario: Benchmark case expects empty retrieval

- **WHEN** a benchmark case expects no matching evidence
- **THEN** the case marks empty retrieval as expected and includes category and difficulty metadata

#### Scenario: Benchmark set covers representative retrieval categories

- **WHEN** local benchmark cases are loaded
- **THEN** the set includes policy, FAQ, evidence, paraphrase, multi-source, and empty retrieval categories

### Requirement: Retrieval benchmark reports comparable metrics

The system SHALL run benchmark cases against a selected retrieval backend and return structured aggregate and category-level metrics.

#### Scenario: Expected evidence is found

- **WHEN** a retrieval backend returns the expected source and citation within top-k
- **THEN** the benchmark case result reports `hit_at_k=true` and `citation_match=true`

#### Scenario: Expected empty retrieval is respected

- **WHEN** a benchmark case expects empty retrieval and the backend returns no documents
- **THEN** the benchmark case result reports `empty_query_handling=true`

#### Scenario: Benchmark summary is reported

- **WHEN** benchmark execution completes
- **THEN** the report includes backend name, total cases, hit rate, citation match rate, empty handling rate, category summaries, and per-case latency
