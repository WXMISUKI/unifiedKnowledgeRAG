# retrieval-benchmark-harness Specification

## Purpose
Defines local retrieval benchmark cases and metrics used to compare retrieval adapters before production infrastructure choices.

## Requirements
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

### Requirement: Chinese benchmark cases cover enterprise support workflows

The system SHALL include Chinese-heavy benchmark cases that exercise representative enterprise support retrieval patterns before real embedding model approval.

#### Scenario: Enterprise workflow categories are present

- **WHEN** local benchmark cases are loaded
- **THEN** the set includes exception-policy, operational-escalation, SLA, cross-source, paraphrase, evidence, and empty retrieval categories

#### Scenario: Benchmark cases remain citation-bearing

- **WHEN** a non-empty Chinese benchmark case is defined
- **THEN** it includes an expected source id and expected citation tied to a local fixture source

#### Scenario: Empty cases remain business-like

- **WHEN** an empty benchmark case is defined
- **THEN** it represents a plausible enterprise question that is intentionally unsupported by the local fixture sources

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

### Requirement: Retrieval candidates can be evaluated consistently

The system SHALL run the same retrieval benchmark cases against one or more named retrieval candidates.

#### Scenario: Candidate has evaluation metadata

- **WHEN** a retrieval candidate is defined
- **THEN** it includes a stable id, backend, description, and optional metadata for later architecture review

#### Scenario: Multiple candidates are evaluated

- **WHEN** multiple retrieval candidates are evaluated together
- **THEN** each candidate is run against the same benchmark cases and returns its own benchmark report

#### Scenario: Candidate IDs are validated

- **WHEN** candidate evaluation is requested
- **THEN** duplicate or filesystem-unsafe candidate ids are rejected before benchmark execution

### Requirement: Retrieval candidate evidence can be exported

The system SHALL export per-candidate benchmark evidence using stable candidate-based filenames.

#### Scenario: Candidate report files are exported

- **WHEN** candidate evaluation is run with an output directory
- **THEN** each candidate writes `<candidate-id>.json` and `<candidate-id>.md` benchmark reports

#### Scenario: Candidate export remains local

- **WHEN** candidate evaluation exports evidence
- **THEN** it writes local files without exposing a new public HTTP API

### Requirement: Qdrant can be registered as a retrieval candidate

The system SHALL expose Qdrant as an explicit retrieval candidate for benchmark comparison without selecting a production embedding model.

#### Scenario: Qdrant candidate metadata is created

- **WHEN** the Qdrant candidate is requested
- **THEN** candidate metadata identifies Qdrant as the vector store and leaves embedding and reranker choices undecided

#### Scenario: Qdrant candidate remains opt-in

- **WHEN** candidate evaluation is configured
- **THEN** Qdrant is included only when the caller explicitly selects the Qdrant candidate

### Requirement: Embedding candidates can be evaluated consistently

The system SHALL provide a local service-level evaluation shape for embedding candidates without invoking real embedding providers.

#### Scenario: Embedding candidate catalog is loaded

- **WHEN** embedding candidates are requested
- **THEN** the catalog includes the mock baseline and explicit hosted/local Chinese-heavy candidate placeholders

#### Scenario: Embedding candidate ids are validated

- **WHEN** embedding candidate evaluation is requested
- **THEN** duplicate or filesystem-unsafe candidate ids are rejected before exporting evidence

#### Scenario: Embedding candidate evidence is exported

- **WHEN** embedding candidate evaluation is run with an output directory
- **THEN** each candidate writes `<candidate-id>.json` and `<candidate-id>.md` files containing candidate metadata and readiness notes

#### Scenario: Evaluation remains local

- **WHEN** embedding candidate evaluation exports evidence
- **THEN** it writes local files without exposing a new public HTTP API or calling hosted/local embedding services
