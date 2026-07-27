# Desearch AI — AI Research & Workbench

> **Tagline:** Deep Research. Smarter Decisions.  
> **Description:** Production-grade AI Research Workbench built using a modular multi-agent orchestration architecture.

---

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg?style=flat-square)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![Release Version](https://img.shields.io/badge/version-0.1.0-orange.svg?style=flat-square)](CHANGELOG.md)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg?style=flat-square)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=flat-square)](https://www.python.org/)

---

## Executive Summary & Vision

Organizations and technical professionals face a critical productivity bottleneck when performing complex technical or business research: meaningful research requires scoping, source validation, multi-source synthesis, and structured output. Single-prompt AI chatbots and search engines produce shallow, unverified, or hallucinated responses because they lack multi-step reasoning, external tool grounding, and systematic factual verification.

**Desearch AI** solves this gap by providing an open, cloud-native AI Research Workbench. Instead of delegating a complex query to a single LLM call, Desearch AI coordinates a **five-agent pipeline** (Planner, Research, Fact Checker, Writer, Reviewer) operating over a shared research session context with external tool grounding and human-in-the-loop oversight.

### Canonical Research Query Benchmark
> *"Compare Supabase vs Firebase for Enterprise SaaS"*

---

## Key Features (Planned MVP)

- **Five-Agent Orchestration Pipeline**:
  - **Planner Agent**: Scopes research queries and generates structured, subtask-based execution plans.
  - **Research Agent**: Gathers live source material using external tools (Web Search, Page Reader, Document Reader).
  - **Fact Checker Agent**: Validates claims against source snippets, detects contradictions, and assigns confidence scores.
  - **Writer Agent**: Synthesizes validated findings into structured Markdown research reports adhering to a strict schema.
  - **Reviewer Agent**: Evaluates reports against 7 measurable quality criteria before final delivery.
- **Tool-Grounded Research**: Real web search, web page reading, and document retrieval to prevent hallucinations.
- **Isolated Research Session Context**: Short-term, session-scoped context exchange across agents without direct inter-agent coupling.
- **Human-in-the-Loop (HITL) Checkpoints**: Durable approval checkpoints (`AWAITING_PLAN_APPROVAL` and `AWAITING_FACTCHECK_APPROVAL`) allowing users to review, approve, or retry agent steps.
- **Report Confidence Model**: Multi-tier confidence scoring (HIGH, MEDIUM, LOW) propagated from individual claims to sections and full reports.
- **Full Observability & Execution Tracing**: Schema-enforced structured logging and per-session execution trace viewer.
- **Exportable Reports**: Standalone Markdown export rendered via an isolated Output Formatter component.

---

## Architecture Overview

Desearch AI separates execution management from cognitive research planning:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          Desearch AI Workbench                           │
│                                                                          │
│  ┌────────────────────────┐            ┌──────────────────────────────┐  │
│  │ Research Workbench UI  │◄──────────►│          API Layer           │  │
│  │  (Next.js / Frontend)  │            │      (FastAPI Backend)       │  │
│  └────────────────────────┘            └──────────────┬───────────────┘  │
│                                                       │                  │
│                                           ┌───────────▼──────────────┐   │
│                                           │       Orchestrator       │   │
│                                           │  (Execution Coordinator) │   │
│                                           └───┬───────────────────┬──┘   │
│                                               │                   │      │
│                    ┌──────────────────────────▼───┐    ┌──────────▼───┐  │
│                    │         Agent Layer          │    │ Research     │  │
│                    │ Planner · Research · FactChk │    │ Session      │  │
│                    │     Writer · Reviewer        │    │ Context      │  │
│                    └──────────────┬───────────────┘    └──────────────┘  │
│                                   │                                      │
│                    ┌──────────────▼──────────────┐                       │
│                    │         Tool Layer          │                       │
│                    │ WebSearch · PageReader · Doc│                       │
│                    └─────────────────────────────┘                       │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ Persistence Layer & Output Formatter (Markdown / Traces / Audit)   │  │
│  └────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────┘
```

### Research Session State Machine
```text
SUBMITTED ──► PLANNING ──► [AWAITING_PLAN_APPROVAL] ──► RESEARCHING ──► FACT_CHECKING
                                                                             │
COMPLETED ◄── REVIEWING ◄── WRITING ◄── [AWAITING_FACTCHECK_APPROVAL] ◄──────┘
```

For complete architectural details, see [`docs/SYSTEM_ARCHITECTURE.md`](docs/SYSTEM_ARCHITECTURE.md) and [`docs/ENGINEERING_DECISIONS.md`](docs/ENGINEERING_DECISIONS.md).

---

## Repository Structure

```text
Desearch AI/
├── .github/              # GitHub Actions CI/CD workflows and issue templates
├── .vscode/              # Recommended IDE workspace settings and launch configurations
├── backend/              # Python FastAPI microservices & Agent orchestration core
├── frontend/             # Next.js / React interactive Research Workbench UI
├── docs/                 # Architectural specifications, EDRs, and implementation tickets
│   ├── PROJECT_VISION.md
│   ├── REQUIREMENTS.md
│   ├── SYSTEM_ARCHITECTURE.md
│   ├── ENGINEERING_DECISIONS.md
│   ├── IMPLEMENTATION_PLAN.md
│   ├── RESUME_SOURCE.md
│   └── CHANGELOG_CONSISTENCY_PASS.md
├── infrastructure/       # Cloud infrastructure-as-code and configuration scripts
├── scripts/              # Local development setup, diagnostic, and utility scripts
├── .editorconfig         # Code formatting standards across IDEs
├── .env.example          # Template for environment variables and service credentials
├── .gitattributes        # Git line ending normalization rules
├── .gitignore            # Master git ignore patterns (Python, Node, IDEs, OS, Secrets)
├── CHANGELOG.md          # Project version history (Keep a Changelog standard)
├── CODE_OF_CONDUCT.md    # Contributor Covenant v2.1
├── CONTRIBUTING.md       # Development workflow, branch strategy & commit rules
├── LICENSE               # MIT Open Source License
├── README.md             # Project overview & engineering documentation
└── SECURITY.md           # Security disclosure policy and vulnerability guidelines
```

---

## Technology Stack (Planned)

| Layer | Technology | Rationale |
| ----- | ---------- | --------- |
| **Frontend** | Next.js 14, React 18, TypeScript, Tailwind CSS | Fast rendering, strict typing, responsive research workbench interface. |
| **Backend API** | Python 3.11+, FastAPI, Pydantic v2 | High performance, async support, native data validation. |
| **Agent Core** | LangChain / Custom Agent Framework | Stateless, role-bounded agent dispatch loop. |
| **Database & Auth** | Supabase (PostgreSQL), Row Level Security | Managed PostgreSQL, authentication, and durable audit storage. |
| **Memory / Cache** | In-Memory / Redis Context Store | Session-scoped context storage with fast read/write access. |
| **LLM Provider API**| Google Gemini / OpenAI / Anthropic API | Provider-agnostic inference layer abstraction. |
| **Observability** | Structured JSON Logging, OpenTelemetry | Schema-enforced logs and per-session execution tracing. |

---

## Development Roadmap

- [x] **Milestone 1 — Core Architecture & Standards (`TICKET: P1-01`)**: Repository foundation, standards, specifications, git conventions.
- [ ] **Milestone 2 — FastAPI Backend Setup & Foundation**: Base application, middleware, API router setup.
- [ ] **Milestone 3 — Functional Research Orchestration & LLM Layer**: Orchestrator core and 5 agent stubs connected to LLM provider.
- [ ] **Milestone 4 — Research Agents with Tools & Session Memory**: Tool integration (Web Search, Page Reader, Doc Reader) and session context manager.
- [ ] **Milestone 5 — Human-in-the-Loop (HITL) Checkpoint Layer**: Approval checkpoint engine and persistence.
- [ ] **Milestone 6 — Observability, Tracing & Logging**: Structured logging and trace export endpoints.
- [ ] **Milestone 7 — Research Workbench Frontend**: Next.js interface for query submission, pipeline tracking, and report viewing.
- [ ] **Milestone 8 — Cloud Deployment & Free-Tier Verification**: Cloud deployment and 30-minute clean setup verification.
- [ ] **Milestone 9 — Production Verification & Acceptance**: End-to-end testing with canonical queries.

---

## Getting Started (Placeholder)

*Note: Application code implementation begins in Milestone 2. Follow the steps below for repository setup.*

### Prerequisites
- **Git** 2.40+
- **Python** 3.11+
- **Node.js** 18.x or 20.x LTS
- **npm** 9.x+

### Repository Setup
```bash
# Clone the repository
git clone https://github.com/BhanuasishreddyAvula/Desearch-AI.git
cd Desearch-AI

# Inspect environment variables template
cp .env.example .env
```

---

## Repository Conventions

- **Branch Naming**: `feature/<name>`, `bugfix/<name>`, `hotfix/<name>`, `release/<version>`
- **Commit Messages**: Conventional Commits specification (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `build:`, `ci:`)
- **Versioning**: Semantic Versioning 2.0.0 (`MAJOR.MINOR.PATCH`)

For complete contribution standards, please refer to [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## Product Non-Goals

To maintain scope discipline, Desearch AI explicitly is **NOT**:
1. A general-purpose AI assistant or chatbot.
2. A search engine replacement.
3. A real-time web monitoring or alerting service.
4. A persistent knowledge graph or database of facts.
5. A plagiarism checker or legal/financial advisory service.

For full details, see [`docs/PROJECT_VISION.md`](docs/PROJECT_VISION.md).

---

## Screenshots Placeholder

```text
+--------------------------------------------------------------------------+
|  [Desearch AI Workbench UI Screenshot Placeholder]                       |
|  Query: "Compare Supabase vs Firebase for Enterprise SaaS"               |
|  Active Step: FACT_CHECKING (Fact Checker Agent validating 5 sources)    |
+--------------------------------------------------------------------------+
```

---

## Deployment Placeholder

```text
+--------------------------------------------------------------------------+
|  [Cloud Infrastructure Deployment Topology Placeholder]                  |
|  Frontend: Cloud Static Hosting (HTTPS)                                  |
|  Backend API & Orchestrator: Managed Container Service / Serverless      |
|  Persistence: Supabase PostgreSQL Managed Instance                       |
+--------------------------------------------------------------------------+
```

---

## Contributing

We welcome community contributions! Please read our [`CONTRIBUTING.md`](CONTRIBUTING.md) guide and [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) before submitting pull requests.

---

## License

This project is licensed under the **MIT License** — see the [`LICENSE`](LICENSE) file for details.
