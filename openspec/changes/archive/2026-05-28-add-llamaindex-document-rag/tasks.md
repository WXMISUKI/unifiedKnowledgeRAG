## 1. Specification

- [x] 1.1 Create proposal for `add-llamaindex-document-rag`
- [x] 1.2 Create design for configurable document RAG backend
- [x] 1.3 Modify `document-rag` spec for backend selection and LlamaIndex readiness
- [x] 1.4 Modify `knowledge-provider` spec for backend readiness health/catalog metadata
- [x] 1.5 Validate the OpenSpec change

## 2. Environment

- [x] 2.1 Use the `GRAPHRAG` conda environment for all Python commands
- [x] 2.2 Add project dependency file for FastAPI, pytest, and LlamaIndex packages
- [x] 2.3 Install and verify dependencies in `GRAPHRAG`

## 3. Retrieval Architecture

- [x] 3.1 Add configuration model for retrieval backend and index paths
- [x] 3.2 Extract a document retriever interface
- [x] 3.3 Move current deterministic retriever into a fixture backend
- [x] 3.4 Add LlamaIndex local index backend with provider-owned citation metadata
- [x] 3.5 Preserve the current `/api/rag/retrieve` contract

## 4. Verification

- [x] 4.1 Keep existing provider contract tests passing
- [x] 4.2 Add tests for fixture backend selection
- [x] 4.3 Add tests for LlamaIndex backend citation preservation
- [x] 4.4 Add tests for degraded backend health behavior
- [x] 4.5 Run pytest through `conda run -n GRAPHRAG`

## 5. Documentation

- [x] 5.1 Update README with `GRAPHRAG` environment commands
- [x] 5.2 Document backend configuration and rollback to `fixture`
