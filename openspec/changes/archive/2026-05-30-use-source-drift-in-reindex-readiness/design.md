## Context

`reindex-readiness-v1` is the current operator-facing plan before index refresh work. It summarizes source file presence, index lifecycle status, latest ingestion job, and recommended action.

`GET /api/rag/sources/{source_id}/documents` now exposes document-level `drift_status` from source file fingerprints. This is the missing signal for deciding whether a ready index may be stale.

## Approach

For each configured source in the reindex readiness report:

1. Keep existing file presence and index lifecycle checks.
2. Load the source document manifest diagnostics.
3. Summarize document drift statuses.
4. Add fields:
   - `source_fingerprint_status`
   - `document_fingerprints`
5. Update recommended action:
   - missing source file -> `restore_source_file_before_reindex`
   - changed document fingerprint -> `run_ingestion_job`
   - unchecked fingerprint -> `review_source_fingerprint`
   - not indexed / failed / canceled / unknown lifecycle -> `run_ingestion_job`
   - ready and in-sync -> `reindex_optional`

## Status Rules

- `blocked`: any source recommends restoring a missing source file.
- `review`: any source recommends ingestion or source fingerprint review.
- `ready`: all sources are ready and in sync.

## Read-Only Boundary

The report only reads local files and existing lifecycle state. It does not start ingestion jobs, rebuild indexes, compact history, call embedding services, call vector databases, or execute graph queries.

## Risks

- Manifest diagnostics are currently local-file oriented. This is acceptable for the current markdown baseline and can be extended later for object-store or database-backed sources.
- Reindex readiness becomes more conservative. That is intentional: changed source content should be visible before callers trust index readiness.
