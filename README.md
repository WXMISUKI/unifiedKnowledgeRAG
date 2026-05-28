# unifiedKnowledgeRAG

unifiedKnowledgeRAG 是面向 MyPrivateAgent 的外部知识能力 Provider。项目定位是知识数据面，负责 RAG / GraphRAG 的检索合同、知识源目录、证据返回和后续索引生命周期；MyPrivateAgent 继续负责智能体身份、权限、策略、审计和调用治理。

## 当前切片

OpenSpec change：`add-knowledge-provider-v1`

本阶段规格纳入 RAG + GraphRAG 的合同边界，但运行时第一阶段只实现 document RAG：

- `GET /health`
- `GET /api/capabilities`
- `GET /api/catalog`
- `GET /api/rag/sources`
- `POST /api/rag/retrieve`
- `GET /api/graph/schemas`
- `POST /api/graph/query`

GraphRAG 当前只暴露 schema 和结构化 `GRAPH_NOT_IMPLEMENTED` 错误，图数据库、ontology traversal、hybrid retrieval 将在后续 change 中实现。

## 本地运行

```powershell
conda run -n GRAPHRAG uvicorn app.main:app --reload --port 8020
```

## 简单验证

```powershell
conda run -n GRAPHRAG python -m pytest tests/test_provider_contract.py -q
openspec validate add-knowledge-provider-v1 --strict
```

## Python 环境

后续开发统一使用 conda 环境 `GRAPHRAG`：

```powershell
conda activate GRAPHRAG
```

安装依赖：

```powershell
conda run -n GRAPHRAG python -m pip install -r requirements.txt
```

## Document RAG Backend

第二阶段 OpenSpec change `add-llamaindex-document-rag` 引入可配置 document RAG backend。

默认后端是 `fixture`，适合快速合同测试：

```powershell
$env:RAG_RETRIEVAL_BACKEND="fixture"
```

启用 LlamaIndex 本地索引后端：

```powershell
$env:RAG_RETRIEVAL_BACKEND="llamaindex"
$env:RAG_SOURCE_DIR="app/data/sources"
$env:RAG_INDEX_DIR="app/data/indexes/llamaindex"
```

当前 LlamaIndex 后端使用本地 markdown 文档和 MockEmbedding，不依赖 OpenAI key。它用于验证 provider-owned citation metadata、backend readiness 和 HTTP 合同稳定性。

第三阶段 OpenSpec change `add-explicit-index-lifecycle` 引入显式索引生命周期。本地第一版使用进程内 job record 和 source 级 index marker，保持 provider-neutral API 合同，不引入外部队列、数据库或生产向量库。

创建本地索引任务：

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8020/api/ingestion/jobs `
  -ContentType "application/json" `
  -Body '{"source_id":"refund_policy_docs"}'
```

查看 source index 状态：

```powershell
Invoke-RestMethod http://127.0.0.1:8020/api/indexes/refund_policy_docs/status
```

如果启用 `llamaindex` 后端但尚未对 source 执行 ingestion job，`POST /api/rag/retrieve` 会返回结构化 `INDEX_NOT_READY` 错误；如需快速回滚到合同测试路径，可切回：

```powershell
$env:RAG_RETRIEVAL_BACKEND="fixture"
```

第四阶段 OpenSpec change `persist-index-lifecycle-store` 将本地生命周期状态升级为轻量持久化文件：

- `RAG_INDEX_DIR/jobs.jsonl`：append-only ingestion job 记录。
- `RAG_INDEX_DIR/sources.json`：当前 source index lifecycle 状态，是本地 provider 的 canonical source status manifest。

这层仍然是 local-file adapter，不提供多进程写锁、队列调度、数据库迁移或远程对象存储。生产队列、持久化数据库、外部向量库、reranker 和增量索引仍属于后续 change。

第五阶段 OpenSpec change `add-index-job-operations` 增加本地 job 运维面：

```powershell
# 查看所有 ingestion jobs
Invoke-RestMethod http://127.0.0.1:8020/api/ingestion/jobs

# 按 source 或状态过滤
Invoke-RestMethod "http://127.0.0.1:8020/api/ingestion/jobs?source_id=refund_policy_docs&status=completed"

# 分页查看 job，返回 total / limit / offset / has_more
Invoke-RestMethod "http://127.0.0.1:8020/api/ingestion/jobs?limit=20&offset=0"

# 查看单个 job
Invoke-RestMethod http://127.0.0.1:8020/api/ingestion/jobs/<job_id>

# 重试 failed job，会创建一个新的 job 记录
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8020/api/ingestion/jobs/<job_id>/retry
```

当前只允许重试 `failed` job；`completed`、`running` 等非失败状态会返回结构化 `JOB_RETRY_NOT_ALLOWED`。取消任务、异步 worker 和鉴权策略仍留给后续 change。

第六阶段 OpenSpec change `add-index-job-pagination-retention` 增加分页和本地 compaction：

```powershell
# 保留最新 100 个 logical jobs，并重写 jobs.jsonl
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8020/api/ingestion/jobs/retention/compact `
  -ContentType "application/json" `
  -Body '{"keep_latest":100}'
```

Job list 展示的是按 `job_id` 去重后的最新 logical job 状态，而不是 `jobs.jsonl` 中的每条 raw event。Compaction 只保留最新 N 个 logical jobs；cursor pagination、定时保留策略、归档导出和鉴权策略仍留给后续 change。

第七阶段 OpenSpec change `add-index-job-cancellation-recovery` 增加显式取消和 stale-running 恢复：

```powershell
# 取消 running job，会追加 canceled 终态记录
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8020/api/ingestion/jobs/<job_id>/cancel `
  -ContentType "application/json" `
  -Body '{"reason":"operator stop"}'

# 将超过阈值仍为 running 的 job 标记为 failed，之后可走 retry
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8020/api/ingestion/jobs/recovery/stale-running `
  -ContentType "application/json" `
  -Body '{"max_age_seconds":3600}'
```

取消只允许作用于 `running` job，非 running 状态会返回结构化 `JOB_CANCEL_NOT_ALLOWED`。Stale recovery 不会后台自动执行，必须由调用方显式触发；它会把超时 running job 标记为带 `STALE_RUNNING_JOB` 错误的 `failed` 状态，以便后续通过 retry 创建新 job。当前仍不提供异步 worker 中断信号、分布式 lease、定时扫描或鉴权策略。

## 设计文档

- [External RAG / GraphRAG Provider Design](docs/external_rag_graphrag_provider_design.md)
- [外部 Knowledge Provider / RAG 项目开发规范](docs/external_rag_provider_development.md)
