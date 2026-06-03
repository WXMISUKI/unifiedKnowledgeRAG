# Phase 2 Unsupported Format Negative-Control Smoke

- Report: `phase2-unsupported-format-negative-control-smoke-v1`
- Status: `ready`
- Decision: `keep_markdown_baseline`
- Generated At: `2026-06-03T02:41:59.279771+00:00`
- Readiness Report: `docs\operations\source-format-demand\phase2-source-format-demand-readiness.json`

## Summary

| Metric | Value |
|---|---|
| Total Checks | `5` |
| Passed Checks | `5` |
| Failed Checks | `0` |
| Parser-Ready Documents | `2` |
| Unsupported Documents | `0` |
| Non-Markdown Sources | `0` |
| Demand Signal | `False` |

## Checks

| Check | Passed | Details |
|---|---|---|
| `phase2_source_format_demand_readiness_present` | `True` | `{"readiness_status": "ready"}` |
| `markdown_positive_control` | `True` | `{"parser_ready_documents": 2}` |
| `unsupported_document_negative_control` | `True` | `{"unsupported_documents": 0}` |
| `non_markdown_source_negative_control` | `True` | `{"non_markdown_sources": 0}` |
| `decision_alignment_control` | `True` | `{"decision": "keep_markdown_baseline", "format_expansion_demand_signal": false}` |

## Notes

- This smoke report is local and read-only for Phase 2 parser-expansion boundary review.
- It verifies unsupported-format and non-markdown-source negative controls from the Phase 2 readiness export.
- It does not enable non-Markdown parsers, ingestion execution, or retrieval default changes.
