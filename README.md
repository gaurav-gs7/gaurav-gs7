# Gaurav G S

SRE · Platform Engineering · AI Infrastructure · Systems Engineering

[LinkedIn](https://www.linkedin.com/in/gaurav-g-s-9a7495180/) ·
[Medium](https://medium.com/@ngs.gaurav7195) ·
[Email](mailto:ngs.gaurav7195@gmail.com)

I build control planes for the places where production systems fail: inference
changes, deployments, incidents, workflows, Kubernetes rollouts, and AI-agent tool
calls. My recurring design rule is simple:

> AI may explain evidence. Deterministic code decides, policy gates mutations, and
> durable records prove what happened.

## Featured work

### [InferLab](https://github.com/gaurav-gs7/InferLab) — release assurance for LLM inference changes

InferLab is the strongest expression of how I approach AI infrastructure. It
consumes benchmark, simulator, and fault evidence and produces a deterministic
`PASS`, `BLOCK`, or `INCONCLUSIVE` release decision without turning missing data
into confidence.

- Strict, versioned contracts bind the exact model, engine, container, CUDA,
  driver, GPU, scheduler, workload, and policy intent.
- Loss-aware adapters preserve raw producer semantics and cryptographic provenance.
- An uncertainty gate checks freshness, compatibility, coverage, sample
  sufficiency, confidence bounds, fairness, SLOs, recovery, and cost.
- Counterexample minimization finds and re-verifies the smallest known failing
  workload.
- Content-addressed safety cases replay the decision offline and support detached
  Ed25519 signatures.
- CI exercises unit, race, fuzz, golden, integration, security, and
  failure-injection paths.

The repository is deliberately honest about its boundary: it is pre-alpha, its
public proofs are synthetic `BLOCK` and `INCONCLUSIVE` cases, and it does not claim
a production `PASS` without observed target-system evidence. The working name also
needs to change before v0.1 because of a conflict in the inference tooling space.

Start with the [architecture](https://github.com/gaurav-gs7/InferLab/blob/main/docs/architecture.md),
[threat model](https://github.com/gaurav-gs7/InferLab/blob/main/docs/threat-model.md),
or reproduce the signed public proof with `make demo-safety-case`.

### [Argus](https://github.com/gaurav-gs7/Argus) — deterministic incident response control plane

Argus correlates operational signals, builds incident timelines, generates
evidence-backed RCA, and routes remediation through deterministic policy and
approval controls. PostgreSQL stores incidents and audit evidence; NATS JetStream
carries work; Prometheus, Grafana, Loki, and OpenTelemetry expose the operating
state. Docker-backed tests verify real database grouping/audit behavior and queue
delivery rather than only isolated functions.

Reproduce the local quality and integration gates with `make ci` and
`make integration-test`.

### [CloudDock AI](https://github.com/gaurav-gs7/CloudDock) — evidence-first AWS deployment platform

CloudDock models the path from GitHub revision to CodeBuild, ECR, ECS Fargate, ALB
health verification, and exact rollback. Its release passport links immutable
source/configuration identity, lifecycle events, policy findings, comparative
health, cost, and rollback lineage. The control plane uses Go, DynamoDB conditional
state transitions, Step Functions, KMS envelope encryption, resumable log delivery,
team RBAC, and AWS CDK; the UI is React and TypeScript.

CDK synthesis and local tests are evidence of implementation, not proof of a live
production deployment. The repository includes an acceptance matrix for that
separate claim. Run the clean-clone gate with `make verify`.

## More systems work

| Project | Problem addressed | Concrete engineering signal |
| --- | --- | --- |
| [Helios](https://github.com/gaurav-gs7/Helios) | Durable DAG task orchestration | PostgreSQL source of truth, NATS dispatch, leases, heartbeats, retries, timeout recovery, worker health, GitOps assets, and a PostgreSQL-backed lease-recovery test |
| [Sentinel](https://github.com/gaurav-gs7/Sentinel) | Kubernetes service onboarding and rollout reliability | SLO/error-budget gates, `RolloutGuard` controller, canary rollback, generated golden paths, workflow audit evidence, Kustomize, Argo CD, and Terraform |
| [MCP-Guard](https://github.com/gaurav-gs7/MCP-Guard) | Constraining AI-agent tool calls | JSON-RPC stdio proxy, allowlist policy, signed approvals, redaction, rate limits, kill switches, SQLite audit, bearer-protected dashboard API, and adversarial evals |

## What I optimize for

- Fail closed when evidence, identity, policy, or persistence is uncertain.
- Keep LLMs out of authorization and correctness paths.
- Treat databases as authoritative state and queues as transport.
- Make retries, leases, idempotency, stale work, and crash boundaries explicit.
- Preserve provenance from raw input to decision and audit record.
- Test the infrastructure boundary with real PostgreSQL, NATS, Docker, and
  Kubernetes machinery where the claim depends on it.
- Document non-goals and residual risk as carefully as features.

## Working stack

Go, Python, TypeScript, React, PostgreSQL, DynamoDB, NATS JetStream, Redis, Docker,
Kubernetes, AWS, CDK, Terraform, Kustomize, Argo CD, GitHub Actions, Prometheus,
Grafana, Loki, and OpenTelemetry.

I am interested in SRE, production engineering, platform engineering, systems
development, and AI-infrastructure roles—especially teams building control planes,
release safety, observability, orchestration, or reliable agent infrastructure.
