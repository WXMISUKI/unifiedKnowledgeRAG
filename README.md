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
- `POST /api/rag/answer`
- `GET /api/graph/schemas`
- `POST /api/graph/query`

`GET /api/capabilities` 当前暴露三个稳定能力 id：

- `knowledge.rag.retrieve`：返回引用证据和紧凑 answer context。
- `knowledge.rag.answer`：执行引用式回答编排、evidence gate 和 composer boundary。
- `knowledge.graph.query`：GraphRAG 查询合同边界，当前仍是 planned。

GraphRAG 当前只暴露 schema 和结构化 `GRAPH_NOT_IMPLEMENTED` 错误，图数据库、ontology traversal、hybrid retrieval 将在后续 change 中实现。

`POST /api/rag/answer` 是 retrieval 之上的引用式回答编排入口。当前第一版使用确定性 extractive composer，不调用 Qwen、OpenAI 或本地大模型；它用于先稳定 answer envelope、citation、evidence 和 insufficient-evidence 合同。生产 LLM、流式回答、reranker、多 chunk synthesis 和 GraphRAG 多跳仍会按后续 OpenSpec change 单独评估。

## 本地运行

```powershell
conda run -n GRAPHRAG uvicorn app.main:app --reload --port 8020
```

## 简单验证

```powershell
conda run -n GRAPHRAG python -m pytest tests/test_provider_contract.py -q
openspec validate add-knowledge-provider-v1 --strict
```

## 引用式回答 MVP

本地 fixture 后端下可以直接验证 answer orchestration：

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8020/api/rag/answer `
  -ContentType "application/json" `
  -Body '{"query":"客户三天未发货能否退款？","knowledge_base_ids":["refund_policy_docs"],"top_k":2}'
```

有证据时返回 `answer_status=answered`，并携带 `answer`、`citations`、`documents` 和 `metadata`。没有可用证据时返回 `ok=true` 且 `answer_status=insufficient_evidence`，不会伪造答案，也不会把证据不足当成 provider error。

Answer orchestration 会先应用本地 evidence sufficiency gate。默认配置保持兼容，便于本地 fixture 和 smoke 测试；需要更严格验证时可以通过环境变量收紧：

```powershell
$env:RAG_ANSWER_MIN_EVIDENCE_COUNT="2"
$env:RAG_ANSWER_MIN_EVIDENCE_SCORE="0.5"
```

如果检索结果未达到门槛，接口会返回 `answer_status=insufficient_evidence`，`answer` 和 `citations` 为空，同时保留 `documents` 和 `metadata.evidence_gate` 供诊断。这个 gate 只是第一层确定性防线，不替代后续 reranker、evidence grading 或 LLM answer validation。

Answer composer 已经有 provider-neutral adapter 边界。默认 composer 是离线确定性的：

```powershell
$env:RAG_ANSWER_COMPOSER="deterministic"
$env:RAG_ANSWER_COMPOSER_MODEL="deterministic-extractive-v1"
```

`hosted` 和 `local` 是后续接入 Qwen、OpenAI、vLLM、Ollama 或其他内网模型的预留配置名；当前会 fail-closed 返回结构化 `ANSWER_COMPOSER_NOT_IMPLEMENTED`，不会静默 fallback，也不会偷偷调用公网或本地 LLM runtime。真正接入模型前仍需单独 OpenSpec change 讨论模型、密钥、数据出公网、prompt、引用约束和成本。

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

第八阶段 OpenSpec change `add-queued-ingestion-runner` 增加本地显式 queued runner：

```powershell
# 创建 queued job，不立即构建索引
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8020/api/ingestion/jobs `
  -ContentType "application/json" `
  -Body '{"source_id":"refund_policy_docs","run_mode":"queued"}'

# 显式处理下一个 queued job
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8020/api/ingestion/jobs/queue/run-next
```

未传 `run_mode` 时仍保持同步执行，避免破坏现有调用方。当前 runner 是本地显式触发，不是后台线程、外部队列或生产 worker pool；真正的异步 worker、队列基础设施、分布式 lease，以及 embedding 模型和向量数据库选择，需要后续单独讨论确认后再推进。

生产级索引架构的 embedding 模型、向量数据库、队列 worker、reranker 和 GraphRAG 存储选择，统一先看 [Production Indexing Architecture Decision](docs/architecture/production_indexing_architecture.md)。这些选择会影响成本、部署、数据安全和检索质量，后续实现前需要先确认候选方案。

第九阶段 OpenSpec change `add-retrieval-benchmark-harness` 增加本地检索评估基线。Benchmark cases 位于 `tests/fixtures/retrieval_benchmark_cases.json`，当前通过 `app.services.retrieval_benchmark` 直接运行，先用于测试和候选 adapter 对比，不暴露新的外部 API：

```powershell
conda run -n GRAPHRAG python -m pytest tests/test_retrieval_benchmark.py -q
```

当前指标包括 `hit_rate`、`citation_match_rate`、`empty_handling_rate`、category summary 和每个 case 的 `latency_ms`。Benchmark cases 覆盖 `policy`、`faq`、`evidence`、`paraphrase`、`multi-source`、`empty` 等类别，并标注 `difficulty`。后续讨论 embedding 模型、向量库、reranker 或 hybrid retrieval 时，应先补充真实语料 benchmark cases，再用同一 harness 对比候选方案。

第十一阶段 OpenSpec change `export-retrieval-benchmark-report` 增加本地报告导出能力。可以在 Python 中调用 benchmark service，将结果保存为 JSON 或 Markdown，作为后续 OpenSpec 选型证据：

```python
from pathlib import Path

from app.config import Settings
from app.services.retrieval_benchmark import (
    export_benchmark_report_json,
    export_benchmark_report_markdown,
    load_benchmark_cases,
    run_retrieval_benchmark,
)

cases = load_benchmark_cases(Path("tests/fixtures/retrieval_benchmark_cases.json"))
report = run_retrieval_benchmark(cases, Settings(rag_retrieval_backend="fixture"))
export_benchmark_report_json(report, Path("docs/benchmark/retrieval-fixture.json"))
export_benchmark_report_markdown(report, Path("docs/benchmark/retrieval-fixture.md"))
```

当前仍不新增 CLI 或 HTTP API；报告导出保持本地开发/评审工具属性。

第十二阶段 OpenSpec change `add-retrieval-candidate-evaluation` 增加本地候选检索 adapter 评估能力。候选评估仍是 service-only 工具，用来在真正选择 embedding 模型、向量数据库或 reranker 前，把候选方案跑在同一组 benchmark cases 上，并导出同名 JSON / Markdown 证据：

```python
from pathlib import Path

from app.services.retrieval_benchmark import (
    RetrievalCandidate,
    evaluate_retrieval_candidates,
    load_benchmark_cases,
)

cases = load_benchmark_cases(Path("tests/fixtures/retrieval_benchmark_cases.json"))
candidates = [
    RetrievalCandidate(
        id="fixture-baseline",
        backend="fixture",
        description="Fixture contract baseline",
        metadata={"embedding": "none", "vector_store": "none"},
    )
]

evaluate_retrieval_candidates(
    cases,
    candidates,
    output_dir=Path("docs/benchmark/candidates"),
)
```

导出后会生成 `fixture-baseline.json` 和 `fixture-baseline.md`。当前候选只映射到已存在的本地 backend；生产 embedding、向量库、reranker、hybrid retrieval 候选需要先讨论确认后再新增 adapter。

第十三阶段 OpenSpec change `evaluate-qdrant-vector-store-adapter` 把 Qdrant 纳入第一向量库候选，但仍保持 opt-in、evaluation-only：

```powershell
$env:RAG_RETRIEVAL_BACKEND="qdrant"
$env:QDRANT_URL="http://localhost:6333"
$env:QDRANT_COLLECTION="knowledge_chunks"
$env:QDRANT_VECTOR_NAME="text-dense"
$env:QDRANT_VECTOR_SIZE="1024"
```

当前 Qdrant backend 会在 readiness 中报告 `degraded`，表示它只是候选 adapter surface，尚未接入 live Qdrant 写入/检索。已落地的是 provider-neutral evidence chunk 到 Qdrant point/payload/filter 的映射，重点保留 `tenant_id`、`source_id`、`document_id`、`chunk_id`、`citation`、`acl_tags`、`embedding_model`、`chunking_strategy` 等企业级元数据。

本机公网测试路径建议是：先用本地 Docker Qdrant + hosted embedding 跑候选验证；企业内网路径则保留同一套 Qdrant payload/filter 合同，只替换为内网 Qdrant 和本地 embedding/reranker。embedding 模型、reranker 和 live Qdrant ingestion/retrieval 会在后续 change 中继续讨论并实现。

第十四阶段 OpenSpec change `add-live-qdrant-ingestion-retrieval` 增加 live Qdrant helper。它已经可以显式构造 Qdrant client、准备 collection、upsert 已有向量的 evidence chunks，并用调用方传入的 query vector 查询 Qdrant 命中结果：

```python
from app.config import Settings
from app.services.qdrant_vector_store import (
    VectorEvidenceChunk,
    create_qdrant_client,
    ensure_qdrant_collection,
    query_qdrant_documents,
    upsert_qdrant_chunks,
)

settings = Settings(
    qdrant_url=":memory:",
    qdrant_collection="knowledge_chunks",
    qdrant_vector_size=3,
)
client = create_qdrant_client(settings)
ensure_qdrant_collection(client, settings)

upsert_qdrant_chunks(
    client,
    [
        VectorEvidenceChunk(
            point_id="refund_policy_2026:section-3:0",
            source_id="refund_policy_docs",
            document_id="refund_policy_2026",
            chunk_id="section-3:0",
            title="售后退款规则",
            text="客户三天未发货可以申请退款。",
            citation="refund_policy_2026#section-3",
            vector=[0.1, 0.2, 0.3],
            metadata={"tenant_id": "tenant-a", "acl_tags": ["after_sales"]},
        )
    ],
    settings,
)

documents = query_qdrant_documents(
    client,
    query_vector=[0.1, 0.2, 0.3],
    source_ids=["refund_policy_docs"],
    settings=settings,
    top_k=3,
    tenant_id="tenant-a",
)
```

这个 helper 不负责把 query text 转成 embedding，也不负责 rerank；embedding/reranker 仍是后续单独选型和 adapter。默认 HTTP 检索路径也没有切到 Qdrant。

第十五阶段 OpenSpec change `add-embedding-adapter-interface` 增加 embedding adapter 抽象。当前默认 provider 是 deterministic mock，只用于合同测试和 Qdrant wiring，不代表真实语义检索质量：

```powershell
$env:EMBEDDING_PROVIDER="mock"
$env:EMBEDDING_MODEL="mock-hash-v1"
$env:EMBEDDING_VECTOR_SIZE="1024"
```

也可以在代码中显式创建 adapter，并为 Qdrant chunk 填充向量：

```python
from app.config import Settings
from app.services.embedding_adapters import create_embedding_adapter
from app.services.qdrant_vector_store import VectorEvidenceChunk, embed_qdrant_chunks

settings = Settings(embedding_provider="mock", embedding_vector_size=3)
adapter = create_embedding_adapter(settings)
embedded_chunks = embed_qdrant_chunks(
    [
        VectorEvidenceChunk(
            point_id="refund_policy_2026:section-3:0",
            source_id="refund_policy_docs",
            document_id="refund_policy_2026",
            chunk_id="section-3:0",
            title="售后退款规则",
            text="客户三天未发货可以申请退款。",
            citation="refund_policy_2026#section-3",
            vector=[],
            metadata={"tenant_id": "tenant-a"},
        )
    ],
    adapter,
)
```

`EMBEDDING_PROVIDER=hosted` 和 `EMBEDDING_PROVIDER=local` 目前是 fail-closed 占位，不会偷偷调用公网 API 或加载本地模型。后续选择 BGE-M3、Qwen、OpenAI、Jina 等候选时，会单独走 OpenSpec change 和 benchmark evidence。

第十六阶段 OpenSpec change `add-qdrant-text-query-orchestration` 将 Qdrant text query 链路打通为显式 opt-in：

```text
query text -> embedding adapter -> Qdrant vector query -> EvidenceDocument
```

启用方式仍然是显式选择 Qdrant：

```powershell
$env:RAG_RETRIEVAL_BACKEND="qdrant"
$env:QDRANT_URL="http://localhost:6333"
$env:QDRANT_COLLECTION="knowledge_chunks"
$env:EMBEDDING_PROVIDER="mock"
```

当前 `mock` embedding 只能证明链路可运行，不代表中文语义检索质量。真实使用前还需要完成：真实文档 ingestion、中文/双语 embedding 候选评估、benchmark report、必要时增加 reranker。

第十七阶段 OpenSpec change `add-qdrant-source-ingestion-flow` 将本地 source docs 接入 Qdrant ingestion lifecycle。显式选择 Qdrant 后，`POST /api/ingestion/jobs` 会读取 `RAG_SOURCE_DIR/<source_id>.md`，按 markdown 段落切成 evidence chunks，通过 embedding adapter 填充 vector，再 upsert 到 Qdrant，并写入 source index ready marker：

```powershell
$env:RAG_RETRIEVAL_BACKEND="qdrant"
$env:RAG_SOURCE_DIR="app/data/sources"
$env:RAG_INDEX_DIR="app/data/indexes/qdrant"
$env:QDRANT_URL=":memory:"
$env:QDRANT_COLLECTION="knowledge_chunks"
$env:QDRANT_VECTOR_NAME="text-dense"
$env:QDRANT_VECTOR_SIZE="1024"
$env:EMBEDDING_PROVIDER="mock"

Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8020/api/ingestion/jobs `
  -ContentType "application/json" `
  -Body '{"source_id":"refund_policy_docs"}'
```

当前 chunking 策略是 `markdown-paragraph-v1`，只作为评估基线。企业级 PDF、Word、表格、长文档结构化切分、chunk overlap、section summary、多粒度索引仍需要后续单独设计和 benchmark 验证。

第十八阶段 OpenSpec change `evaluate-chinese-embedding-candidates` 增加中文 embedding 候选评估入口。它只记录候选元数据和本地评估证据，不调用真实公网 API，也不加载本地模型：

```python
from pathlib import Path

from app.services.retrieval_benchmark import evaluate_embedding_candidates

evaluate_embedding_candidates(
    output_dir=Path("docs/benchmark/embedding-candidates"),
)
```

默认候选包括：

- `mock-hash-v1`：当前 deterministic contract baseline，不代表语义质量。
- `qwen-embedding-candidate`：中文 hosted 候选占位，需要单独确认数据出公网和私有化可行性。
- `bge-m3-local-candidate`：本地/内网中文与多语候选占位，需要后续验证部署资源和吞吐。
- `openai-embedding-candidate`：公网 hosted 多语 baseline，占位用于质量对比，不默认启用。

导出结果会生成 `<candidate-id>.json` 和 `<candidate-id>.md`。这些报告用于后续 OpenSpec 选型讨论，不等于批准生产 embedding provider。

第十九阶段 OpenSpec change `expand-chinese-retrieval-benchmark-cases` 扩展了中文企业场景 benchmark seed。当前本地 cases 从 8 条增加到 15 条，覆盖：

- 基础政策问答
- 退款例外规则
- 高价值退款复核
- 地址变更与未发货多意图问题
- 同城配送 SLA
- 包裹丢失跨团队协同
- 地址拦截操作
- 业务化 empty retrieval

这些 cases 仍是 seed benchmark，不是最终生产验收集。它们的价值是让后续 embedding、Qdrant、reranker 或 hybrid retrieval 候选先跑在同一张中文场景清单上。

第二十阶段 OpenSpec change `export-chinese-seed-evaluation-evidence` 增加中文 seed evidence bundle 导出。可以在本地生成 retrieval baseline 和 embedding candidate 的 JSON / Markdown 证据：

```python
from pathlib import Path

from app.services.retrieval_benchmark import export_chinese_seed_evidence_bundle

export_chinese_seed_evidence_bundle(Path("docs/benchmark/chinese-seed"))
```

当前默认证据已生成在：

- `docs/benchmark/chinese-seed/retrieval-candidates/fixture-chinese-seed-baseline.json`
- `docs/benchmark/chinese-seed/retrieval-candidates/fixture-chinese-seed-baseline.md`
- `docs/benchmark/chinese-seed/embedding-candidates/*.json`
- `docs/benchmark/chinese-seed/embedding-candidates/*.md`

`fixture-chinese-seed-baseline` 只代表本地合同基线，不代表真实语义检索质量。后续如果要接真实 Qwen、BGE-M3、OpenAI 或本地 embedding adapter，应先生成同格式候选报告再讨论是否推进。

第二十一阶段 OpenSpec change `add-bge-m3-local-embedding-adapter` 增加本地 BGE-M3 dense embedding adapter。默认仍是 `mock`，需要显式开启：

```powershell
$env:EMBEDDING_PROVIDER="bge_m3_local"
$env:EMBEDDING_MODEL="BAAI/bge-m3"
$env:EMBEDDING_VECTOR_SIZE="1024"
$env:BGE_M3_USE_FP16="true"
$env:BGE_M3_BATCH_SIZE="12"
$env:BGE_M3_MAX_LENGTH="8192"
```

安装依赖：

```powershell
conda run -n GRAPHRAG python -m pip install -r requirements.txt
```

如果国内直接访问 Hugging Face 下载较慢，可以显式配置镜像 endpoint：

```powershell
$env:EMBEDDING_HF_ENDPOINT="https://hf-mirror.com"
```

镜像地址不作为默认值写死进代码；生产或企业内网部署时更推荐提前下载模型，然后指定本地路径：

```powershell
$env:EMBEDDING_MODEL_PATH="D:\models\bge-m3"
$env:EMBEDDING_LOCAL_FILES_ONLY="true"
```

当前 adapter 只使用 BGE-M3 的 `dense_vecs`，不启用 sparse / ColBERT / hybrid retrieval；这些能力会在后续基于 benchmark misses 单独讨论。

第二十二阶段 OpenSpec change `cache-bge-m3-local-model-artifact` 增加本地模型缓存脚本，方便先把 BGE-M3 下载好，后续本地和内网部署直接复用模型目录：

```powershell
conda run -n GRAPHRAG python scripts/download_bge_m3_model.py `
  --output-dir models/bge-m3
```

国内网络较慢时，可以显式使用 Hugging Face 兼容镜像：

```powershell
conda run -n GRAPHRAG python scripts/download_bge_m3_model.py `
  --output-dir models/bge-m3 `
  --hf-endpoint https://hf-mirror.com
```

如果 Hugging Face 镜像 metadata 兼容性不稳定，可以改用 ModelScope 下载源：

```powershell
conda run -n GRAPHRAG python scripts/download_bge_m3_model.py `
  --source modelscope `
  --output-dir models/bge-m3
```

下载完成后会生成：

```text
models/bge-m3/model-manifest.json
```

`models/` 已加入 `.gitignore`，模型文件不会进入仓库。内网部署时拷贝整个 `models/bge-m3` 目录，然后配置：

```powershell
$env:EMBEDDING_PROVIDER="bge_m3_local"
$env:EMBEDDING_MODEL_PATH="D:\models\bge-m3"
$env:EMBEDDING_LOCAL_FILES_ONLY="true"
$env:EMBEDDING_VECTOR_SIZE="1024"
```

第二十三阶段 OpenSpec change `guard-rag-retrieval-index-readiness` 加强了检索入口的生命周期防线。`POST /api/rag/retrieve` 现在会先校验 source 是否存在、source index 是否 ready，再执行具体 backend 检索；对于 Qdrant，这可以避免未索引时提前触发向量库查询或 embedding 调用。

本地 Qdrant + BGE-M3 验证顺序建议固定为：

```powershell
$env:RAG_RETRIEVAL_BACKEND="qdrant"
$env:RAG_SOURCE_DIR="app/data/sources"
$env:RAG_INDEX_DIR="app/data/indexes/qdrant"
$env:QDRANT_URL=":memory:"
$env:QDRANT_COLLECTION="knowledge_chunks"
$env:QDRANT_VECTOR_NAME="text-dense"
$env:QDRANT_VECTOR_SIZE="1024"
$env:EMBEDDING_PROVIDER="bge_m3_local"
$env:EMBEDDING_MODEL_PATH="models/bge-m3"
$env:EMBEDDING_LOCAL_FILES_ONLY="true"
$env:EMBEDDING_VECTOR_SIZE="1024"
```

先建立 source index：

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8020/api/ingestion/jobs `
  -ContentType "application/json" `
  -Body '{"source_id":"refund_policy_docs"}'
```

确认 ready 后再检索：

```powershell
Invoke-RestMethod http://127.0.0.1:8020/api/indexes/refund_policy_docs/status

Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8020/api/rag/retrieve `
  -ContentType "application/json" `
  -Body '{"query":"客户三天未发货能否退款？","knowledge_base_ids":["refund_policy_docs"],"top_k":3}'
```

如果 status 不是 `ready`，检索会返回结构化 `INDEX_NOT_READY`，不会先触发 Qdrant retrieval。

第二十四阶段 OpenSpec change `export-qdrant-bge-smoke-evidence` 增加本地 smoke evidence 导出。它会在一次进程内使用同一个 Qdrant client 完成 source ingestion、query retrieval 和 JSON/Markdown 报告导出，适合验证 `QDRANT_URL=":memory:"`、本地 BGE-M3 模型和中文 seed cases 是否能跑通：

```powershell
conda run -n GRAPHRAG python scripts/export_qdrant_bge_smoke_evidence.py `
  --output-dir docs/benchmark/chinese-seed/retrieval-candidates `
  --source-id refund_policy_docs `
  --source-id logistics_faq `
  --embedding-model-path models/bge-m3 `
  --rag-score-threshold 0.5 `
  --embedding-local-files-only
```

导出文件：

```text
docs/benchmark/chinese-seed/retrieval-candidates/qdrant-bge-m3-smoke.json
docs/benchmark/chinese-seed/retrieval-candidates/qdrant-bge-m3-smoke.md
```

这个报告是“集成 smoke evidence”，不是生产验收。若命中率或 citation match 低，优先把它视为 chunking、top-k、reranker、hybrid retrieval 或 benchmark expected citation 需要继续设计的证据。

第二十五阶段 OpenSpec change `add-qdrant-score-threshold` 让 Qdrant retrieval 使用 `RAG_SCORE_THRESHOLD` 过滤低置信 hits。该阈值会写入 smoke evidence metadata，便于比较不同阈值下的 hit rate 和 empty handling：

```powershell
$env:RAG_SCORE_THRESHOLD="0.5"

conda run -n GRAPHRAG python scripts/export_qdrant_bge_smoke_evidence.py `
  --output-dir docs/benchmark/chinese-seed/retrieval-candidates `
  --source-id refund_policy_docs `
  --source-id logistics_faq `
  --embedding-model-path models/bge-m3 `
  --embedding-local-files-only
```

阈值不是越高越好：过低会让 empty 问题返回噪声证据，过高会压掉真实命中。后续应基于导出的 smoke/benchmark 报告讨论默认阈值、按 backend/model 区分阈值、以及是否引入 reranker 或 empty-intent 检测。

第二十六阶段 OpenSpec change `align-qdrant-markdown-citations` 将本地 Qdrant markdown ingestion 的 citation 从通用 `chunk-N` 对齐到业务锚点。当前只覆盖本地 fixture source，用于让中文 seed benchmark 的 citation match 具备评估意义：

```text
refund_policy_docs:
  chunk-1 -> refund_policy_2026#section-3
  chunk-2 -> refund_policy_2026#section-5
  chunk-3 -> refund_policy_2026#exception
  chunk-4 -> refund_policy_2026#high-value-review
  chunk-5 -> refund_policy_2026#address-change

logistics_faq:
  chunk-1 -> logistics_faq_2026#delay
  chunk-2 -> logistics_faq_2026#same-city-timeout
  chunk-3 -> logistics_faq_2026#lost-package
  chunk-4 -> logistics_faq_2026#address-intercept
```

未知 source 或未映射段落仍回退到 `document_id#chunk-N`。这不是最终企业文档解析器；后续 PDF/Word/表格、标题层级、显式 anchor、chunk overlap 和多粒度索引仍需要单独设计。

第二十七阶段 OpenSpec change `add-qdrant-threshold-sweep-evidence` 增加 Qdrant+BGE-M3 阈值扫描证据导出。它会用同一组 source 和中文 seed cases 比较多个 `RAG_SCORE_THRESHOLD`，帮助判断“调阈值是否足够”，还是需要继续引入 empty-intent 检测、reranker 或 hybrid retrieval：

```powershell
conda run -n GRAPHRAG python scripts/export_qdrant_bge_smoke_evidence.py `
  --output-dir docs/benchmark/chinese-seed/retrieval-candidates `
  --source-id refund_policy_docs `
  --source-id logistics_faq `
  --embedding-model-path models/bge-m3 `
  --embedding-local-files-only `
  --threshold-sweep 0.3 `
  --threshold-sweep 0.5 `
  --threshold-sweep 0.7
```

导出文件：

```text
docs/benchmark/chinese-seed/retrieval-candidates/qdrant-bge-m3-threshold-sweep.json
docs/benchmark/chinese-seed/retrieval-candidates/qdrant-bge-m3-threshold-sweep.md
```

当前本地 seed evidence 显示：

| Threshold | Hit Rate | Citation Match Rate | Empty Handling Rate |
| ---: | ---: | ---: | ---: |
| 0.3000 | 0.6316 | 0.6316 | 0.0000 |
| 0.5000 | 0.7368 | 0.7368 | 0.2857 |
| 0.7000 | 1.0000 | 1.0000 | 1.0000 |

第二十八阶段 OpenSpec change `expand-empty-retrieval-stress-cases` 将中文 seed benchmark 从 15 条扩展到 19 条，其中 expected-empty cases 从 3 条扩展到 7 条，覆盖会员等级、优惠券、密码重置、财务对账等当前知识源不支持但企业客服中常见的问题域。

扩展后，`0.5` 的 empty handling 从原先 0.6667 下降到 0.2857，说明较低阈值会把大量相近但不相关的政策片段误召回。`0.7` 在当前 seed 上仍保持全过，但这只说明它是下一轮默认阈值候选；生产默认阈值仍需要加入客户真实语料、长文档 chunking、更多空问法和必要的人工复核后再确认。

第二十九阶段 OpenSpec change `record-qdrant-threshold-recommendation` 将 threshold sweep 转成独立推荐证据。它读取已有 sweep JSON，按显式质量门槛选择最低通过阈值，不重新跑模型，也不修改运行时默认值：

```powershell
conda run -n GRAPHRAG python scripts/export_qdrant_bge_smoke_evidence.py `
  --output-dir docs/benchmark/chinese-seed/retrieval-candidates `
  --recommend-threshold-from-sweep docs/benchmark/chinese-seed/retrieval-candidates/qdrant-bge-m3-threshold-sweep.json
```

导出文件：

```text
docs/benchmark/chinese-seed/retrieval-candidates/qdrant-bge-m3-threshold-recommendation.json
docs/benchmark/chinese-seed/retrieval-candidates/qdrant-bge-m3-threshold-recommendation.md
```

当前推荐证据选择：

```text
selected_threshold: 0.7
approval_status: local_seed_recommendation
gates: hit_rate >= 1.0, citation_match_rate >= 1.0, empty_handling_rate >= 1.0
```

这仍是本地 seed recommendation，不是生产 approval。若后续新增客户真实语料、改 chunking、启用 reranker 或 hybrid retrieval，需要重新导出 sweep 和 recommendation。

第三十阶段 OpenSpec change `expand-long-document-chunking-cases` 增加长段落检索压力样本。当前 markdown baseline 仍是 `markdown-paragraph-v1`，但新增了更接近企业制度/流程文档的长段落：

- `refund_policy_2026#appeal-review`：退款申诉复核、补充举证、二线审核时限和处理记录。
- `logistics_faq_2026#batch-exception`：批量物流异常、订单汇总、物流运营团队同步和售后预案。

中文 seed benchmark 现在为 21 条，其中 long-section cases 2 条、expected-empty cases 7 条。重新导出的 Qdrant+BGE-M3 threshold sweep 显示：

| Threshold | Hit Rate | Citation Match Rate | Empty Handling Rate |
| ---: | ---: | ---: | ---: |
| 0.3000 | 0.6667 | 0.6667 | 0.0000 |
| 0.5000 | 0.7619 | 0.7619 | 0.2857 |
| 0.7000 | 1.0000 | 1.0000 | 1.0000 |

这说明 `0.7` 在当前长段落 seed 上仍未压掉真实召回，但还不能代表 PDF/Word、跨标题层级、超长章节、多粒度摘要 chunk 或客户真实语料。

第三十一阶段 OpenSpec change `evaluate-structure-aware-chunking` 增加 chunking strategy candidate evidence。当前只做本地评估证据，不切换运行时 ingestion：

```powershell
conda run -n GRAPHRAG python -c "from pathlib import Path; from app.services.retrieval_benchmark import export_chunking_strategy_evaluation; export_chunking_strategy_evaluation(Path('docs/benchmark/chinese-seed/chunking-candidates'))"
```

导出文件：

```text
docs/benchmark/chinese-seed/chunking-candidates/chunking-strategy-candidates.json
docs/benchmark/chinese-seed/chunking-candidates/chunking-strategy-candidates.md
```

当前候选状态：

| Candidate | Status | Notes |
| --- | --- | --- |
| `markdown-paragraph-v1` | implemented | 当前 Qdrant ingestion baseline，11 个本地 source chunks，citation stable，覆盖 long-section seed |
| `markdown-section-v1` | runnable | 可生成 section chunks，当前本地 source 生成 2 个 chunks，citation stable，运行时 ingestion 仍未切换 |
| `token-window-v1` | planned | 适合长段落、PDF/Word 抽取正文和 overlap 场景，尚无运行时检索指标 |

后续如果要真正替换 chunking，需要先把 planned candidate 做成 runnable adapter，再用同一组 benchmark 和 Qdrant+BGE evidence 对比，而不是直接改生产 ingestion。

第三十二阶段 OpenSpec change `add-markdown-section-chunking-candidate` 将 `markdown-section-v1` 从 planned 推进为 runnable candidate。它会按 markdown heading 聚合段落并生成 `markdown-section-v1` metadata，但 `load_qdrant_source_chunks(...)` 和运行时 Qdrant ingestion 仍使用 `markdown-paragraph-v1`。当前 evidence 只说明 section candidate 能生成稳定 chunk，还不声明检索质量优于 paragraph baseline；下一步需要把 section candidate 接入独立 Qdrant smoke，对比实际 retrieval metrics。

第三十三阶段 OpenSpec change `compare-qdrant-chunking-strategies` 增加 Qdrant+BGE-M3 分块策略 smoke 对比证据导出。它允许在不改变运行时默认 ingestion 的前提下，用同一组中文 seed cases 对比 `markdown-paragraph-v1` 和 `markdown-section-v1`：

```powershell
conda run -n GRAPHRAG python scripts/export_qdrant_bge_smoke_evidence.py `
  --output-dir docs/benchmark/chinese-seed/chunking-candidates `
  --source-id refund_policy_docs `
  --source-id logistics_faq `
  --embedding-model-path models/bge-m3 `
  --embedding-local-files-only `
  --rag-score-threshold 0.7 `
  --chunking-comparison
```

导出文件：

```text
docs/benchmark/chinese-seed/chunking-candidates/qdrant-bge-m3-chunking-comparison.json
docs/benchmark/chinese-seed/chunking-candidates/qdrant-bge-m3-chunking-comparison.md
```

当前本地 seed evidence 显示：

| Strategy | Chunk Count | Hit Rate | Citation Match Rate | Empty Handling Rate | Long-Section Hit Rate | Long-Section Citation Match Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `markdown-paragraph-v1` | 11 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| `markdown-section-v1` | 2 | 0.6667 | 0.3333 | 1.0000 | 0.5000 | 0.0000 |

结论：`markdown-section-v1` 虽然显著减少 chunk 数，但当前会损失细粒度 citation match 和部分命中；因此默认 Qdrant ingestion 继续保留 `markdown-paragraph-v1`。下一步更适合推进 `token-window-v1` 或“section + paragraph 多粒度索引”候选，而不是直接切换到纯 section chunking。

第三十四阶段 OpenSpec change `research-agentic-rag-patterns` 增加成熟 Agentic RAG / GraphRAG 模式研究文档：[Agentic RAG Pattern Research](docs/research/agentic_rag_patterns.md)。它对 LlamaIndex、LangGraph、OpenAI Retrieval、Microsoft GraphRAG 和 Qdrant hybrid/rerank 的设计模式做了项目内映射，结论是：

- 短期继续优先完善企业级文档 chunking，尤其是 `token-window-v1`。
- Query rewrite 和 evidence grading 适合作为后续 service-level candidate。
- Hybrid retrieval、reranker、GraphRAG storage 都需要独立 benchmark gate，不应一次性引入。
- MyPrivateAgent 继续做 agent control plane，`unifiedKnowledgeRAG` 继续做 knowledge data plane。

第三十五阶段 OpenSpec change `add-token-window-chunking-candidate` 将 `token-window-v1` 从 planned 推进为 runnable candidate。它使用轻量确定性 tokenizer：中文字符按单字计，英文/数字连续串按一个 token 计，并支持窗口 overlap。当前默认参数是 `max_tokens=120`、`overlap_tokens=24`、`min_tokens=12`，仍只用于本地评估，不改变默认 Qdrant ingestion。

重新导出的三策略 Qdrant+BGE-M3 evidence 显示：

| Strategy | Chunk Count | Hit Rate | Citation Match Rate | Empty Handling Rate | Long-Section Hit Rate | Long-Section Citation Match Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `markdown-paragraph-v1` | 11 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| `markdown-section-v1` | 2 | 0.6667 | 0.3333 | 1.0000 | 0.5000 | 0.0000 |
| `token-window-v1` | 8 | 0.7619 | 0.3333 | 1.0000 | 0.5000 | 0.0000 |

结论：`token-window-v1` 比纯 section 多保留了一些命中，但当前 citation match 仍不足，不能替换 `markdown-paragraph-v1` 默认策略。后续更适合做“多粒度索引”或先进入 query rewrite / evidence grading 评估，而不是直接推广单一 token-window 策略。

第三十六阶段 OpenSpec change `evaluate-query-rewrite-candidate` 增加离线 query rewrite candidate evidence。当前候选只使用确定性规则，不调用 LLM，不改变运行时检索默认行为，也不新增 HTTP API：

```powershell
conda run -n GRAPHRAG python -c "from pathlib import Path; from app.services.retrieval_benchmark import export_query_rewrite_candidate_evaluation; export_query_rewrite_candidate_evaluation(Path('docs/benchmark/chinese-seed/query-rewrite-candidates'))"
```

导出文件：

```text
docs/benchmark/chinese-seed/query-rewrite-candidates/query-rewrite-candidates.json
docs/benchmark/chinese-seed/query-rewrite-candidates/query-rewrite-candidates.md
```

当前本地 seed evidence 显示：

| Candidate | Rewritten Cases | Rewrite Rate | Expected-empty Rewrites | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `original-query-baseline` | 0 | 0.0000 | 0 | 1.0000 | 1.0000 | 1.0000 |
| `controlled-support-rewrite-v1` | 6 | 0.2857 | 0 | 1.0000 | 1.0000 | 1.0000 |

结论：受控改写在当前 fixture seed 上没有造成回归，并且保护了 expected-empty 样本；但这只是离线候选证据，不代表可以直接上线 LLM query rewrite。后续若启用运行时改写，需要先扩展真实问法、空问法和 false-positive 评估，并明确是否允许公网 LLM 或仅使用内网模型。

第三十七阶段 OpenSpec change `evaluate-evidence-grading-candidate` 增加离线 evidence grading candidate evidence。它用于判断召回证据是否真正 answer-bearing，而不是只看向量分数或是否返回了某个 source。当前仍是确定性本地评估，不调用 LLM，不过滤运行时结果，不改变回答生成行为：

```powershell
conda run -n GRAPHRAG python -c "from pathlib import Path; from app.services.retrieval_benchmark import export_evidence_grading_candidate_evaluation; export_evidence_grading_candidate_evaluation(Path('docs/benchmark/chinese-seed/evidence-grading-candidates'))"
```

导出文件：

```text
docs/benchmark/chinese-seed/evidence-grading-candidates/evidence-grading-candidates.json
docs/benchmark/chinese-seed/evidence-grading-candidates/evidence-grading-candidates.md
```

当前本地 seed evidence 显示：

| Candidate | Policy | Answer-bearing Rate | Related-insufficient | Missing Evidence | Unexpected Evidence | Expected-empty Pass Rate |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `citation-match-grader-v1` | citation match | 1.0000 | 0 | 0 | 0 | 1.0000 |
| `source-match-grader-v1` | source match | 1.0000 | 0 | 0 | 0 | 1.0000 |

结论：当前 fixture baseline 下，严格 citation grader 和宽松 source grader 都没有暴露失败。但这主要说明当前 seed 的 fixture 检索链路稳定；后续要让 evidence grading 真正产生决策价值，需要引入“同 source 但 citation 不足”“相关但不能回答”“召回为空但应回答”等 harder cases，再讨论是否作为 runtime answer gate。

第三十八阶段 OpenSpec change `expand-insufficient-evidence-benchmark-cases` 增加 evidence grading stress fixture。它独立于主中文 seed，不影响 threshold、chunking、query rewrite 的历史 baseline，用来专门暴露 answer gate 需要处理的失败模式：

```powershell
conda run -n GRAPHRAG python -c "from pathlib import Path; from app.services.retrieval_benchmark import export_evidence_grading_candidate_evaluation; export_evidence_grading_candidate_evaluation(Path('docs/benchmark/chinese-seed/evidence-grading-stress'), cases_path=Path('tests/fixtures/evidence_grading_stress_cases.json'))"
```

导出文件：

```text
docs/benchmark/chinese-seed/evidence-grading-stress/evidence-grading-candidates.json
docs/benchmark/chinese-seed/evidence-grading-stress/evidence-grading-candidates.md
```

当前 stress evidence 显示：

| Candidate | Answer-bearing Rate | Related-insufficient | Missing Evidence | Unexpected Evidence | Expected-empty Pass Rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| `citation-match-grader-v1` | 0.0000 | 1 | 1 | 1 | 0.0000 |
| `source-match-grader-v1` | 0.3333 | 0 | 1 | 1 | 0.0000 |

结论：严格 citation grader 能把“同 source 但 citation 不足”识别为 `related_insufficient`，宽松 source grader 会把它放过；两者都会暴露漏召回和 expected-empty 误召回。这说明后续若做 runtime answer gate，不能只按 source 命中判断，需要继续扩展真实 false-positive/false-negative 样本并评估是否需要 reranker 或更细粒度 citation。

第三十九阶段 OpenSpec change `expand-exact-term-identifier-benchmark-cases` 增加 exact-term / identifier benchmark fixture。它独立于主中文 seed，用来专门观察政策编号、表单名、工作流缩写、订单样式 ID 这类问题是否会成为 dense-only retrieval 的短板：

```powershell
conda run -n GRAPHRAG python -c "from pathlib import Path; from app.services.retrieval_benchmark import load_benchmark_cases, run_retrieval_benchmark, export_benchmark_report_json, export_benchmark_report_markdown; from app.config import Settings; cases=load_benchmark_cases(Path('tests/fixtures/exact_term_identifier_cases.json')); report=run_retrieval_benchmark(cases, Settings(rag_retrieval_backend='fixture')); output=Path('docs/benchmark/chinese-seed/exact-term-candidates'); export_benchmark_report_json(report, output / 'exact-term-fixture-baseline.json'); export_benchmark_report_markdown(report, output / 'exact-term-fixture-baseline.md')"
```

导出文件：

```text
docs/benchmark/chinese-seed/exact-term-candidates/exact-term-fixture-baseline.json
docs/benchmark/chinese-seed/exact-term-candidates/exact-term-fixture-baseline.md
```

当前 exact-term fixture baseline 显示：

| Category | Cases | Hit Rate | Citation Match Rate |
| --- | ---: | ---: | ---: |
| `policy-code` | 1 | 1.0000 | 1.0000 |
| `form-name` | 1 | 1.0000 | 1.0000 |
| `workflow-acronym` | 1 | 1.0000 | 1.0000 |
| `order-like-id` | 1 | 1.0000 | 1.0000 |

结论：fixture backend 可以命中这些精确词锚点，但这只是本地合同 baseline。后续是否需要 sparse/hybrid retrieval，应基于 Qdrant+BGE-M3 或真实向量检索对这组 exact-term fixture 的表现决定，不能因为 fixture 通过就直接认为 dense-only 足够。

第四十阶段 OpenSpec change `evaluate-qdrant-exact-term-smoke` 将 exact-term fixture 跑到了 Qdrant + 本地 BGE-M3 dense-only 链路。导出命令：

```powershell
conda run -n GRAPHRAG python scripts/export_qdrant_bge_smoke_evidence.py `
  --exact-term-smoke `
  --output-dir docs/benchmark/chinese-seed/exact-term-candidates `
  --cases-path tests/fixtures/exact_term_identifier_cases.json `
  --source-id refund_policy_docs `
  --source-id logistics_faq `
  --embedding-model-path models/bge-m3 `
  --embedding-local-files-only `
  --rag-score-threshold 0.7
```

导出文件：

```text
docs/benchmark/chinese-seed/exact-term-candidates/qdrant-bge-m3-exact-term-smoke.json
docs/benchmark/chinese-seed/exact-term-candidates/qdrant-bge-m3-exact-term-smoke.md
```

当前 dense-only evidence 显示：

| Category | Cases | Hit Rate | Citation Match Rate | Notes |
| --- | ---: | ---: | ---: | --- |
| `policy-code` | 1 | 1.0000 | 1.0000 | `RFD-2026-003` 命中 |
| `form-name` | 1 | 0.0000 | 0.0000 | `AF-REFUND-02` 未返回证据 |
| `workflow-acronym` | 1 | 1.0000 | 1.0000 | `LST-BATCH-OPS` 命中 |
| `order-like-id` | 1 | 0.0000 | 0.0000 | `ORD-ZS-2026-0007` 未返回证据 |

总计 hit rate / citation match rate 均为 `0.5000`。这说明当前 Qdrant+BGE-M3 dense-only 在编号、表单名、订单样式 ID 上已经暴露漏召回；下一步更适合推进 sparse/BM25/dense+sparse hybrid candidate 对比，而不是继续只调 dense 阈值或直接引入 reranker。

第四十一阶段 OpenSpec change `evaluate-qdrant-hybrid-exact-term-candidate` 增加 evaluation-only Qdrant dense+sparse hybrid 候选。它使用 Qdrant named vectors：

- `text-dense`：现有 BGE-M3 dense vector。
- `text-sparse`：本地确定性 `lexical-identifier-sparse-v1`，用于政策编号、表单名、工作流缩写、订单样式 ID 等精确 token。
- `fusion=rrf`：通过 Qdrant Query API 的 prefetch + Reciprocal Rank Fusion 合并 dense/sparse 结果。

导出命令：

```powershell
conda run -n GRAPHRAG python scripts/export_qdrant_bge_smoke_evidence.py `
  --hybrid-exact-term-smoke `
  --output-dir docs/benchmark/chinese-seed/exact-term-candidates `
  --cases-path tests/fixtures/exact_term_identifier_cases.json `
  --source-id refund_policy_docs `
  --source-id logistics_faq `
  --embedding-model-path models/bge-m3 `
  --embedding-local-files-only `
  --rag-score-threshold 0.7
```

导出文件：

```text
docs/benchmark/chinese-seed/exact-term-candidates/qdrant-bge-m3-hybrid-exact-term-smoke.json
docs/benchmark/chinese-seed/exact-term-candidates/qdrant-bge-m3-hybrid-exact-term-smoke.md
```

dense-only 与 hybrid exact-term seed 对比：

| Candidate | Retrieval Mode | Hit Rate | Citation Match Rate | Notes |
| --- | --- | ---: | ---: | --- |
| `qdrant-bge-m3-exact-term-smoke` | dense-only | 0.5000 | 0.5000 | 漏掉 `AF-REFUND-02` 和 `ORD-ZS-2026-0007` |
| `qdrant-bge-m3-hybrid-exact-term-smoke` | dense+sparse RRF | 1.0000 | 1.0000 | 四类 exact-term seed 全部命中 |

结论：hybrid 对 exact-term recall 有明确帮助，但当前 exact-term fixture 没有 expected-empty case，不能证明 false-positive 风险可控。下一步如果继续推进 retrieval 质量，应该补 `evaluate-qdrant-hybrid-empty-stress` 或同类门禁，用 unsupported business queries 验证 hybrid 不会因为 sparse token overlap 带来过召回。

第四十二阶段 OpenSpec change `evaluate-qdrant-hybrid-empty-stress` 增加 hybrid expected-empty 压力集。它独立于主中文 seed 和 exact-term fixture，专门放入“看起来像已有编号/缩写、但知识源并不支持”的问题：

- `AF-REFUND-99`
- `RFD-2026-999`
- `LST-BATCH-BILLING`
- `ORD-ZS-2026-9999`

导出命令：

```powershell
conda run -n GRAPHRAG python scripts/export_qdrant_bge_smoke_evidence.py `
  --hybrid-empty-stress `
  --output-dir docs/benchmark/chinese-seed/hybrid-empty-stress `
  --cases-path tests/fixtures/hybrid_empty_stress_cases.json `
  --source-id refund_policy_docs `
  --source-id logistics_faq `
  --embedding-model-path models/bge-m3 `
  --embedding-local-files-only `
  --rag-score-threshold 0.7
```

导出文件：

```text
docs/benchmark/chinese-seed/hybrid-empty-stress/qdrant-bge-m3-hybrid-empty-stress.json
docs/benchmark/chinese-seed/hybrid-empty-stress/qdrant-bge-m3-hybrid-empty-stress.md
```

当前 evidence 显示：

| Candidate | Cases | Empty Handling Rate | Notes |
| --- | ---: | ---: | --- |
| `qdrant-bge-m3-hybrid-empty-stress` | 4 | 0.0000 | 四条 unsupported token-overlap 问题全部返回了证据 |

结论：hybrid 证明了 exact-term recall 价值，也证明了 false-positive 风险。它现在不能作为 runtime 默认，也不能只靠“exact-term 全过”推进生产；下一步应做 hybrid gating candidate，例如 sparse score gate、exact-token allowlist、dense+hybrid two-stage gate，或 evidence grading/reranker 组合，用同一组 exact-term + empty-stress 证据同时衡量召回和过召回。

第四十三阶段 OpenSpec change `evaluate-hybrid-gating-candidate` 增加 evaluation-only hybrid gating 候选。当前实现的是最窄的 `exact-identifier-containment-gate-v1`：当 query 含有 `AF-REFUND-02`、`RFD-2026-003`、`LST-BATCH-OPS`、`ORD-ZS-2026-0007` 这类 identifier-like token 时，只有 evidence snippet 同时包含 query 中全部 identifier 才会被保留；没有 identifier 的 query 不受该 gate 影响。

导出命令：

```powershell
conda run -n GRAPHRAG python scripts/export_qdrant_bge_smoke_evidence.py `
  --hybrid-gating-candidate `
  --output-dir docs/benchmark/chinese-seed/hybrid-gating-candidates `
  --cases-path tests/fixtures/exact_term_identifier_cases.json `
  --empty-cases-path tests/fixtures/hybrid_empty_stress_cases.json `
  --source-id refund_policy_docs `
  --source-id logistics_faq `
  --embedding-model-path models/bge-m3 `
  --embedding-local-files-only `
  --rag-score-threshold 0.7
```

导出文件：

```text
docs/benchmark/chinese-seed/hybrid-gating-candidates/qdrant-bge-m3-hybrid-exact-identifier-gate.json
docs/benchmark/chinese-seed/hybrid-gating-candidates/qdrant-bge-m3-hybrid-exact-identifier-gate.md
```

当前 evidence 显示：

| Candidate | Cases | Hit Rate | Citation Match Rate | Empty Handling Rate | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| `qdrant-bge-m3-hybrid-exact-identifier-gate` | 8 | 1.0000 | 1.0000 | 1.0000 | exact-term 4/4 保留，empty-stress 4/4 由 raw false positive 过滤为空 |

结论：这个 gate 证明“hybrid recall + exact identifier false-positive control”在本地 seed 上可行，但它仍不是 runtime 默认。生产推广前还需要扩充真实客户语料、评估无编号自然语言 query、决定是否使用 BGE-M3 原生 sparse / BM25 / reranker，并明确误拒风险。

第四十四阶段 OpenSpec change `expand-hybrid-gating-benchmark` 扩展 hybrid gating 压力集，并把 `exact-identifier-containment-gate-v1` 从“字符串包含”收紧为“identifier 集合精确匹配”。这可以避免 `AF-REFUND` 被 `AF-REFUND-02` 这种更长编号误放行。

新增 fixture：

```text
tests/fixtures/hybrid_gating_positive_cases.json
tests/fixtures/hybrid_gating_empty_expanded_cases.json
```

导出命令：

```powershell
conda run -n GRAPHRAG python scripts/export_qdrant_bge_smoke_evidence.py `
  --hybrid-gating-candidate `
  --output-dir docs/benchmark/chinese-seed/hybrid-gating-candidates-expanded `
  --cases-path tests/fixtures/hybrid_gating_positive_cases.json `
  --empty-cases-path tests/fixtures/hybrid_gating_empty_expanded_cases.json `
  --source-id refund_policy_docs `
  --source-id logistics_faq `
  --embedding-model-path models/bge-m3 `
  --embedding-local-files-only `
  --rag-score-threshold 0.7
```

导出文件：

```text
docs/benchmark/chinese-seed/hybrid-gating-candidates-expanded/qdrant-bge-m3-hybrid-exact-identifier-gate.json
docs/benchmark/chinese-seed/hybrid-gating-candidates-expanded/qdrant-bge-m3-hybrid-exact-identifier-gate.md
```

当前 expanded evidence 显示：

| Candidate | Cases | Hit Rate | Citation Match Rate | Empty Handling Rate | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| `qdrant-bge-m3-hybrid-exact-identifier-gate` | 7 | 1.0000 | 1.0000 | 1.0000 | multi-id positive 3/3 保留，partial/same-prefix empty 4/4 过滤为空 |

结论：扩展 fixture 进一步证明 exact identifier gate 对“多编号正例”和“部分编号/同前缀错号”都有本地防护效果。不过这仍然只覆盖规范编号文本。生产前还应补 OCR 错字、别名、编号跨 chunk、用户简称、无编号语义问题，以及需要 reranker/evidence grading 的 noisy top-k 场景。

第四十五阶段 OpenSpec change `evaluate-noisy-identifier-gate-candidate` 增加 evaluation-only noisy/alias gate 候选。`alias-aware-identifier-gate-v1` 会在 identifier gate 前做本地归一化：处理 `O/0` OCR 混淆、空格拆分编号，以及当前 fixture 中的中文简称，例如 `AF退款02`、`LST批量OPS`。

新增 fixture：

```text
tests/fixtures/noisy_identifier_positive_cases.json
tests/fixtures/noisy_identifier_empty_cases.json
```

导出命令：

```powershell
conda run -n GRAPHRAG python scripts/export_qdrant_bge_smoke_evidence.py `
  --hybrid-alias-gating-candidate `
  --output-dir docs/benchmark/chinese-seed/noisy-identifier-gating-candidates `
  --cases-path tests/fixtures/noisy_identifier_positive_cases.json `
  --empty-cases-path tests/fixtures/noisy_identifier_empty_cases.json `
  --source-id refund_policy_docs `
  --source-id logistics_faq `
  --embedding-model-path models/bge-m3 `
  --embedding-local-files-only `
  --rag-score-threshold 0.7
```

导出文件：

```text
docs/benchmark/chinese-seed/noisy-identifier-gating-candidates/qdrant-bge-m3-hybrid-alias-identifier-gate.json
docs/benchmark/chinese-seed/noisy-identifier-gating-candidates/qdrant-bge-m3-hybrid-alias-identifier-gate.md
```

当前 noisy/alias evidence 显示：

| Candidate | Cases | Hit Rate | Citation Match Rate | Empty Handling Rate | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| `qdrant-bge-m3-hybrid-alias-identifier-gate` | 8 | 1.0000 | 1.0000 | 1.0000 | OCR/中文简称 positive 4/4 保留，错误别名/错号 empty 4/4 过滤为空 |

结论：alias-aware gate 证明了“小型本地归一化表 + strict identifier gate”的可行性，但它仍不是生产别名治理。生产推广前需要把 alias 来源、审批、版本、审计、冲突处理做成显式流程，并继续补编号跨 chunk、OCR 噪声更强、无编号语义问题和 noisy top-k reranker/evidence grading 证据。

第四十六阶段 OpenSpec change `add-alias-governance-split-chunk-benchmark` 将别名规则从代码中的硬编码推进为本地治理 catalog，并增加 split-chunk 风险证据。

新增 alias catalog：

```text
app/data/identifier_alias_catalog.json
```

新增 split-chunk source / fixture：

```text
app/data/sources/split_refund_policy_docs.md
tests/fixtures/split_chunk_identifier_cases.json
tests/fixtures/no_benchmark_cases.json
```

alias governance 导出命令：

```powershell
conda run -n GRAPHRAG python scripts/export_qdrant_bge_smoke_evidence.py `
  --alias-governance `
  --output-dir docs/benchmark/chinese-seed/alias-governance-candidates
```

split-chunk gating 导出命令：

```powershell
conda run -n GRAPHRAG python scripts/export_qdrant_bge_smoke_evidence.py `
  --hybrid-gating-candidate `
  --output-dir docs/benchmark/chinese-seed/split-chunk-gating-candidates `
  --cases-path tests/fixtures/split_chunk_identifier_cases.json `
  --empty-cases-path tests/fixtures/no_benchmark_cases.json `
  --source-id split_refund_policy_docs `
  --embedding-model-path models/bge-m3 `
  --embedding-local-files-only `
  --rag-score-threshold 0.7
```

导出文件：

```text
docs/benchmark/chinese-seed/alias-governance-candidates/identifier-alias-governance.json
docs/benchmark/chinese-seed/alias-governance-candidates/identifier-alias-governance.md
docs/benchmark/chinese-seed/split-chunk-gating-candidates/qdrant-bge-m3-hybrid-exact-identifier-gate.json
docs/benchmark/chinese-seed/split-chunk-gating-candidates/qdrant-bge-m3-hybrid-exact-identifier-gate.md
```

当前 evidence 显示：

| Evidence | Result | Notes |
| --- | --- | --- |
| alias governance | 6 aliases, all `candidate`, all `medium` risk | 仍需 owner approval、版本、审计和冲突处理，不能当生产 alias service |
| split-chunk gating | hit rate `0.0000`, citation match `0.0000` | raw hybrid 返回了 `policy-code` 和 `form-code` 两个相关 chunk，但 strict gate 因没有单个 chunk 同时包含两个 identifier 而全部过滤 |

结论：alias 方向需要治理流程，而不是继续硬编码；split-chunk 结果说明 strict identifier gate 不能单独解决“相关证据分散在多个 chunk”的企业文档问题。下一步应评估 parent/section context、multi-chunk evidence aggregation 或 reranker/evidence grading，而不是直接把 strict gate 推为默认。

## 设计文档

- [External RAG / GraphRAG Provider Design](docs/external_rag_graphrag_provider_design.md)
- [外部 Knowledge Provider / RAG 项目开发规范](docs/external_rag_provider_development.md)
- [Production Indexing Architecture Decision](docs/architecture/production_indexing_architecture.md)
- [Agentic RAG Pattern Research](docs/research/agentic_rag_patterns.md)
