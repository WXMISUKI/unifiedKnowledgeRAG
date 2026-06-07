## Overview

This change adds a small acceptance smoke for an already registered local corpus. It runs in-process against the FastAPI app via `TestClient`, so it does not require the user to start `uvicorn` or run external services.

Default source:

```text
company_profile_2025_trial
```

Default cases:

| Query | Expected Mode |
| --- | --- |
| 公司主营业务是什么？ | answerable |
| 公司有哪些资质？ | answerable |
| 公司组织机构包括哪些部门？ | answerable |
| 公司完成过哪些工程规模？ | answerable |
| 退款规则是什么？ | insufficient_evidence |

## Decision Rules

- `go`: source is visible, manifest is available, all answerable cases return evidence and valid citations, and negative-control cases do not cite the approved source.
- `review`: source and API paths are available but one or more cases have weak or unexpected evidence.
- `blocked`: source is missing, manifest fails, HTTP contract fails, or any answer cites outside the retrieved citation allowlist.

## Boundaries

The smoke only reads existing provider APIs in-process. It does not register sources, create source-to-agent bindings, create formal ingestion jobs, start OCR, promote retrieval backends, run MyPrivateAgent, call vector databases, or execute GraphRAG.

## Output

The default export writes:

```text
docs/local-run/approved-local-corpus-acceptance/approved-local-corpus-acceptance-smoke.json
docs/local-run/approved-local-corpus-acceptance/approved-local-corpus-acceptance-smoke.md
```
