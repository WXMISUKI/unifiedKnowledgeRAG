## 1. Specification

- [x] 1.1 Validate `expand-retrieval-benchmark-cases` with OpenSpec strict mode
- [x] 1.2 Keep expanded cases local and dependency-free

## 2. Benchmark Data

- [x] 2.1 Add category and difficulty metadata to cases
- [x] 2.2 Add policy paraphrase cases
- [x] 2.3 Add evidence/receipt rule cases
- [x] 2.4 Add multi-source and empty retrieval cases
- [x] 2.5 Keep cases compatible with existing fixture backend

## 3. Benchmark Reporting

- [x] 3.1 Extend case dataclass with metadata
- [x] 3.2 Include metadata in per-case results
- [x] 3.3 Add category-level summary metrics
- [x] 3.4 Preserve existing aggregate metrics

## 4. Verification

- [x] 4.1 Add tests for required benchmark categories
- [x] 4.2 Add tests for category summary metrics
- [x] 4.3 Keep existing benchmark tests passing
- [x] 4.4 Run `conda run -n GRAPHRAG python -m pytest -q`
- [x] 4.5 Run `openspec validate expand-retrieval-benchmark-cases --strict`

## 5. Documentation

- [x] 5.1 Document expanded benchmark categories in README
- [x] 5.2 Update production indexing architecture doc with category evidence expectations
