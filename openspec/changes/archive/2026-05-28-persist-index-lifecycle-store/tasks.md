## 1. Specification

- [x] 1.1 Validate `persist-index-lifecycle-store` with OpenSpec strict mode
- [x] 1.2 Keep the store scope local-file based and API-compatible in README/docs

## 2. Store Implementation

- [x] 2.1 Add a file-backed lifecycle store helper under `app/services`
- [x] 2.2 Persist ingestion jobs to `jobs.jsonl`
- [x] 2.3 Persist source lifecycle state to `sources.json`
- [x] 2.4 Use atomic replace for manifest writes

## 3. Service Integration

- [x] 3.1 Replace the process-local `_JOBS` truth with the durable store
- [x] 3.2 Update successful ingestion to persist both job and source status
- [x] 3.3 Update failed ingestion to persist both job and source failure status
- [x] 3.4 Update index status lookup to read from the source manifest

## 4. API Compatibility

- [x] 4.1 Preserve `POST /api/ingestion/jobs` response shape
- [x] 4.2 Preserve `GET /api/indexes/{source_id}/status` response shape
- [x] 4.3 Preserve fixture backend ready behavior
- [x] 4.4 Preserve health/catalog lifecycle metadata behavior

## 5. Verification

- [x] 5.1 Add tests for job persistence to `jobs.jsonl`
- [x] 5.2 Add tests for source status persistence to `sources.json`
- [x] 5.3 Add restart-style tests that reload status from existing files
- [x] 5.4 Keep existing provider contract tests passing
- [x] 5.5 Run `conda run -n GRAPHRAG python -m pytest -q`
- [x] 5.6 Run `openspec validate persist-index-lifecycle-store --strict`

## 6. Documentation

- [x] 6.1 Document local store files and limitations in README
- [x] 6.2 Document that `sources.json` is canonical local lifecycle status for this slice
