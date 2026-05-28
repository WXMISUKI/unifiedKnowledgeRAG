## 1. Specification

- [x] 1.1 Add OpenSpec deltas for Qdrant candidate evaluation
- [x] 1.2 Validate `evaluate-qdrant-vector-store-adapter` with OpenSpec strict mode

## 2. Configuration

- [x] 2.1 Add Qdrant candidate settings
- [x] 2.2 Keep Qdrant disabled unless explicitly selected

## 3. Adapter Model

- [x] 3.1 Add provider-neutral vector evidence chunk model
- [x] 3.2 Add Qdrant point payload mapping
- [x] 3.3 Add source and tenant filter mapping
- [x] 3.4 Preserve citation and enterprise metadata fields

## 4. Candidate Evaluation

- [x] 4.1 Add Qdrant retrieval candidate factory metadata
- [x] 4.2 Ensure candidate metadata does not choose an embedding model by default

## 5. Verification

- [x] 5.1 Add tests for Qdrant settings
- [x] 5.2 Add tests for point payload mapping
- [x] 5.3 Add tests for filter mapping
- [x] 5.4 Add tests for candidate metadata
- [x] 5.5 Run `conda run -n GRAPHRAG python -m pytest -q`

## 6. Documentation

- [x] 6.1 Document local/public and private-network Qdrant evaluation paths
- [x] 6.2 Update production indexing architecture decision with Qdrant as primary candidate
