# Reindex Readiness Plan

- Report: `reindex-readiness-v1`
- Status: `ready`
- Generated At: `2026-06-05T02:20:53.454950+00:00`
- Retrieval Backend: `fixture`
- Source Dir: `app\data\sources`
- Index Dir: `app\data\indexes\llamaindex`

## Sources

| Source | Source File | Index Status | Fingerprint | Latest Job | Recommended Action |
|---|---|---|---|---|---|
| `refund_policy_docs` | `present` | `ready` | `in_sync` | `none` | `reindex_optional` |
| `logistics_faq` | `present` | `ready` | `in_sync` | `none` | `reindex_optional` |

## Job Summary

- Total latest logical jobs: `0`
- Status counts: `{}`

## Operation Notes

- This plan is read-only and does not trigger ingestion or index rebuilds.
- Back up the index directory before production reindex operations.
- Fixture backend does not require persisted source indexes.
- Some sources have no recorded ingestion job history.
