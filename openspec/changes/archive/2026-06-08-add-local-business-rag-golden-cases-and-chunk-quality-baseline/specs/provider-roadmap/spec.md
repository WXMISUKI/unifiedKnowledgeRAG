## ADDED Requirements

### Requirement: RAG_Techniques adoption proceeds through local quality baselines
The project SHALL convert accepted real business RAG trials into reusable golden-case and chunk-quality baseline evidence before promoting advanced RAG techniques.

#### Scenario: Advanced RAG technique is proposed after the baseline
- **WHEN** a future change proposes query rewrite, HyDE, HyPE, rerank, hybrid or fusion retrieval, RAPTOR, Self-RAG, Corrective RAG, or GraphRAG execution for business RAG maturity
- **THEN** it references local golden-case and chunk-quality baseline evidence or explains which real failure mode is not covered by the current baseline

#### Scenario: Current next-stage work remains lightweight
- **WHEN** the local business RAG golden-case and chunk-quality baseline is exported
- **THEN** it records the current company-profile trial as reusable quality evidence
- **AND** it preserves runtime defaults and provider/caller ownership boundaries

#### Scenario: Baseline result guides next direction
- **WHEN** the local business RAG golden-case and chunk-quality baseline reports `go`, `review`, or `blocked`
- **THEN** the project uses the decision reasons to choose whether to add more real documents, review chunking, review insufficient-evidence behavior, evaluate rerank, evaluate query rewrite, or open a graph use-case gate
