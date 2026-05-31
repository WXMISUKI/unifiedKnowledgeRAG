## MODIFIED Requirements

### Requirement: Deployed provider smoke evidence is exportable

The system SHALL provide a read-only deployed provider smoke probe that validates an already-running provider component over HTTP using a configured base URL and optional provider API credentials.

#### Scenario: Deployed smoke calls required discovery endpoints

- **WHEN** a caller runs the deployed provider smoke export against a running provider base URL
- **THEN** the probe calls `GET /health`, `GET /api/provider/manifest`, `GET /api/provider/preflight`, `GET /api/provider/source-bindings`, and `GET /api/provider/handoff`

#### Scenario: Deployed smoke validates source binding review

- **WHEN** the deployed source binding summary endpoint returns `status=ready` or `status=review`
- **THEN** the smoke report marks the source binding check as passing and summarizes source count and bindable source count

#### Scenario: Deployed smoke blocks invalid source binding evidence

- **WHEN** the deployed source binding summary endpoint is unreachable, returns non-200, returns invalid JSON, or reports `status=blocked`
- **THEN** the smoke report marks the source binding check as `blocked` and the overall smoke status as `blocked`

#### Scenario: Deployed smoke writes evidence artifacts

- **WHEN** the deployed provider smoke export completes
- **THEN** it writes machine-readable JSON and human-readable Markdown under the deployed provider smoke evidence directory

#### Scenario: Deployed smoke supports provider API credentials

- **WHEN** a provider API key is supplied
- **THEN** protected `/api/*` smoke requests include accepted provider API key headers and the secret value is not written to the evidence report

#### Scenario: Deployed smoke remains read-only

- **WHEN** the deployed provider smoke probe runs
- **THEN** it does not execute retrieval, answer composition, ingestion jobs, index rebuilds, embedding models, vector databases, model downloads, graph queries, provider registration, heartbeat governance, audit policy, source-to-agent binding, or final answer policy
