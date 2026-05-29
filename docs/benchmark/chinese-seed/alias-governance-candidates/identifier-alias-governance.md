# Identifier Alias Governance Evidence

## Summary

| Metric | Value |
| --- | ---: |
| total_aliases | 6 |
| status:candidate | 6 |
| risk:medium | 6 |

## Alias Rules

| ID | Canonical Prefix | Pattern | Owner | Status | Version | Risk |
| --- | --- | --- | --- | --- | --- | --- |
| af-refund-chinese-shorthand | af-refund | `af退款([0-9o]{1,3})` | customer_service | candidate | 2026-05-29 | medium |
| af-refund-compact | af-refund | `afrefund([0-9o]{1,3})` | customer_service | candidate | 2026-05-29 | medium |
| rfd-compact-ocr | rfd | `rfd([0-9o]{4})([0-9o]{3})` | customer_service | candidate | 2026-05-29 | medium |
| lst-batch-chinese-shorthand | lst-batch | `lst批量([a-z0-9o]+)` | logistics | candidate | 2026-05-29 | medium |
| lst-batch-compact | lst-batch | `lstbatch([a-z0-9o]+)` | logistics | candidate | 2026-05-29 | medium |
| ord-zs-compact-ocr | ord-zs | `ordzs([0-9o]{4})([0-9o]{4})` | logistics | candidate | 2026-05-29 | medium |

## Decision Notes

- This catalog is local evaluation evidence and is not a production alias service.
- Runtime retrieval defaults and public provider contracts remain unchanged.
- 6 alias rule(s) remain candidate status and require owner approval before production use.