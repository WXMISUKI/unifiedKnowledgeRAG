# Design: add-bge-m3-local-embedding-adapter

## Approach

Extend the existing embedding adapter factory with a `BgeM3LocalEmbeddingAdapter`. The adapter lazy-loads `FlagEmbedding.BGEM3FlagModel` on first use, then calls `encode(..., return_dense=True, return_sparse=False, return_colbert_vecs=False)` and reads `dense_vecs`.

The adapter remains local and opt-in:

- default provider remains `mock`
- provider key: `bge_m3_local`
- default model name: `BAAI/bge-m3`
- default vector size: `1024`

## Configuration

Add environment-backed settings:

- `EMBEDDING_PROVIDER=bge_m3_local`
- `EMBEDDING_MODEL=BAAI/bge-m3`
- `EMBEDDING_VECTOR_SIZE=1024`
- `EMBEDDING_MODEL_PATH=<local path>` to load an already-downloaded model
- `EMBEDDING_HF_ENDPOINT=https://hf-mirror.com` to opt into a Hugging Face-compatible mirror
- `EMBEDDING_LOCAL_FILES_ONLY=true` to force offline/local cache mode
- `BGE_M3_USE_FP16=true`
- `BGE_M3_BATCH_SIZE=12`
- `BGE_M3_MAX_LENGTH=8192`

The mirror is documented as an operator choice, not a default.

## Safety

Readiness returns `degraded` if `FlagEmbedding` is missing or the configured model cannot be loaded. The adapter is lazy so normal fixture/mock tests do not require model downloads.

The implementation records dense-only behavior in metadata and leaves sparse/hybrid retrieval for a later change.
