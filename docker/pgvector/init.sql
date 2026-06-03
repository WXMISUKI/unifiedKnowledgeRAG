CREATE EXTENSION IF NOT EXISTS vector;

CREATE SCHEMA IF NOT EXISTS unified_knowledge_rag;

CREATE TABLE IF NOT EXISTS unified_knowledge_rag.knowledge_chunks (
    id BIGSERIAL PRIMARY KEY,
    source_id TEXT NOT NULL,
    chunk_id TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(1024) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS knowledge_chunks_embedding_idx
    ON unified_knowledge_rag.knowledge_chunks
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 10);
