# Knowledge Provider V1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a minimal independent Knowledge Provider v1 with RAG + GraphRAG contracts and a document-RAG-only first implementation slice.

**Architecture:** FastAPI routes expose provider-neutral Pydantic contracts. A static catalog service owns configured knowledge bases and graph namespaces, while a deterministic local retrieval service proves document RAG behavior and can later be replaced behind the same interface.

**Tech Stack:** Python 3.13, FastAPI, Pydantic v2, pytest, FastAPI TestClient.

---

### Task 1: OpenSpec Baseline

**Files:**
- Create: `openspec/changes/add-knowledge-provider-v1/proposal.md`
- Create: `openspec/changes/add-knowledge-provider-v1/design.md`
- Create: `openspec/changes/add-knowledge-provider-v1/specs/knowledge-provider/spec.md`
- Create: `openspec/changes/add-knowledge-provider-v1/specs/document-rag/spec.md`
- Create: `openspec/changes/add-knowledge-provider-v1/tasks.md`

- [ ] **Step 1: Write OpenSpec artifacts**

Create proposal, design, spec deltas, and tasks that define provider health, capabilities, catalog, document RAG retrieve, and graph query boundary behavior.

- [ ] **Step 2: Validate OpenSpec**

Run: `openspec validate add-knowledge-provider-v1 --strict`

Expected: validation succeeds with no missing artifact or scenario format errors.

### Task 2: Contract Tests

**Files:**
- Create: `tests/test_provider_contract.py`

- [ ] **Step 1: Write failing tests**

Add tests for `/health`, `/api/capabilities`, `/api/catalog`, `/api/rag/sources`, successful `/api/rag/retrieve`, empty retrieval, unknown source error, `/api/graph/schemas`, and graph query not implemented.

- [ ] **Step 2: Run tests to verify RED**

Run: `pytest tests/test_provider_contract.py -q`

Expected: tests fail because `app.main` and provider endpoints do not exist yet.

### Task 3: Provider Implementation

**Files:**
- Create: `app/__init__.py`
- Create: `app/main.py`
- Create: `app/models/__init__.py`
- Create: `app/models/contracts.py`
- Create: `app/services/__init__.py`
- Create: `app/services/source_catalog.py`
- Create: `app/services/document_retriever.py`
- Create: `app/routers/__init__.py`
- Create: `app/routers/health.py`
- Create: `app/routers/capabilities.py`
- Create: `app/routers/catalog.py`
- Create: `app/routers/rag.py`
- Create: `app/routers/graph.py`

- [ ] **Step 1: Implement Pydantic contracts**

Define request, result, source metadata, evidence document, graph schema, and error envelope models.

- [ ] **Step 2: Implement catalog and retrieval services**

Add static source metadata and deterministic lexical document retrieval with stable citation values.

- [ ] **Step 3: Implement FastAPI routers**

Wire health, capabilities, catalog, RAG source listing, RAG retrieval, graph schema listing, and graph query structured error behavior.

- [ ] **Step 4: Run tests to verify GREEN**

Run: `pytest tests/test_provider_contract.py -q`

Expected: all tests pass.

### Task 4: Documentation and Verification

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Update README**

Document local run command, pytest command, implemented endpoints, and first-slice limitations.

- [ ] **Step 2: Run final verification**

Run: `pytest tests/test_provider_contract.py -q`

Expected: all tests pass.

Run: `openspec validate add-knowledge-provider-v1 --strict`

Expected: validation succeeds.
