## ADDED Requirements

### Requirement: Provider includes lightweight container deployment profile

The system SHALL provide a lightweight container deployment profile that can run the provider component without changing runtime capability contracts.

#### Scenario: Container image starts provider API

- **WHEN** the deployment image is built from the provided Dockerfile
- **THEN** it starts `uvicorn app.main:app` on port `8020`

#### Scenario: Compose profile declares component health check

- **WHEN** the compose example is reviewed
- **THEN** it declares a health check against `GET /health`

#### Scenario: Runtime state is mounted, not baked into image

- **WHEN** the container deployment profile is reviewed
- **THEN** source documents, index lifecycle state, and model artifacts are represented as mounted runtime directories rather than copied into the image

#### Scenario: Deployment profile preserves local defaults

- **WHEN** the compose example is used without production overrides
- **THEN** it keeps conservative fixture/mock defaults and does not require Qdrant, BGE-M3 downloads, GraphRAG storage, or external LLM services

#### Scenario: Secrets remain external

- **WHEN** deployment configuration is documented
- **THEN** provider API keys and Qdrant API keys are represented as environment variables and are not committed as concrete secret values
