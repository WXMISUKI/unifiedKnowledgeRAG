## 1. Specification

- [x] 1.1 Validate `export-retrieval-benchmark-report` with OpenSpec strict mode
- [x] 1.2 Keep report export local and dependency-free

## 2. Report Serialization

- [x] 2.1 Add JSON-serializable report conversion
- [x] 2.2 Add Markdown report rendering
- [x] 2.3 Include summary metrics and category summaries
- [x] 2.4 Include per-case result details

## 3. File Export

- [x] 3.1 Add JSON export helper
- [x] 3.2 Add Markdown export helper
- [x] 3.3 Ensure parent directories are created

## 4. Verification

- [x] 4.1 Add tests for JSON export
- [x] 4.2 Add tests for Markdown export
- [x] 4.3 Keep existing benchmark tests passing
- [x] 4.4 Run `conda run -n GRAPHRAG python -m pytest -q`
- [x] 4.5 Run `openspec validate export-retrieval-benchmark-report --strict`

## 5. Documentation

- [x] 5.1 Document report export workflow in README
- [x] 5.2 Update production indexing architecture doc to prefer exported benchmark evidence
