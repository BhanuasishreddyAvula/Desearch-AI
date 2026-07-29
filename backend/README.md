# Desearch AI Backend

> Production-grade FastAPI backend foundation for Desearch AI.

---

## Purpose

The backend service coordinates application lifecycle events, modular domain settings, standardized API response envelopes, centralized exception handling, HTTP middleware, observability (logging, tracing, metrics, events), dependency injection, abstract repository persistence layers, Supabase PostgreSQL database integration, research session management, production multi-agent AI pipelines (Planner Agent, Research Agent, Writer Agent, Reviewer Agent, Multi-Agent Orchestrator), universal tool registration (`ToolRegistry`), and routing for the **Desearch AI** research workbench.

---

## System Architecture Rules (Frozen Principles)

From Phase 2 onwards, Desearch AI strictly enforces non-bypassable control flow principles:

### Control Flow Hierarchy
```text
API Layer (FastAPI Routers)
         │
         ▼
Multi-Agent Orchestrator (app/orchestrator/)
         │
         ▼
AI Agent Pipeline (Planner -> Research -> Writer -> Reviewer)
         │
         ▼
Universal Tool Registry (app/tools/registry.py)
         │
         ▼
Tool Execution Capabilities (web_search, web_fetch, ...)
```

- **Rule 1**: AI Agents must **never** call each other directly.
- **Rule 2**: API endpoints must **never** coordinate multiple agents directly.
- **Rule 3**: The Orchestrator is the **only** component allowed to sequence and coordinate multi-agent execution flows.
- **Rule 4 (Writer Agent Boundary)**: The Writer Agent MUST NEVER access `ToolRegistry`, `WebSearchTool`, `WebFetchTool`, `DocumentReaderTool`, or `CitationExtractorTool`. Its ONLY source of truth is the structured `ResearchResult` evidence payload.
- **Rule 5 (Reviewer Agent Boundary)**: The Reviewer Agent MUST NEVER access `ToolRegistry`, perform research, or modify the report text. Its ONLY responsibility is quality evaluation and evidence alignment validation.

---

## Reviewer Agent Module

The **Reviewer Agent** (`app/agents/reviewer/`) is the fourth autonomous AI agent in Desearch AI. It evaluates the generated report against the original `PlannerResult` strategy and `ResearchResult` evidence collection.

```text
backend/app/agents/reviewer/
├── __init__.py            # Package re-exports
├── models.py              # ReviewResult domain model
├── prompts.py             # System prompt for rigorous peer review quality evaluation
├── reviewer.py            # ReviewerAgent (Evaluates quality & evidence validity via LLMClient)
├── router.py              # API router (/api/v1/reviewer/review)
├── schemas.py             # Pydantic v2 schemas (ReviewRunRequest, ReviewResultSchema)
└── service.py             # ReviewerService validating session & executing evaluation workflow
```

### Key Responsibilities & Rules

1. **Quality Evaluation Only**: Evaluates report structure, factual accuracy, evidence coverage, and structural completeness. NEVER rewrites or modifies the report text.
2. **Unsupported Claim Detection**: Identifies claims made in the report that lack backing evidence in `ResearchResult`.
3. **Approval Determination**: Sets `approved` to `true` ONLY if `overall_score` >= 0.75 and `unsupported_claims` is empty.
4. **Zero Tool Access**: Does NOT access `ToolRegistry` or perform external research queries.

### API Endpoint (`/api/v1/reviewer/review`)

- **`POST /api/v1/reviewer/review`**:
  - Request Body: `{"session_id": "<uuid>", "plan": {...}, "research": {...}, "report": {...}}`
  - Response: Returns `ReviewEnvelope` wrapping `ReviewResultSchema` containing `approved`, `overall_score`, `confidence`, `strengths`, `issues`, `missing_evidence`, `unsupported_claims`, `recommendations`, and `summary`.

---

## Writer Agent Module

The **Writer Agent** (`app/agents/writer/`) is the third autonomous AI agent in Desearch AI. It receives a `PlannerResult` plan and a structured `ResearchResult` evidence collection, then synthesizes a comprehensive, executive-ready Markdown Research Report.

---

## Multi-Agent Orchestrator Module

The **Multi-Agent Orchestrator** (`app/orchestrator/`) sequences agent workflows across four steps (`PlannerAgent` -> `ResearchAgent` -> `WriterAgent` -> `ReviewerAgent`), tracking execution metrics and aggregating `PlannerResult`, `ResearchResult`, `ReportResult`, and `ReviewResult` into a unified `WorkflowResult` response.

---

## Research Agent Module

The **Research Agent** (`app/agents/research/`) receives a `PlannerResult` plan from the Planner Agent, requests necessary tools strictly through `ToolRegistry`, gathers raw research findings, and structures them into a formal `ResearchResult` evidence collection.

---

## Planner Agent Module

The **Planner Agent** (`app/agents/planner/`) receives a research query from a `ResearchSession` and uses `LLMClient` to construct a structured, multi-step Research Execution Plan.

---

## Universal Tool Registry Module

The **Tool Registry** (`app/tools/`) is the central catalog of every capability available to AI agents. It acts as a metadata directory that tracks tool identities, specifications, input/output JSON schemas, versioning, enabling status, and supported agent roles without performing tool execution.

---

## Universal LLM Platform (OpenRouter Integration)

Desearch AI integrates **OpenRouter** (`app/core/llm/`) as its decoupled, universal LLM platform provider using direct HTTP REST calls (`httpx`). Agents communicate exclusively with the normalized `LLMClient` interface and remain completely decoupled from specific LLM providers or vendor SDKs.

---

## Supabase Persistence

Desearch AI integrates **Supabase PostgreSQL** as its production persistence layer (`app/sessions/supabase_repository.py`). The domain service layer remains 100% untouched due to the repository abstraction pattern established in Ticket P2-02.

---

## Repository Architecture

Desearch AI strictly separates domain business logic from data storage mechanisms using abstract repository interfaces (`app/core/repositories/`). This adheres to SOLID principles (Dependency Inversion), allowing seamless swapping of persistence providers without altering service layer code.

---

## Research Session Module

The Research Session domain (`app/sessions/`) manages the complete lifecycle of research queries across 9 states using an in-memory repository pattern or Supabase PostgreSQL persistence, domain service layer, Pydantic schemas, and FastAPI endpoints.

---

## Application Container

Desearch AI implements a lightweight service container (`app/core/container.py`) to centralize shared infrastructure singletons without global mutable state or heavy third-party DI frameworks.

---

## Dependency Injection Architecture

Dependency Injection in Desearch AI uses FastAPI's native `Depends()` mechanism (`app/dependencies/`). Reusable dependency providers decouple API handlers from infrastructure implementations and enable seamless unit test mocking.

---

## Development Quality Workflow

Desearch AI strictly enforces automated quality control infrastructure across code formatting, linting, static type checking, and Git hooks. All tooling configuration is centralized in `backend/pyproject.toml`.

### Quality Commands (`backend/Makefile`)

```bash
# Format code with Black and isort
make format

# Run Ruff linter checks
make lint

# Run mypy strict static type checking
make typecheck

# Run complete quality suite (format, lint, typecheck)
make quality
```

---

## Setup & Local Development

### 1. Create Virtual Environment

```cmd
cd backend
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run Development Server

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
