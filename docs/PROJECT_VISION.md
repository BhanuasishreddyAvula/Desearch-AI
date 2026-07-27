# Project Vision — Desearch AI

> Product: **Desearch AI** — Deep Research. Smarter Decisions.
> Derived from: Original `Docs/PROJECT_VISION.md` (AI Agent Platform)
> Updated: TICKET-007 — Product repositioning to Desearch AI
> Updated: Consistency Pass — Product non-goals, canonical example, terminology
> Status: Baseline

---

## Problem Statement

Organizations and professionals conducting complex research face a consistent productivity gap: meaningful research requires planning, source validation, multi-source synthesis, and structured output — all of which are beyond what single-prompt AI chatbots or conventional search engines can provide.

Real-world research tasks — technology comparisons, competitive analyses, architecture evaluations, market investigations, academic surveys — are inherently multi-step and require coordinated behavior across multiple cognitive roles: a planner to scope the work, a researcher to gather information, a fact-checker to validate sources, a writer to structure findings, and a reviewer to ensure quality. Current tools either delegate all of this to a single LLM call (producing shallow, unverifiable output) or leave the coordination work entirely to the human.

Desearch AI addresses that gap by providing a deployable, cloud-native multi-agent research platform that structures the research process through specialized agents, grounded tool use, persistent research session context, and optional human oversight — producing research reports that are structured, sourced, and auditable.

---

## Target Users

**Primary**

- AI Engineers and Software Engineers who need deep, structured technical research on frameworks, architectures, tools, and APIs.
- Researchers and Students conducting academic topic investigations and literature surveys.
- Startup Founders evaluating technology stacks, competitive landscapes, and market opportunities.
- Product Managers performing product comparison, feature benchmarking, and competitive analysis.
- Technical Consultants preparing client-facing research reports and technology assessments.

**Secondary**

- Business Analysts conducting market research and business intelligence tasks.
- Enterprise Teams evaluating vendor solutions, platforms, or architectural approaches before committing resources.
- Educators assembling structured, sourced content for curriculum and course material.

---

## Vision

Desearch AI aims to be a production-grade, cloud-native AI research workbench that orchestrates multiple specialized agents to produce structured, verified, exportable research reports for complex real-world research queries.

The long-term vision is a self-hostable research platform where users can submit a research query and receive a fully structured research report — planned, researched, fact-checked, written, and reviewed by a coordinated pipeline of specialized AI agents. The platform is designed to be model-agnostic, provider-agnostic, and extensible — capable of integrating new research tools, memory backends, output formats, and LLM providers without requiring architectural changes.

Desearch AI serves as both a functional research product and a public engineering reference: demonstrating how multi-agent orchestration, tool grounding, observability, and human oversight are built into a system designed for real-world use rather than demonstration purposes.

---

## Core Value Proposition

Single-agent AI tools, basic chatbot interfaces, and isolated LLM API wrappers share a fundamental limitation when applied to research tasks: they are stateless, single-step, and unverified. They perform no source validation, no research planning, no iterative refinement, and no structured output generation. They produce a plausible-sounding response — not a research report.

Desearch AI is built for users who need more:

- **Research pipeline orchestration** — a Planner Agent scopes the research query, produces an ordered execution plan, and the Orchestrator coordinates the pipeline through to a finished report.
- **Tool-grounded research** — agents invoke real external tools (web search, web page reader, document reader) to gather findings from live, verifiable sources rather than model memory alone.
- **Persistent research session context** — session-scoped memory allows findings produced by the Research Agent to be read by the Fact Checker, Writer, and Reviewer without manual handoff.
- **Observability** — structured logging, execution tracing, and audit trails covering every agent invocation, tool call, and LLM request — making the research process fully transparent and auditable.
- **Extensibility** — a modular design that allows new research agents, output formats, and tool integrations to be added without rearchitecting the system.
- **Human oversight** — configurable approval checkpoints that allow users to review, approve, or redirect agent decisions before the research pipeline continues.

Desearch AI is not a chatbot. It is a research operating system.

---

## MVP Scope

The following features constitute the first release:

- **Planner Agent** — Receives the research query, produces a structured ordered execution plan, and writes it to research session context for the Orchestrator and downstream agents.
- **Research Agent** — Gathers information from external sources using registered tools (web search, web page reader, document reader) and writes sourced findings to research session context.
- **Fact Checker Agent** — Validates key claims and sources in the Research Agent's findings; scores claim confidence; flags unsupported assertions before the Writer Agent receives the validated findings.
- **Writer Agent** — Synthesizes validated findings from research session context into a structured research report conforming to the defined report output schema.
- **Reviewer Agent** — Evaluates the Writer Agent's report against defined quality criteria; approves the output or returns structured improvement feedback.
- **Tool Registry** — At least three external tools available to agents: web search, web page reader, and document reader.
- **Output Formatter** — Renders the completed research report into at least one exportable format (Markdown) upon research session completion.
- **Research Session Context** — Short-term, session-scoped memory allowing all agents to read findings and context produced by prior agents.
- **Research Execution API** — An endpoint that accepts a research query, runs the full agent pipeline, and returns a structured research report.
- **Structured Logging** — Every agent invocation, tool call, and LLM request logged with timestamps, agent identity, and token usage.
- **Research Workbench Frontend** — A functional web interface where users can submit research queries, monitor the research pipeline, review agent outputs, and inspect execution traces.
- **Cloud Deployment** — The full system deployed and accessible via a public URL using free-tier cloud services.
- **LLM Provider Integration** — Integration with at least one free-tier or low-cost LLM provider API.
- **Human-in-the-Loop Approval** — Configurable approval checkpoints allowing users to review, approve, reject, or retry agent outputs at critical pipeline stages (after the Planner Agent's execution plan and after the Fact Checker Agent's validated findings).

---

## Out of Scope

The following will not be built as part of the MVP:

- Local or self-hosted LLM inference.
- Paid, production-tier API subscriptions as a hard dependency.
- Fine-tuning or model training of any kind.
- Voice or audio interfaces.
- Multi-tenant user management and authentication beyond a basic API key.
- Real-time collaborative research sessions or shared workspaces.
- Mobile applications.
- SLA-backed production infrastructure or on-call operations.
- Plugin marketplaces or third-party agent registries.
- Automated billing or usage metering.
- PDF export (deferred to a future iteration; Markdown export only in MVP).

---

## Product Non-Goals

The following are explicit non-goals. They define what Desearch AI will never attempt to be, regardless of future development, to prevent scope creep and preserve product clarity:

- **Not a general-purpose AI assistant or chatbot.** Desearch AI does not answer casual questions or engage in open-ended conversation. Every research session is a structured, bounded workflow with a defined terminal state.
- **Not a search engine replacement.** Desearch AI does not index the web or produce ranked result lists. It produces structured research reports by synthesizing information from external sources.
- **Not a real-time web monitoring service.** Desearch AI does not track changes to web content, alert on new developments, or maintain standing subscriptions to external data sources.
- **Not a fact database or knowledge graph.** Desearch AI does not maintain a persistent, queryable store of verified facts. Research session context is scoped to a single session and archived after completion.
- **Not a plagiarism checker or compliance tool.** Desearch AI does not evaluate documents against copyright databases, legal corpora, or regulatory standards.
- **Not a financial advisory or legal research tool.** Desearch AI does not provide regulated professional advice. Research outputs are decision-support materials, not authoritative professional judgements.
- **Not a multi-language platform.** Research queries and outputs are in English only in the MVP and planned iterations unless explicitly scoped as a future capability.
- **Not a document management system.** Desearch AI does not store, organize, or retrieve user-uploaded documents. Document reader tool access is limited to publicly accessible content.

---

## Success Criteria

The MVP is considered successful when all of the following are true:

1. A user can submit a research query (e.g., "Compare Supabase vs Firebase for Enterprise SaaS") and receive a structured research report produced by the five-agent pipeline — not a single LLM call.
2. The execution trace for every completed research session is logged and retrievable, showing which agent acted, which tools were called, and what the LLM received and returned at each step.
3. The full system is deployed and publicly accessible without requiring local setup by an external evaluator.
4. The deployment is reproducible from a clean environment using documented steps in under 30 minutes.
5. The system completes at least three distinct research queries end-to-end without manual intervention.
6. The system handles agent failures gracefully — logging the error and either retrying or returning a structured error response rather than an unhandled exception.

---

## Resume Positioning

Desearch AI demonstrates applied AI engineering across the full stack of a production research system: multi-agent pipeline design, orchestration logic, tool grounding, research session context management, observability, and cloud deployment. These are the skills that distinguish an AI Engineer from a developer who can call an API. Building this platform requires real engineering decisions — how to coordinate five specialized agents without direct inter-agent communication, how to handle partial research failures mid-pipeline, how to maintain LLM context within token limits across a five-step research workflow — the kind of decisions that appear in production AI systems at serious engineering organizations.

For an AI Engineer targeting roles in applied AI, LLM infrastructure, or agent systems, Desearch AI provides concrete, evaluable evidence: not a chatbot wrapper, but a structured multi-agent research system with observable behavior, defined failure modes, a documented engineering rationale, and a publicly deployed, interactive demonstration.
