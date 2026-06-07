## Why

The provider can now register local business corpus sources and MyPrivateAgent can consume a registered source, but operators still need one lightweight command that verifies an approved local source can move through preflight, ingestion job, index status, and retrieval acceptance.

This closes the next RAG usability gap without promoting Qdrant/BGE-M3, parsing raw PDFs, or expanding GraphRAG.

## What Changes

- Add a local approved-source ingestion loop that chains existing onboarding, preflight, explicit ingestion job, index status, and acceptance smoke.
- Export JSON and Markdown artifacts under `docs/local-run/approved-source-ingestion-loop/`.
- Add focused tests for `go`, `review`, `blocked`, and boundary behavior.
- Update roadmap/progress docs with the Stage 2 ingestion-loop milestone.

收口对象：已批准本地 markdown 业务资料成为 provider-visible source 后，能够明确完成 ingestion job、index status 与 retrieval smoke。

非目标：不解析原始 PDF，不启动 OCR，不调用 MyPrivateAgent，不创建 source-to-agent binding，不启用 `/api/chat`，不切换 Qdrant/BGE-M3 默认运行时，不执行 GraphRAG，不引入生产队列或后台 worker。

## Capabilities

### New Capabilities

- `local-approved-source-ingestion-loop`: Local operator loop that verifies an approved local source can be preflighted, ingested, indexed, and retrieval-smoked.

### Modified Capabilities

- None.

## Impact

- Code:
  - `app/services/local_approved_source_ingestion_loop.py`
  - `scripts/export_local_approved_source_ingestion_loop.py`
  - `tests/test_local_approved_source_ingestion_loop.py`
- Docs/artifacts:
  - `docs/local-run/approved-source-ingestion-loop/`
  - `docs/roadmap/enterprise_rag_maturity_next_stages.md`
  - `docs/progress/provider-improvement-tracker.md`
- APIs: none. This is a local CLI/report loop over existing provider-owned services.
- Dependencies: none.

