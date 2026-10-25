<a href="https://gaurav-gs7.pages.dev"><img src="https://gaurav-gs7.pages.dev/og.jpg" alt="Gaurav G S, Senior Site Reliability Engineer: AI infrastructure and payments at scale. Visit gaurav-gs7.pages.dev" width="100%"></a>

# Gaurav G S

Senior Site Reliability Engineer at Mastercard. Previously PhonePe, on UPI.

**Portfolio: [gaurav-gs7.pages.dev](https://gaurav-gs7.pages.dev)**. Break a live payments stack and watch my projects heal it.

[LinkedIn](https://www.linkedin.com/in/gaurav-g-s-9a7495180/) · [Medium](https://medium.com/@ngs.gaurav7195) · [Email](mailto:ngs.gaurav7195@gmail.com)

Four years running payment and banking infrastructure: on-call, zero-downtime migrations, disaster-recovery drills, and the automation that makes them boring. On the side, I build open-source control planes that let AI take part in operations without taking the controls.

> LLMs advise. Deterministic systems decide. Policy gates. Audits prove.

## Production work

- **Mastercard** (Apr 2025 – now). Reliability for the FLS/BRAM platform, used by global banks in a business line worth $77M+ a year. Release automation in Jenkins and XLR, incident triage across Splunk, deployment and database signals, and recovery of corrupted financial data during incidents.
- **PhonePe** (Aug 2022 – Apr 2025). Bank PSP infrastructure for UPI, on a platform handling 360M+ transactions a day. Migrated Yes Bank's PSP orchestration from Mesos to Drove and moved Axis Bank and Yes Bank between data centers, both with zero downtime. Made MariaDB backup verification 33% faster with SaltStack.

## Projects

### [Judikt](https://github.com/gaurav-gs7/Judikt): security gateway for AI agents using MCP

Sits between AI agents and the tools they call. Every call passes policy-as-code, OAuth/JWT identity, risk scoring, human approvals, rate limits and kill switches, and lands in a hash-chained audit trail. Tool responses are treated as untrusted input. Ships AttackBench for testing prompt-injection defences.

**Status:** v0.3.0 on [PyPI](https://pypi.org/project/judikt/) (`pip install judikt`). [How and why I built it](https://medium.com/@ngs.gaurav7195/i-built-verdikt-a-security-and-reliability-control-plane-for-ai-agents-using-mcp-2580b5835abc).

### [Argus](https://github.com/gaurav-gs7/Argus): incident correlation and RCA, with AI kept advisory

Groups alerts into one incident by walking the service topology, then scores root causes deterministically before an LLM is allowed to explain anything. Fixes are typed, idempotent and policy-gated, and every decision is written to a PostgreSQL audit trail.

**Stack:** Go, PostgreSQL, NATS, Redis, Prometheus, Grafana, Loki, OpenTelemetry

### [Attesta](https://github.com/gaurav-gs7/Attesta): Kubernetes reliability control plane

Onboards services with owners, SLOs, runbooks and rollback policy, scores their production readiness, guards progressive rollouts and rolls back when a release breaches its SLO. Generates the Terraform, Argo CD, Kustomize, alerting and tracing config a new service needs. (Formerly Sentinel.)

**Stack:** Go, Kubernetes, Argo CD, Terraform, Alertmanager, OpenTelemetry

### [InferLab](https://github.com/gaurav-gs7/InferLab): release checks for LLM inference changes

A benchmark can say an inference change is faster without proving the evidence is complete, comparable, or safe to release on. InferLab checks the evidence first, then returns `PASS`, `BLOCK` or `INCONCLUSIVE`: versioned contracts for the exact model, runtime and workload; freshness, coverage and sample-sufficiency checks; re-verification of the smallest workload that reproduces a failure; and replayable safety cases signed with Ed25519.

**Status:** pre-alpha. The public examples deliberately show `BLOCK` and `INCONCLUSIVE`; I don't claim a production `PASS` without real target-system evidence.

### [Helios](https://github.com/gaurav-gs7/Helios): durable workflow engine (learning project)

A hands-on deep dive into durable execution: DAG workflows with PostgreSQL as the source of truth and NATS for dispatch, worker leases and heartbeats, retries with backoff, and dead-worker recovery. Built to learn the mechanics, not a production claim.

## Stack

- **Languages:** Go, Python, Bash
- **Platform:** Linux, Kubernetes, Docker, Terraform, Argo CD, GitHub Actions, Jenkins, Nginx, HAProxy
- **Data:** PostgreSQL, MariaDB, Redis, NATS, ZooKeeper
- **Observability:** Prometheus, Grafana, Splunk, OpenTelemetry, Jaeger
- **Cloud:** AWS, GCP

## Open to

SRE, platform engineering and AI-infrastructure roles, remote or hybrid in Bengaluru.
