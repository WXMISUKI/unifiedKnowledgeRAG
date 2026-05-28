## 1. Specification

- [x] 1.1 Validate `add-queued-ingestion-runner` with OpenSpec strict mode
- [x] 1.2 Document that queue execution is local and explicit, not production worker infrastructure

## 2. Contract Models

- [x] 2.1 Add `run_mode` to ingestion job creation request
- [x] 2.2 Add queue runner response model
- [x] 2.3 Add structured error for empty local queue

## 3. Store And Service

- [x] 3.1 Add queued create path that persists `queued` without building
- [x] 3.2 Add oldest queued job selection
- [x] 3.3 Add run-next service that appends `running`
- [x] 3.4 Add run-next success terminal state
- [x] 3.5 Add run-next failure terminal state and source status update

## 4. API Wiring

- [x] 4.1 Preserve default `POST /api/ingestion/jobs` synchronous behavior
- [x] 4.2 Support `run_mode=queued` in `POST /api/ingestion/jobs`
- [x] 4.3 Add `POST /api/ingestion/jobs/queue/run-next`

## 5. Verification

- [x] 5.1 Add tests for queued job creation
- [x] 5.2 Add tests for run-next success
- [x] 5.3 Add tests for run-next failure
- [x] 5.4 Add tests for empty queue error
- [x] 5.5 Run `conda run -n GRAPHRAG python -m pytest -q`
- [x] 5.6 Run `openspec validate add-queued-ingestion-runner --strict`

## 6. Documentation

- [x] 6.1 Document queued run mode in README
- [x] 6.2 Document run-next endpoint and future production queue decision points
