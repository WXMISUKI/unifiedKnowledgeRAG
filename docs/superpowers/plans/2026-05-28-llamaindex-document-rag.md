# LlamaIndex Document RAG Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace direct lexical retrieval coupling with a configurable document RAG backend that supports fixture retrieval and LlamaIndex local indexing while preserving the provider HTTP contract.

**Architecture:** Routes continue to depend on provider-owned service functions and Pydantic contracts. A backend factory selects `fixture` or `llamaindex` from configuration, and both backends return the same provider-neutral evidence document model.

**Tech Stack:** Python 3.11 in conda env `GRAPHRAG`, FastAPI, Pydantic v2, pytest, LlamaIndex.

---

### Task 1: Environment and Dependencies

**Files:**
- Create: `requirements.txt`
- Modify: `README.md`

- [ ] **Step 1: Add dependency file**

Create `requirements.txt` with pinned runtime and test dependencies for FastAPI, Pydantic, pytest, httpx, uvicorn, and LlamaIndex packages selected during implementation.

- [ ] **Step 2: Install dependencies**

Run: `conda run -n GRAPHRAG python -m pip install -r requirements.txt`

Expected: installation succeeds.

- [ ] **Step 3: Verify existing tests**

Run: `conda run -n GRAPHRAG python -m pytest tests/test_provider_contract.py -q`

Expected: existing provider contract tests pass before refactoring.

### Task 2: Configuration and Backend Interface

**Files:**
- Create: `app/config.py`
- Create: `app/services/retrieval_backends.py`
- Modify: `app/services/document_retriever.py`
- Test: `tests/test_retrieval_backend_config.py`

- [ ] **Step 1: Write failing backend selection tests**

Test that `RAG_RETRIEVAL_BACKEND=fixture` selects the fixture backend and `RAG_RETRIEVAL_BACKEND=llamaindex` selects the LlamaIndex backend.

- [ ] **Step 2: Implement config model and backend factory**

Add environment-backed settings and a backend factory that returns a provider-owned interface.

- [ ] **Step 3: Run tests**

Run: `conda run -n GRAPHRAG python -m pytest tests/test_retrieval_backend_config.py -q`

Expected: backend selection tests pass.

### Task 3: Fixture Backend Refactor

**Files:**
- Modify: `app/services/document_retriever.py`
- Modify: `app/routers/rag.py`
- Test: `tests/test_provider_contract.py`

- [ ] **Step 1: Move lexical retrieval behind the backend interface**

Keep scoring behavior and citations unchanged.

- [ ] **Step 2: Verify contract compatibility**

Run: `conda run -n GRAPHRAG python -m pytest tests/test_provider_contract.py -q`

Expected: all existing tests pass with the fixture backend.

### Task 4: LlamaIndex Local Backend

**Files:**
- Create: `app/services/llamaindex_retriever.py`
- Create: `app/data/sources/refund_policy_docs.md`
- Create: `app/data/sources/logistics_faq.md`
- Test: `tests/test_llamaindex_retriever.py`

- [ ] **Step 1: Write failing citation preservation test**

Test that a LlamaIndex retrieval result is normalized into `EvidenceDocument` with stable `source_id`, `document_id`, `title`, `snippet`, `score`, and `citation`.

- [ ] **Step 2: Implement local index load/build**

Use configured source documents and provider-owned metadata to build or load a local persisted index.

- [ ] **Step 3: Implement retrieval normalization**

Convert LlamaIndex retrieval nodes into provider contracts without returning framework objects.

- [ ] **Step 4: Run backend tests**

Run: `conda run -n GRAPHRAG python -m pytest tests/test_llamaindex_retriever.py -q`

Expected: LlamaIndex backend tests pass.

### Task 5: Health, Catalog, and Documentation

**Files:**
- Modify: `app/models/contracts.py`
- Modify: `app/routers/health.py`
- Modify: `app/services/source_catalog.py`
- Modify: `README.md`
- Test: `tests/test_provider_contract.py`

- [ ] **Step 1: Add backend readiness fields**

Expose backend name and backend status in health and catalog responses.

- [ ] **Step 2: Add degraded health test**

Test that an unavailable LlamaIndex index reports degraded health with a reason.

- [ ] **Step 3: Update README**

Document `GRAPHRAG`, backend env vars, fixture rollback, and verification commands.

- [ ] **Step 4: Final verification**

Run: `conda run -n GRAPHRAG python -m pytest -q`

Expected: all tests pass.

Run: `openspec validate add-llamaindex-document-rag --strict`

Expected: OpenSpec validation succeeds.
