## ADDED Requirements

### Requirement: Source binding deployed smoke advances Phase 6 integration evidence

The project SHALL treat deployed source binding endpoint smoke as Phase 6 integration and operations evidence when it verifies that live provider binding-review surfaces are reachable without executing retrieval, ingestion, answer composition, or GraphRAG.

#### Scenario: Source binding deployed smoke is phase-aligned

- **WHEN** an OpenSpec change adds `GET /api/provider/source-bindings` to deployed smoke
- **THEN** the roadmap records it as lightweight Phase 6 deployed integration evidence

#### Scenario: Source binding deployed smoke preserves provider boundary

- **WHEN** deployed smoke validates source binding review over HTTP
- **THEN** source-to-agent binding creation, approvals, audit, heartbeat governance, registration, and final answer policy remain outside this provider
