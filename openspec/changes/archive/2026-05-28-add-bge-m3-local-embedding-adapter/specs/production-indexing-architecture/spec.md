## ADDED Requirements

### Requirement: BGE-M3 local embedding adapter remains opt-in

The system SHALL provide BGE-M3 as an explicit local embedding candidate without changing production defaults.

#### Scenario: BGE-M3 local provider is selected

- **WHEN** `EMBEDDING_PROVIDER=bge_m3_local` is configured
- **THEN** the system loads BGE-M3 through a local adapter and emits dense vectors compatible with the configured vector size

#### Scenario: BGE-M3 dependencies are unavailable

- **WHEN** the local BGE-M3 runtime dependency or model files are unavailable
- **THEN** readiness reports degraded instead of falling back silently or switching providers

#### Scenario: Mirror acceleration is configured

- **WHEN** an operator configures a Hugging Face endpoint override for local model download
- **THEN** the adapter uses that endpoint only for the selected local provider and does not hard-code a mirror as the default

#### Scenario: Hybrid retrieval is deferred

- **WHEN** BGE-M3 is used in this change
- **THEN** only dense vectors are produced and sparse, ColBERT, reranker, and hybrid retrieval remain separate decisions
