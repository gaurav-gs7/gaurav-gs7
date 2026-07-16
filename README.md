<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&height=180&color=0:0F172A,50:1E40AF,100:14B8A6&text=Gaurav%20G%20S&fontColor=FFFFFF&fontSize=46&fontAlignY=38&desc=SRE%20%7C%20Platform%20Engineering%20%7C%20AI%20Infra%20%7C%20AIOps&descAlignY=60&animation=fadeIn" />

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Inter&weight=600&size=22&duration=2800&pause=800&color=38BDF8&center=true&vCenter=true&width=900&lines=I+build+reliability+and+platform+systems;I+care+about+failure+modes%2C+clear+boundaries%2C+and+good+evidence;Currently+working+on+AI+infrastructure+and+release+safety)](https://git.io/typing-svg)

</div>

<p align="center">
  <a href="https://github.com/gaurav-gs7">
    <img src="https://img.shields.io/badge/GitHub-gaurav--gs7-181717?style=for-the-badge&logo=github" />
  </a>
  <a href="https://www.linkedin.com/in/gaurav-g-s-9a7495180/">
    <img src="https://img.shields.io/badge/LinkedIn-Gaurav%20G%20S-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" />
  </a>
  <a href="mailto:ngs.gaurav7195@gmail.com">
    <img src="https://img.shields.io/badge/Gmail-ngs.gaurav7195@gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white" />
  </a>
  <a href="https://medium.com/@ngs.gaurav7195">
    <img src="https://img.shields.io/badge/Medium-%40ngs.gaurav7195-000000?style=for-the-badge&logo=medium&logoColor=white" />
  </a>
</p>

---

<img align="right" width="240" src="https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif" alt="systems engineering gif" />

## 👋 About Me

I build reliability and platform systems, usually around the points where failures
become hard to explain: an alert turns into an incident, a worker disappears with
a task, a rollout crosses an SLO boundary, or an AI agent asks to run a risky tool.

I like working close to those mechanics—leases, retries, duplicate delivery,
idempotency, audit records, and rollback state. My recent projects cover incident
response, Kubernetes delivery, workflow orchestration, AWS deployments, inference
release checks, and tool-call safety.

The rule I try to follow is:

> AI can help explain the evidence. Deterministic code should make the decision,
> policy should control mutations, and the audit trail should show what happened.

---

## 🚀 Current Focus

<table>
<tr>
<td width="50%">

### Reliability Engineering
- Incident intake, grouping, and recovery
- SLO-aware rollout and rollback decisions
- Durable state, retries, leases, and stale work
- Runbooks and evidence that can be reproduced

</td>
<td width="50%">

### AI Infrastructure
- Release checks for inference changes
- Safe boundaries around agent tool calls
- Evaluation, tracing, and provenance
- Keeping models out of authorization paths

</td>
</tr>
</table>

---

## 🧠 Featured Projects

Here are the projects I have spent the most time on. They are at different stages,
and I have called out the unfinished parts where they matter.

### 1. [InferLab](https://github.com/gaurav-gs7/InferLab) — Release Checks for LLM Inference Changes

I built InferLab because a faster benchmark result is not automatically trustworthy
release evidence. The model may be different, the workload may be too small, or the
runtime and hardware may no longer match the baseline.

InferLab checks those conditions before returning `PASS`, `BLOCK`, or
`INCONCLUSIVE`. It uses versioned contracts, coverage and freshness checks,
loss-aware adapters, counterexample re-verification, and replayable safety cases
that can be signed with Ed25519.

It is still pre-alpha. The public examples deliberately show `BLOCK` and
`INCONCLUSIVE`; I do not claim a production `PASS` without evidence from the
target system. The quickest way to inspect the full path is `make demo-safety-case`.

---

### 2. [Argus](https://github.com/gaurav-gs7/Argus) — Incident Response Control Plane

Argus started with one constraint: an LLM should not decide whether production is
changed. It can help explain an incident, but the evidence, policy, approval, and
remediation path stay deterministic.

The system groups alerts into incidents, builds a timeline, runs deterministic RCA,
and records remediation decisions in PostgreSQL. NATS JetStream carries work, while
Prometheus, Grafana, Loki, and OpenTelemetry expose what the control plane is doing.
The integration suite exercises real PostgreSQL grouping and audit behavior as well
as JetStream delivery.

Run `make ci` for the local quality gate and `make integration-test` for the
database and queue boundaries.

---

### 3. [CloudDock](https://github.com/gaurav-gs7/CloudDock) — AWS Deployment Control Plane

CloudDock came from a question I kept returning to: after a deployment goes wrong,
can we prove what changed, why it was allowed, how health was checked, and exactly
what the rollback restored?

It follows a GitHub revision through CodeBuild, ECR, ECS Fargate, ALB health checks,
and Step Functions. DynamoDB conditional writes protect state transitions; KMS and
team RBAC protect credentials and access. Each deployment produces a release
passport tying together source identity, health evidence, audit events, cost, and
rollback lineage.

`make verify` runs the clean-clone gate and CDK synthesis. That proves the
implementation is reproducible; it is not a claim that I have already operated
CloudDock as a production AWS service.

---

### 4. [Helios](https://github.com/gaurav-gs7/Helios) — Durable Workflow Orchestration

Helios is where I worked through the failure mechanics behind a distributed workflow
engine. PostgreSQL is the source of truth, NATS is transport, and workers coordinate
through registrations, heartbeats, leases, retries, and timeouts.

The interesting part is not drawing a DAG. It is deciding what happens when a lease
expires, a worker finishes stale work, a retry budget is exhausted, or the control
plane restarts. The PostgreSQL integration test covers those recovery paths against
a real database.

Run `make integration-test` to reproduce the lease-recovery checks.

---

### 5. [Sentinel](https://github.com/gaurav-gs7/Sentinel) — Kubernetes Reliability Platform

Sentinel combines a service catalog and golden path with SLO checks, error-budget
gates, canary decisions, and a Kubernetes `RolloutGuard` controller. It generates
deployment assets with Kustomize and Argo CD patterns and records the workflow state
behind readiness and rollout decisions.

One boundary is intentionally explicit: the embedded workflow runner persists
snapshots, but it is not yet crash-resumable from the last completed step. Persistence
failures now stop the operation instead of being ignored.

The root CI gate runs formatting, vet, race tests, builds, CRD rendering, and
controller rendering.

---

### 6. [MCP-Guard](https://github.com/gaurav-gs7/MCP-Guard) — Guardrails for Agent Tool Calls

MCP-Guard is a smaller project with a narrow job: sit between an agent and its tools,
then make the risky parts visible and controllable. It applies allowlist policy,
signed approvals, redaction, rate limits, kill switches, and audit logging before a
tool call is allowed through.

The dashboard requires bearer authentication when it is exposed beyond loopback,
and the test suite covers the HTTP boundary as well as adversarial inputs. The
current gateway is still a local JSON-RPC stdio implementation, not a distributed
production MCP gateway.

Run `PYTHONPATH=src python3 -m unittest discover -s tests -v` to exercise it.

---

## 🛠️ Tech Stack

<div align="center">

### Languages
<img src="https://skillicons.dev/icons?i=go,python,bash" />

### Infra / Platform
<img src="https://skillicons.dev/icons?i=docker,kubernetes,terraform,githubactions,nginx,linux" />

### Data / Messaging
<img src="https://skillicons.dev/icons?i=postgres,redis,kafka,rabbitmq" />

### Cloud / DevOps
<img src="https://skillicons.dev/icons?i=aws,gcp,git,github,vscode" />

</div>

---

## 📌 How I Think About Reliability

- If state cannot be persisted, the operation should fail instead of pretending it
  succeeded.
- A database is authoritative state; a queue is transport and may deliver twice.
- Retries, lease expiry, stale work, and partial failure belong in the normal design.
- Production mutations need explicit policy and approval boundaries.
- Logs and dashboards are useful, but reproducible evidence and audit records are
  what let someone verify a claim later.
- I would rather document a limitation clearly than call an unfinished system
  production-ready.

---

## 📚 What I Am Working On Next

- Run InferLab against a pinned inference stack and publish the raw baseline and
  candidate evidence.
- Record a fresh Argus failure demo from alert ingestion through recovery and audit
  closure.
- Add a kind-based controller test to Sentinel for status updates, events, and
  rollback behavior.
- Complete CloudDock's AWS acceptance matrix with deployment, rollback, teardown,
  timing, and cost evidence.

---

## 📊 GitHub Snapshot

<div align="center">

<img height="165" src="https://github-readme-stats.vercel.app/api?username=gaurav-gs7&show_icons=true&hide_border=true&theme=tokyonight" />
<img height="165" src="https://github-readme-streak-stats.herokuapp.com/?user=gaurav-gs7&hide_border=true&theme=tokyonight" />

<br/>

<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=gaurav-gs7&layout=compact&hide_border=true&theme=tokyonight" />

</div>

---

## 🤝 Open To

I am interested in SRE, production engineering, platform engineering, systems
development, and AI-infrastructure roles—especially work involving control planes,
distributed failure handling, release safety, observability, or reliable agent
infrastructure.

---

<div align="center">

### I like systems that stay understandable when they fail.

<img src="https://capsule-render.vercel.app/api?type=waving&height=110&color=0:14B8A6,50:1E40AF,100:0F172A&section=footer" />

</div>
