## ADDED Requirements

### Requirement: Second real business source expansion precedes advanced strategy work
The project SHALL treat second-source aggregate evidence expansion as the next lightweight maturity slice after the first aggregate real-business golden-case baseline.

#### Scenario: Next slice expands real-input breadth first
- **WHEN** the first aggregate real-business golden-case baseline still contains only `company_profile_2025_trial`
- **THEN** the next provider-side maturity slice adds a second real business source or real failed question pack before proposing advanced retrieval strategy changes

#### Scenario: Second-source success does not trigger runtime promotion
- **WHEN** the aggregate baseline passes with a second real business source
- **THEN** the roadmap still classifies chunking, query rewrite, rerank, hybrid retrieval, and GraphRAG as separate evidence-backed gates
- **AND** it does not promote runtime defaults by breadth expansion alone
