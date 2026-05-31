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
- **THEN** the set includes exception-policy, operational-escalation, SLA, cross-source, paraphrase, evidence, long-section, and empty retrieval categories

#### Scenario: Benchmark cases remain citation-bearing

- **WHEN** a non-empty Chinese benchmark case is defined
- **THEN** it includes an expected source id and expected citation tied to a local fixture source

#### Scenario: Empty cases remain business-like

- **WHEN** an empty benchmark case is defined
- **THEN** it represents a plausible enterprise question that is intentionally unsupported by the local fixture sources

#### Scenario: Empty cases cover unsupported business domains

- **WHEN** local benchmark cases are loaded
- **THEN** expected-empty cases cover multiple unsupported business domains so threshold evidence can expose false-positive retrieval risk

#### Scenario: Long-section cases cover dense procedure details

- **WHEN** local benchmark cases are loaded
- **THEN** long-section cases ask about details embedded inside longer policy or procedure paragraphs

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

#### Scenario: Phase 3 FP/FN review can be exported from benchmark evidence

- **WHEN** a caller exports Phase 3 FP/FN review from an existing benchmark evidence JSON
- **THEN** the system writes local JSON and Markdown files containing false-positive and false-negative counts, rates, and case ids

#### Scenario: FP/FN review export remains local and evaluation-only

- **WHEN** Phase 3 FP/FN review evidence is exported
- **THEN** runtime retrieval defaults, provider HTTP contracts, and production promotion status remain unchanged

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

### Requirement: Chinese seed evidence can be exported as a local bundle

The system SHALL provide a local service-level helper that exports the current Chinese benchmark seed evidence for architecture review.

#### Scenario: Seed evidence bundle is exported

- **WHEN** the Chinese seed evidence export helper is run with an output directory
- **THEN** it writes retrieval candidate evidence and embedding candidate evidence under stable subdirectories

#### Scenario: Retrieval seed baseline is exported

- **WHEN** the seed evidence bundle exports retrieval evidence
- **THEN** it includes a fixture baseline candidate evaluated against the current Chinese benchmark cases

#### Scenario: Embedding candidate seed evidence is exported

- **WHEN** the seed evidence bundle exports embedding evidence
- **THEN** it includes local metadata reports for the default embedding candidate catalog without invoking hosted or local embedding services

#### Scenario: Seed bundle remains local

- **WHEN** the seed evidence bundle is exported
- **THEN** it writes local JSON and Markdown files without exposing a public HTTP API

### Requirement: Qdrant smoke evidence can be exported locally

The system SHALL provide a local helper that runs a Qdrant ingestion-and-retrieval smoke flow and exports durable evidence files, including the configured retrieval score threshold used by the run and the business citations emitted by Qdrant ingestion.

#### Scenario: Qdrant smoke evidence is exported

- **WHEN** the Qdrant smoke helper is run with source ids, benchmark cases, and an output directory
- **THEN** it indexes the sources, queries the cases, and writes JSON and Markdown evidence files

#### Scenario: Smoke evidence includes runtime metadata

- **WHEN** the Qdrant smoke helper exports evidence
- **THEN** the output includes Qdrant collection/vector metadata, embedding provider/model metadata, indexed source ids, generated ingestion job ids, and the configured retrieval score threshold

#### Scenario: Smoke evidence reports business citations

- **WHEN** Qdrant ingestion emits business citation anchors for indexed chunks
- **THEN** smoke evidence case results include those citations in `returned_citations`

#### Scenario: Smoke helper remains local

- **WHEN** Qdrant smoke evidence is exported
- **THEN** the system writes local files without exposing a public HTTP API

### Requirement: Qdrant smoke uses one client per run

The system SHALL use one Qdrant client instance for both source ingestion and retrieval within a single smoke run.

#### Scenario: In-memory Qdrant is used

- **WHEN** the Qdrant smoke helper is configured with an in-memory Qdrant URL
- **THEN** source ingestion and retrieval use the same client so indexed chunks are queryable during the same run

#### Scenario: Smoke run reports actual retrieval misses

- **WHEN** indexed Qdrant retrieval returns citations that differ from expected benchmark citations
- **THEN** the evidence report records the miss rather than rewriting expected outcomes

### Requirement: Qdrant smoke threshold sweep evidence can be exported locally

The system SHALL provide a local helper that runs Qdrant+BGE smoke evidence across explicit score thresholds and exports comparable threshold-level evidence.

#### Scenario: Threshold sweep evidence is exported

- **WHEN** the threshold sweep helper is run with source ids, benchmark cases, thresholds, and an output directory
- **THEN** it writes JSON and Markdown evidence files that include one Qdrant smoke benchmark report per threshold

#### Scenario: Threshold sweep includes comparable metrics

- **WHEN** threshold sweep evidence is exported
- **THEN** the output includes each threshold value, hit rate, citation match rate, empty handling rate, total cases, and embedding/vector metadata

#### Scenario: Threshold sweep remains local

- **WHEN** threshold sweep evidence is exported
- **THEN** the system writes local files without exposing a public HTTP API or changing the default retrieval threshold

#### Scenario: Threshold sweep rejects invalid thresholds

- **WHEN** a threshold sweep is requested with duplicate or out-of-range thresholds
- **THEN** the request is rejected before running Qdrant ingestion or retrieval

### Requirement: Qdrant threshold recommendation evidence can be exported locally

The system SHALL derive a local Qdrant+BGE threshold recommendation from threshold sweep evidence without changing runtime defaults.

#### Scenario: Threshold recommendation is exported

- **WHEN** a threshold sweep report and quality gates are provided
- **THEN** the system writes JSON and Markdown recommendation files with the selected threshold, gates, source sweep path, metrics, and caveats

#### Scenario: Lowest passing threshold is selected

- **WHEN** multiple threshold sweep rows satisfy the configured quality gates
- **THEN** the recommendation selects the lowest passing threshold

#### Scenario: No threshold satisfies the gates

- **WHEN** no threshold sweep row satisfies the configured quality gates
- **THEN** recommendation generation fails with a clear error and does not write a misleading recommendation

#### Scenario: Recommendation does not change defaults

- **WHEN** threshold recommendation evidence is exported
- **THEN** the runtime `RAG_SCORE_THRESHOLD` default remains unchanged and the recommendation is marked as local seed evidence only

### Requirement: Chunking strategy candidates can be evaluated locally

The system SHALL export local evidence for chunking strategy candidates without changing runtime ingestion behavior.

#### Scenario: Chunking candidate evidence is exported

- **WHEN** chunking strategy evaluation is run with source ids and an output directory
- **THEN** the system writes JSON and Markdown evidence with one result per candidate strategy

#### Scenario: Implemented strategy reports source metrics

- **WHEN** an implemented chunking strategy is evaluated
- **THEN** the evidence includes source ids, chunk counts, citation stability, chunking strategy id, and implementation status

#### Scenario: Runnable section strategy reports source metrics

- **WHEN** `markdown-section-v1` is evaluated
- **THEN** the evidence reports section chunk counts, citation stability, source ids, and runnable implementation status without changing ingestion defaults

#### Scenario: Runnable token-window strategy reports source metrics

- **WHEN** `token-window-v1` is evaluated
- **THEN** the evidence reports token-window chunk counts, citation stability, source ids, and runnable implementation status without changing ingestion defaults

#### Scenario: Evaluation does not change ingestion defaults

- **WHEN** chunking strategy evidence is exported
- **THEN** runtime Qdrant ingestion continues using the configured baseline strategy

### Requirement: Qdrant chunking strategies can be compared with smoke evidence

The system SHALL export local Qdrant+BGE smoke comparison evidence for selected chunking strategies without changing runtime ingestion defaults.

#### Scenario: Chunking comparison evidence is exported

- **WHEN** chunking comparison is run with source ids, benchmark cases, chunking strategy ids, and an output directory
- **THEN** the system writes JSON and Markdown evidence with one Qdrant smoke report per strategy

#### Scenario: Comparison preserves benchmark expectations

- **WHEN** a chunking strategy returns citations that differ from expected benchmark citations
- **THEN** the comparison records lower citation match instead of rewriting expected citations

#### Scenario: Comparison includes strategy-level metrics

- **WHEN** chunking comparison evidence is exported
- **THEN** the output includes each strategy id, chunk count, hit rate, citation match rate, empty handling rate, and long-section category metrics

#### Scenario: Token-window strategy participates in comparison

- **WHEN** chunking comparison uses `token-window-v1`
- **THEN** the comparison indexes token-window chunks and includes their strategy-level metrics

#### Scenario: Comparison remains local

- **WHEN** chunking comparison evidence is exported
- **THEN** runtime Qdrant ingestion defaults and public HTTP APIs remain unchanged

### Requirement: Query rewrite candidates can be evaluated locally

The system SHALL evaluate query rewrite candidates against local retrieval benchmark cases without changing runtime retrieval behavior.

#### Scenario: Query rewrite candidate evidence is exported

- **WHEN** query rewrite candidate evaluation is run with benchmark cases and an output directory
- **THEN** the system writes JSON and Markdown evidence with one result per candidate

#### Scenario: Original and rewritten queries are retained

- **WHEN** a candidate rewrites a benchmark query
- **THEN** the evidence records the original query, rewritten query, rewrite flag, and benchmark outcome

#### Scenario: Expected-empty cases are protected

- **WHEN** a benchmark case expects empty retrieval
- **THEN** deterministic rewrite candidates avoid rewriting it unless a future approved change explicitly evaluates that risk

#### Scenario: Rewrite metrics are reported

- **WHEN** query rewrite evidence is exported
- **THEN** the output includes total cases, rewritten case count, rewrite rate, expected-empty rewrite count, hit rate, citation match rate, and empty handling rate

#### Scenario: Query rewrite remains local

- **WHEN** query rewrite candidate evidence is exported
- **THEN** runtime retrieval defaults and public HTTP APIs remain unchanged

### Requirement: Evidence grading candidates can be evaluated locally

The system SHALL evaluate evidence grading candidates against local retrieval benchmark results without changing runtime retrieval or answer generation behavior.

#### Scenario: Evidence grading candidate evidence is exported

- **WHEN** evidence grading candidate evaluation is run with benchmark cases and an output directory
- **THEN** the system writes JSON and Markdown evidence with one result per candidate

#### Scenario: Retrieved evidence is graded per case

- **WHEN** a benchmark case is evaluated by an evidence grading candidate
- **THEN** the evidence records the case id, expected source id, expected citation, returned source ids, returned citations, grading label, and grading reason

#### Scenario: Expected-empty cases are protected

- **WHEN** a benchmark case expects empty retrieval
- **THEN** the grading evidence distinguishes `no_evidence_expected` from `unexpected_evidence`

#### Scenario: Evidence grading metrics are reported

- **WHEN** evidence grading evidence is exported
- **THEN** the output includes total cases, answer-bearing rate, related-insufficient count, missing-evidence count, unexpected-evidence count, and expected-empty pass rate

#### Scenario: Evidence grading remains local

- **WHEN** evidence grading candidate evidence is exported
- **THEN** runtime retrieval defaults, answer generation behavior, and public HTTP APIs remain unchanged

### Requirement: Evidence grading stress cases are maintained separately

The system SHALL maintain dedicated evidence grading stress cases that expose insufficient, missing, and unexpected evidence outcomes without replacing the baseline Chinese retrieval seed.

#### Scenario: Stress fixture is loaded separately

- **WHEN** evidence grading stress cases are evaluated
- **THEN** the cases are loaded from a dedicated fixture rather than modifying the baseline retrieval benchmark fixture

#### Scenario: Stress cases include related but insufficient evidence

- **WHEN** the stress fixture is evaluated by a strict citation grader
- **THEN** at least one case produces `related_insufficient`

#### Scenario: Stress cases include missing evidence

- **WHEN** the stress fixture is evaluated by an evidence grader
- **THEN** at least one non-empty expected case produces `missing_evidence`

#### Scenario: Stress cases include unexpected evidence

- **WHEN** the stress fixture is evaluated by an evidence grader
- **THEN** at least one expected-empty case produces `unexpected_evidence`

#### Scenario: Stress evidence remains local

- **WHEN** stress evidence is exported
- **THEN** runtime retrieval defaults, answer generation behavior, and public HTTP APIs remain unchanged

### Requirement: Exact-term identifier cases are maintained separately

The system SHALL maintain dedicated exact-term and identifier-heavy benchmark cases without replacing the baseline Chinese retrieval seed.

#### Scenario: Exact-term fixture is loaded separately

- **WHEN** exact-term identifier cases are evaluated
- **THEN** the cases are loaded from a dedicated fixture rather than modifying the baseline retrieval benchmark fixture

#### Scenario: Exact-term categories are represented

- **WHEN** exact-term identifier cases are loaded
- **THEN** the set includes policy code, form name, workflow acronym, and order-like id categories

#### Scenario: Exact-term evidence is exported

- **WHEN** exact-term identifier evidence is exported
- **THEN** the system writes local JSON and Markdown reports with benchmark metrics and per-case citations

#### Scenario: Exact-term Qdrant dense evidence is exported

- **WHEN** exact-term identifier cases are evaluated against Qdrant+BGE dense retrieval
- **THEN** the system writes local JSON and Markdown evidence that includes Qdrant metadata, indexed sources, returned citations, and benchmark metrics

#### Scenario: Exact-term evidence remains local

- **WHEN** exact-term identifier evidence is exported
- **THEN** runtime retrieval defaults, answer generation behavior, and public HTTP APIs remain unchanged

### Requirement: Qdrant exact-term smoke evidence can be exported locally

The system SHALL provide a named local export path for running the exact-term identifier fixture through Qdrant+BGE smoke retrieval without changing runtime defaults.

#### Scenario: Exact-term Qdrant smoke evidence is exported

- **WHEN** the exact-term Qdrant smoke helper is run with source ids and an output directory
- **THEN** it indexes the sources, evaluates the exact-term identifier fixture, and writes JSON and Markdown evidence files with stable exact-term filenames

#### Scenario: Exact-term Qdrant smoke keeps expected citations

- **WHEN** dense-only retrieval returns citations that differ from the exact-term fixture expectations
- **THEN** the evidence records the miss instead of rewriting expected citations

#### Scenario: Exact-term Qdrant smoke remains evaluation-only

- **WHEN** exact-term Qdrant smoke evidence is exported
- **THEN** runtime retrieval defaults, public HTTP APIs, and hybrid retrieval decisions remain unchanged

### Requirement: Qdrant hybrid exact-term smoke evidence can be exported locally

The system SHALL provide a named local export path for evaluating exact-term identifier cases against an evaluation-only Qdrant dense+sparse hybrid candidate.

#### Scenario: Hybrid exact-term smoke evidence is exported

- **WHEN** the hybrid exact-term smoke helper is run with source ids and an output directory
- **THEN** it indexes dense and sparse vectors, evaluates the exact-term identifier fixture, and writes JSON and Markdown evidence files with stable hybrid filenames

#### Scenario: Hybrid evidence includes vector strategy metadata

- **WHEN** hybrid exact-term evidence is exported
- **THEN** the output includes dense vector name, sparse vector name, fusion strategy, sparse vectorizer id, indexed sources, returned citations, and benchmark metrics

#### Scenario: Hybrid evidence remains evaluation-only

- **WHEN** hybrid exact-term evidence is exported
- **THEN** runtime retrieval defaults, public HTTP APIs, and production indexing dependencies remain unchanged

#### Scenario: Hybrid evidence records misses honestly

- **WHEN** dense+sparse retrieval returns citations that differ from exact-term fixture expectations
- **THEN** the evidence records the miss instead of rewriting expected citations

#### Scenario: Hybrid exact-term success requires empty-stress follow-up

- **WHEN** hybrid exact-term evidence improves identifier recall
- **THEN** the benchmark harness can export a separate expected-empty stress report before runtime hybrid promotion is considered

### Requirement: Hybrid empty-stress cases are maintained separately

The system SHALL maintain dedicated hybrid empty-stress benchmark cases that expose sparse-token false-positive risk without replacing the baseline Chinese retrieval seed or exact-term fixture.

#### Scenario: Hybrid empty-stress fixture is loaded separately

- **WHEN** hybrid empty-stress cases are evaluated
- **THEN** the cases are loaded from a dedicated fixture rather than modifying the baseline retrieval benchmark fixture or exact-term fixture

#### Scenario: Hybrid empty-stress cases use unsupported token overlap

- **WHEN** hybrid empty-stress cases are loaded
- **THEN** each case expects empty retrieval while sharing lexical structure with known policy codes, form names, workflow acronyms, or order-like ids

### Requirement: Qdrant hybrid empty-stress evidence can be exported locally

The system SHALL provide a named local export path for evaluating expected-empty stress cases against the evaluation-only Qdrant dense+sparse hybrid candidate.

#### Scenario: Hybrid empty-stress evidence is exported

- **WHEN** the hybrid empty-stress helper is run with source ids and an output directory
- **THEN** it indexes dense and sparse vectors, evaluates the hybrid empty-stress fixture, and writes JSON and Markdown evidence files with stable empty-stress filenames

#### Scenario: Hybrid empty-stress evidence records false positives

- **WHEN** hybrid retrieval returns evidence for an expected-empty case
- **THEN** the evidence records `empty_query_handling=false`, preserves the returned citations, and can be used as input for later hybrid gating candidate evaluation

#### Scenario: Hybrid empty-stress evidence remains evaluation-only

- **WHEN** hybrid empty-stress evidence is exported
- **THEN** runtime retrieval defaults, public HTTP APIs, and production indexing dependencies remain unchanged

### Requirement: Hybrid gating candidates can be evaluated locally

The system SHALL provide a local export path for evaluating hybrid retrieval gating candidates against both exact-term recall cases and hybrid expected-empty stress cases without changing runtime retrieval behavior.

#### Scenario: Hybrid gating evidence is exported

- **WHEN** the hybrid gating helper is run with exact-term cases, empty-stress cases, source ids, and an output directory
- **THEN** it indexes dense and sparse vectors, runs hybrid retrieval, applies the gating candidate, and writes JSON and Markdown evidence files

#### Scenario: Raw and gated citations are retained

- **WHEN** a hybrid gating candidate filters retrieved evidence
- **THEN** the evidence records both raw hybrid returned citations and gated returned citations per case

#### Scenario: Identifier gate protects unsupported exact tokens

- **WHEN** a query contains identifier-like tokens and the retrieved evidence does not contain every query identifier as an exact extracted identifier
- **THEN** the exact identifier containment gate removes that evidence before benchmark metrics are calculated

#### Scenario: Hybrid gating remains evaluation-only

- **WHEN** hybrid or noisy identifier gating evidence is exported
- **THEN** runtime retrieval defaults, public HTTP APIs, production sparse-vector dependencies, production alias dictionaries, and answer generation behavior remain unchanged

### Requirement: Expanded hybrid gating fixtures are maintained separately

The system SHALL maintain expanded hybrid gating benchmark fixtures that cover both supported and expected-empty identifier-heavy cases without replacing the baseline Chinese seed, exact-term fixture, or first hybrid empty-stress fixture.

#### Scenario: Expanded positive fixture is loaded separately

- **WHEN** expanded hybrid gating positive cases are evaluated
- **THEN** the cases are loaded from a dedicated fixture rather than modifying the baseline exact-term fixture

#### Scenario: Expanded empty fixture is loaded separately

- **WHEN** expanded hybrid gating expected-empty cases are evaluated
- **THEN** the cases are loaded from a dedicated fixture rather than modifying the first hybrid empty-stress fixture

#### Scenario: Expanded fixtures cover partial identifiers

- **WHEN** expanded hybrid gating expected-empty cases are loaded
- **THEN** at least one case uses a partial identifier that must not be accepted as evidence for a longer known identifier

#### Scenario: Expanded fixtures cover multi-identifier positives

- **WHEN** expanded hybrid gating positive cases are loaded
- **THEN** at least one case requires a single evidence chunk to contain multiple query identifiers

### Requirement: Noisy identifier gate candidates can be evaluated locally

The system SHALL provide a local export path for evaluating noisy or alias-aware identifier gating candidates without changing runtime retrieval behavior.

#### Scenario: Noisy identifier gate evidence is exported

- **WHEN** the noisy identifier gate helper is run with supported and expected-empty noisy identifier cases
- **THEN** it runs hybrid retrieval, applies the alias-aware gating candidate, and writes JSON and Markdown evidence files

#### Scenario: Canonical identifiers are retained

- **WHEN** an alias-aware gate normalizes query identifiers
- **THEN** the evidence records the resulting query identifiers, raw hybrid citations, and gated citations per case

#### Scenario: Noisy gate remains evaluation-only

- **WHEN** noisy identifier gate evidence or alias governance evidence is exported
- **THEN** runtime retrieval defaults, public HTTP APIs, production alias dictionaries, and production indexing dependencies remain unchanged

### Requirement: Noisy identifier fixtures are maintained separately

The system SHALL maintain noisy and alias-heavy identifier benchmark fixtures without replacing the baseline Chinese seed or clean identifier fixtures.

#### Scenario: Noisy positive fixture is loaded separately

- **WHEN** noisy identifier positive cases are evaluated
- **THEN** the cases are loaded from a dedicated fixture rather than modifying clean identifier fixtures

#### Scenario: Noisy empty fixture is loaded separately

- **WHEN** noisy identifier expected-empty cases are evaluated
- **THEN** the cases are loaded from a dedicated fixture rather than modifying clean empty-stress fixtures

#### Scenario: Noisy fixtures cover OCR and shorthand

- **WHEN** noisy identifier fixtures are loaded
- **THEN** they include cases with OCR-like digit confusion and local shorthand aliases

### Requirement: Identifier alias governance can be evaluated locally

The system SHALL provide local evidence for identifier alias governance without creating a production alias service.

#### Scenario: Alias governance evidence is exported

- **WHEN** the alias governance export helper is run with a local catalog
- **THEN** it writes JSON and Markdown evidence with alias ids, canonical identifiers, owners, versions, statuses, risk levels, and decision notes

#### Scenario: Alias catalog is auditable

- **WHEN** aliases are used for noisy identifier candidate evaluation
- **THEN** each alias pattern is represented in the local catalog with owner and status metadata

#### Scenario: Alias governance remains evaluation-only

- **WHEN** alias governance evidence is exported
- **THEN** runtime retrieval defaults, public HTTP APIs, and production alias dictionaries remain unchanged

### Requirement: Split-chunk identifier cases are maintained separately

The system SHALL maintain split-chunk identifier benchmark cases that expose false-negative risk when related identifiers are not co-located in the same evidence chunk.

#### Scenario: Split-chunk source is indexed separately

- **WHEN** split-chunk benchmark evidence is exported
- **THEN** the system indexes a dedicated fixture source rather than modifying the baseline refund or logistics sources

#### Scenario: Split-chunk miss is recorded honestly

- **WHEN** strict identifier gating removes all retrieved chunks because no single chunk contains every query identifier
- **THEN** the evidence records the miss instead of rewriting expected citations

#### Scenario: Split-chunk benchmark remains evaluation-only

- **WHEN** split-chunk evidence is exported
- **THEN** runtime chunking defaults, public HTTP APIs, and production retrieval behavior remain unchanged

### Requirement: Multi-chunk aggregation candidates can be evaluated locally

The system SHALL provide an evaluation-only path for measuring whether hybrid retrieval evidence can satisfy identifier coverage across multiple retrieved chunks from the same source document.

#### Scenario: Multi-chunk aggregation evidence is exported

- **WHEN** the multi-chunk aggregation helper runs with split-chunk identifier cases
- **THEN** it runs hybrid retrieval, groups raw evidence chunks by source document, applies identifier coverage over each group, and writes JSON and Markdown evidence files

#### Scenario: Split identifiers can be recovered across chunks

- **WHEN** a query contains multiple identifier-like tokens and raw hybrid retrieval returns those identifiers in separate chunks from the same source document
- **THEN** the aggregation candidate can retain the grouped evidence instead of requiring every identifier to appear in one chunk

#### Scenario: Aggregation evidence preserves raw diagnostics

- **WHEN** multi-chunk aggregation evidence is exported
- **THEN** the evidence includes query identifiers, raw returned citations, raw source ids, aggregated returned citations, and benchmark summary metrics

#### Scenario: Multi-chunk aggregation remains evaluation-only

- **WHEN** multi-chunk aggregation evidence is exported
- **THEN** runtime retrieval defaults, public HTTP APIs, production parent-document stores, production rerankers, graph stores, and answer generation behavior remain unchanged

### Requirement: Multi-chunk aggregation negative controls are maintained separately

The system SHALL maintain expected-empty negative-control benchmark cases for multi-chunk aggregation without replacing split-chunk positive fixtures.

#### Scenario: Same-document negative controls are loaded separately

- **WHEN** multi-chunk aggregation negative controls are evaluated
- **THEN** the cases are loaded from a dedicated fixture rather than modifying split-chunk positive cases

#### Scenario: Unsupported same-document relationship is expected empty

- **WHEN** a negative-control query asks for an unsupported relationship between identifiers that can appear in the same source document
- **THEN** the benchmark case marks `expect_empty=true` and has no expected citation

### Requirement: Multi-chunk aggregation evidence reports negative-control behavior

The system SHALL include expected-empty negative controls in multi-chunk aggregation evidence so reviewers can see both split-chunk recovery and over-broad grouping risk.

#### Scenario: Aggregation report includes positive and negative cases

- **WHEN** multi-chunk aggregation evidence is exported with positive and negative-control fixtures
- **THEN** the report summary includes hit rate, citation match rate, and empty handling rate across both fixture groups

#### Scenario: Over-broad aggregation is recorded honestly

- **WHEN** multi-chunk aggregation returns evidence for an expected-empty same-document negative control
- **THEN** the report records empty handling failure instead of hiding or rewriting the returned citations

#### Scenario: Negative-control evidence remains evaluation-only

- **WHEN** negative-control evidence is exported
- **THEN** runtime retrieval defaults, public HTTP APIs, production parent-document stores, production rerankers, graph stores, and answer generation behavior remain unchanged

### Requirement: Relation-aware aggregation grading can be evaluated locally

The system SHALL provide an evaluation-only relation-aware grading path for multi-chunk aggregation evidence.

#### Scenario: Relation grading evidence is exported

- **WHEN** relation-aware aggregation grading is exported
- **THEN** the system evaluates multi-chunk aggregation case results and writes JSON and Markdown evidence files

#### Scenario: Positive split-chunk recovery remains answer-bearing

- **WHEN** a non-empty split-chunk case returns the expected citation
- **THEN** the relation-aware grader labels it as answer-bearing

#### Scenario: Unsupported relationship is labeled separately

- **WHEN** an expected-empty query asks for an unsupported relationship and aggregation returns citation-bearing evidence
- **THEN** the relation-aware grader labels the case as relation-unsupported rather than answer-bearing

#### Scenario: Relation grading remains evaluation-only

- **WHEN** relation-aware grading evidence is exported
- **THEN** runtime retrieval defaults, public HTTP APIs, answer generation behavior, production rerankers, graph stores, and LLM graders remain unchanged

### Requirement: Phase 3 benchmark fixtures include customer-like gate cases

The system SHALL maintain a lightweight customer-like fixture extension for retrieval benchmark evaluation so Phase 3 promotion reviews can inspect false-positive and false-negative behavior beyond baseline seed phrasing.

#### Scenario: Customer-like fixture includes false-negative review cases

- **WHEN** benchmark cases are loaded from the canonical retrieval benchmark fixture
- **THEN** customer-like additions include at least one non-empty case that targets false-negative risk in refund/logistics support workflows

#### Scenario: Customer-like fixture includes false-positive review cases

- **WHEN** benchmark cases are loaded from the canonical retrieval benchmark fixture
- **THEN** customer-like additions include at least one expected-empty case that targets lexical-overlap false-positive risk in refund/logistics support workflows

### Requirement: Seed evidence exports stay synchronized with canonical fixture revisions

The system SHALL regenerate Chinese-seed benchmark evidence after canonical fixture updates so review artifacts reflect the current case set and category summaries.

#### Scenario: Chinese-seed evidence reflects current baseline case count

- **WHEN** the Chinese-seed evidence export runs after fixture expansion
- **THEN** the exported retrieval baseline summary reflects the updated total baseline case count and category summaries

#### Scenario: Seed evidence refresh remains evaluation-only

- **WHEN** Chinese-seed evidence is regenerated
- **THEN** runtime retrieval defaults and production promotion gates remain unchanged unless separate gate evidence explicitly approves promotion

