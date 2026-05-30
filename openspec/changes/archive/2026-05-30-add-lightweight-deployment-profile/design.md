## Context

`unifiedKnowledgeRAG` is meant to be deployed as an external knowledge provider component. The current repository can run with `uvicorn`, but deployment reviewers still have to infer container build behavior, mounted state directories, model artifact directories, health checks, and the new API key guard configuration.

The goal is not to build a full platform deployment. The profile should be small, inspectable, and easy to adapt for local testing, public-network experiments, and future private-network deployments.

## Goals / Non-Goals

**Goals:**

- Provide a repeatable container build entry point.
- Provide a compose example with port mapping, health check, volumes for sources/indexes/models, and environment placeholders.
- Keep secrets out of git and images.
- Keep default retrieval behavior conservative.
- Document how to run and verify the profile.

**Non-Goals:**

- Do not add Kubernetes, Helm, Terraform, CI/CD, reverse proxy, TLS termination, or managed secret storage.
- Do not start Qdrant or other production infrastructure by default.
- Do not download BGE-M3 model artifacts during image build.
- Do not bake local source/index/model data into the image.

## Decisions

1. Use a single Python slim image.
   - Rationale: smallest clear path for a FastAPI component.
   - Alternative considered: conda image. It matches local development but creates a larger image and is unnecessary for the first deployment profile.

2. Keep compose example on fixture/mock defaults.
   - Rationale: it should boot without external services. Operators can opt into Qdrant/BGE-M3 later using existing settings.

3. Mount data and model directories.
   - Rationale: source documents, index state, and model artifacts should be operator-managed runtime state, not image content.

4. Include a health check against `/health`.
   - Rationale: `/health` intentionally remains public and suitable for liveness/readiness checks.

## Risks / Trade-offs

- [Risk] Docker build may be heavy because dependencies include optional model libraries. -> Mitigation: do not download model artifacts at build time; keep the profile explicit and reviewable.
- [Risk] Compose example may be mistaken for production hardening. -> Mitigation: name it as an example and document that TLS, secret storage, backup, and external vector stores remain deployment-owner responsibilities.
- [Risk] Operators may forget `PROVIDER_API_KEY`. -> Mitigation: `.env.example` and README call it out for non-local exposure.
