## Context

The deployment readiness evidence already exposes the relevant config surface. The remaining gap is a single reference page that tells operators what each setting does and which defaults belong to local development versus deployment.

## Goals / Non-Goals

**Goals**

- Document the deployment config surface in one place.
- Keep the guide aligned with actual env var names and mount paths.
- Make the "safe local defaults" vs "deployment inputs" distinction explicit.

**Non-Goals**

- No runtime config changes.
- No secret management implementation.
- No deployment orchestration or automation.

## Decisions

- Use the existing `.env.example` and `docker-compose.example.yml` as the source of truth for examples.
- Group variables by local development, deployment inputs, and evidence-refresh commands.
- Keep the guide short enough to be used as a pre-deploy checklist.

## Risks / Trade-offs

- If env var names evolve, the guide must be updated in lockstep.
- Too much detail could duplicate README content; keep only deployment-relevant fields here.
