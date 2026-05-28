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

当前 job record 仅保存在进程内，source index marker 保存在 `RAG_INDEX_DIR`。生产队列、持久化 job store、外部向量库、reranker 和增量索引仍属于后续 change。

## 设计文档

- [External RAG / GraphRAG Provider Design](docs/external_rag_graphrag_provider_design.md)
- [外部 Knowledge Provider / RAG 项目开发规范](docs/external_rag_provider_development.md)
