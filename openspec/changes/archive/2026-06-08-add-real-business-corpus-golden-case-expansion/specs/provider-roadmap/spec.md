## ADDED Requirements

### Requirement: Mature RAG work expands real cases before changing strategies
The project SHALL add real business documents or real failed questions to the local golden-case baseline before proposing advanced RAG strategy changes.

#### Scenario: Strategy change requires real-case evidence
- **WHEN** a future change proposes chunking default changes, query rewrite, HyDE, HyPE, rerank, hybrid or fusion retrieval, RAPTOR, Self-RAG, Corrective RAG, or GraphRAG execution
- **THEN** it references aggregate real-business golden-case evidence and identifies the failure modes that justify the strategy

#### Scenario: No failure mode means no advanced strategy work
- **WHEN** aggregate real-business golden-case evidence reports `go` without accepted failures
- **THEN** the next provider work adds more real documents or real user questions rather than promoting advanced retrieval strategies

#### Scenario: Failure mode selects the next gate
- **WHEN** aggregate real-business golden-case evidence reports parser/OCR, chunking, query mismatch, retrieval quality, citation/evidence, provider availability, caller/operator flow, or graph use-case failures
- **THEN** the next OpenSpec change targets that failure class and keeps unrelated advanced techniques out of scope
