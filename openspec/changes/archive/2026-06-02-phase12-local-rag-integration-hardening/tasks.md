## 1. Specification

- [x] 1.1 Add short-term local RAG integration hardening goals to `provider-roadmap` requirements.
- [x] 1.2 Add local integration hardening constraints to `knowledge-provider` requirements.

## 2. Documentation and Design

- [x] 2.1 Add `docs/roadmap/open_source_rag_engine_evaluation_roadmap.md` hardening handoff note for local RAG integration precedence.
- [x] 2.2 Add local RAG integration hardening contract:
  - [x] 2.2.1 `docs/integration/myprivateagent-local-rag-integration-hardening/phase12-local-rag-integration-hardening-contract.md`
- [x] 2.3 Add hardening readiness profile export format:
  - [x] 2.3.1 `docs/integration/myprivateagent-local-rag-integration-hardening/phase12-local-rag-integration-hardening-profile.md`
  - [x] 2.3.2 `docs/integration/myprivateagent-local-rag-integration-hardening/phase12-local-rag-integration-hardening-profile.json`
- [x] 2.4 Add hardening decision record:
  - [x] 2.4.1 `docs/integration/myprivateagent-local-rag-integration-hardening/phase12-local-rag-integration-hardening-decision-record.md`

## 3. Evidence and Smoke

- [x] 3.1 Add local hardening profile export helper:
  - [x] 3.1.1 Service + export script (read-only) to aggregate readiness for local integration.
  - [x] 3.1.2 Generate `docs/integration/myprivateagent-local-rag-integration-hardening/phase12-local-rag-integration-hardening-profile.json`.
- [x] 3.2 Add local hardening smoke helper:
  - [x] 3.2.1 Smoke checks: profile present, manifest smoke pass, contract smoke pass, handoff consistency, source-binding preview readiness, retrieval consumption readiness.
  - [x] 3.2.2 Smoke output to:
    - `docs/smoke/myprivateagent-local-rag-integration-hardening/phase12-local-rag-integration-hardening-smoke.json`
    - `docs/smoke/myprivateagent-local-rag-integration-hardening/phase12-local-rag-integration-hardening-smoke.md`
- [x] 3.3 Update handoff refresh pipeline to include hardening status as an optional row.

## 4. Consumption Verification

- [x] 4.1 Add consumption checklist for MyPrivateAgent local URL and API-key mode with deterministic fallback.
- [x] 4.2 Add local hardening verification section to:
  - `docs/operations/myprivateagent-consumption-readiness/`
  - `docs/operations/myprivateagent-local-provider-readiness/`
  (existing docs where this project already tracks cross-phase readiness).

## 5. Documentation Closure

- [x] 5.1 Run focused local-only review by updating the next-step section in:
  - [x] 5.1.1 `docs/progress/provider-improvement-tracker.md`
  - [x] 5.1.2 `openspec/changes/phase12-local-rag-integration-hardening` decision record
- [x] 5.2 Archive this change after explicit review approval.
