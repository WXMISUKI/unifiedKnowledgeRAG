## Why

The provider already has approved-source ingestion, indexing, and answer smoke loops, but the practical local user path is still too phase/report-oriented: a developer has to know which markdown trial, handoff, registration, ingestion, and acceptance scripts to chain together.

This change adds a lightweight file-to-QA entrypoint so local enterprise materials can be supplied by path, normalized when safe, ingested through the existing approved-source loop, and tested with a business query without adding a heavy ingestion platform.

## What Changes

- Add a local enterprise corpus ingestion + QA loop that accepts a local file path and emits a single go/review/blocked report.
- Support direct `.md`, `.markdown`, and `.txt` inputs by materializing them as markdown before reusing the existing approved-source ingestion loop.
- Return an explicit `blocked` result for raw `.pdf` and other unsupported formats, with recovery actions pointing to parser/OCR-derived markdown or normalized parser artifacts.
- Add a CLI exporter for day-to-day local use.
- Add focused tests for markdown, txt, missing file, unsupported pdf, downstream review/blocking, and boundary preservation.

收口对象：本地企业资料从文件路径进入 provider 管理并完成一次问答试跑的最小闭环。

非目标：

- 不实现原生 PDF/OCR 解析。
- 不启动 PaddleOCR 或外部 parser 服务。
- 不引入 LlamaIndex/Qdrant/GraphRAG 新依赖或改变默认检索后端。
- 不创建 source-to-agent binding。
- 不调用 MyPrivateAgent。
- 不做复杂资料管理后台、异步任务平台、权限审计或生产部署。

## Capabilities

### New Capabilities

- `local-enterprise-corpus-ingestion-qa-loop`: Defines the lightweight local file-to-RAG ingestion and QA loop for enterprise materials.

### Modified Capabilities

- None.

## Impact

- New service under `app/services/`.
- New exporter under `scripts/`.
- New focused tests under `tests/`.
- New local run artifacts under `docs/local-run/local-enterprise-corpus-ingestion-qa-loop/`.
- No runtime API behavior change, no database migration, no new dependency.
