# Desearch AI Backend

> Production-grade FastAPI backend foundation for Desearch AI.

---

## Purpose

The backend service coordinates application lifecycle events, modular domain settings, standardized API response envelopes, centralized exception handling, HTTP middleware, observability (logging, tracing, metrics, events), dependency injection, abstract repository persistence layers, Supabase PostgreSQL database integration, research session management, production multi-agent AI pipelines (Planner Agent, Research Agent, Writer Agent, Reviewer Agent, Multi-Agent Orchestrator), real search & web content extraction tools (`SearchTool` via Exa, `ContentTool` via Firecrawl), universal tool registration (`ToolRegistry`), real-time research progress streaming with Server-Sent Events (`POST /api/v1/orchestrator/stream`), deterministic report exports (Markdown `.md` and PDF `.pdf`), and routing for the **Desearch AI** research workbench.

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
Production Tool Providers
  ├─ SearchTool  -> ExaProvider      -> Exa API (https://api.exa.ai)
  └─ ContentTool -> FirecrawlProvider -> Firecrawl API (https://api.firecrawl.dev)
```

- **Rule 1**: AI Agents must **never** call each other directly.
- **Rule 2**: API endpoints must **never** coordinate multiple agents directly.
- **Rule 3**: The Orchestrator is the **only** component allowed to sequence and coordinate multi-agent execution flows.
- **Rule 4 (Writer Agent Boundary)**: The Writer Agent MUST NEVER access `ToolRegistry` or search/fetch tools. Its ONLY source of truth is the structured `ResearchResult` evidence payload.
- **Rule 5 (Reviewer Agent Boundary)**: The Reviewer Agent MUST NEVER access `ToolRegistry`, perform research, or modify the report text. Its ONLY responsibility is quality evaluation and evidence alignment validation.
- **Rule 6 (Tool Provider Boundary)**: AI Agents MUST NEVER communicate directly with Exa or Firecrawl. Agents request tools ONLY through `ToolRegistry`.
- **Rule 7 (Export Boundary)**: Report generation and report export are separate responsibilities. Report export is a 100% deterministic formatting operation that MUST NOT invoke LLMs or external search/content APIs.
- **Rule 8 (Streaming Boundary)**: Streaming concerns (SSE, HTTP headers, FastAPI `StreamingResponse`) MUST remain decoupled from agent business logic. Agents emit domain progress events via listener callbacks without knowing about transport layers.

---

## Real-Time Progress Streaming (SSE)

The backend provides Server-Sent Events (SSE) progress streaming via `POST /api/v1/orchestrator/stream`.

- **Endpoint**: `POST /api/v1/orchestrator/stream`
- **Media Type**: `text/event-stream`
- **Shared Business Logic**: Both `POST /orchestrator/run` and `POST /orchestrator/stream` execute identical underlying business logic via `MultiAgentOrchestrator`.
- **Event Vocabulary & Progress Percentages**:
  - `workflow.started` (0%)
  - `planner.started` (5%) -> `planner.completed` (15%)
  - `research.started` (20%) -> `research.searching` (25%) -> `research.extracting` (40%) -> `research.completed` (60%)
  - `writer.started` (65%) -> `writer.completed` (80%)
  - `reviewer.started` (85%) -> `reviewer.completed` (95%)
  - `report.persisted` (98%)
  - `workflow.completed` (100%)
  - `workflow.failed` (100% on exception)

---

## Report Export Module (`app/export/`)

The **Report Export Service** (`ReportExportService`) formats completed research reports into downloadable Markdown (`.md`) or PDF (`.pdf`) documents.

- **Endpoint**: `GET /api/v1/reports/{session_id}/export?format=markdown` or `format=pdf`
- **Formatters**:
  - `MarkdownExportFormatter`: Formats canonical report text into UTF-8 encoded `.md` documents.
  - `PdfExportFormatter`: Formats report title, executive summary, headings, paragraphs, and citations into professional binary `.pdf` documents using ReportLab.
- **Persistence**: Persists canonical `ReportResult` data in Supabase `research_sessions` metadata column upon workflow completion.

---

## Real Search & Content Tool Architecture

### 1. Search Tool Module (`app/tools/search/`)

The **Search Tool** (`SearchTool`) executes web search queries via the `ExaProvider` HTTP REST integration (`POST https://api.exa.ai/search`).

- **Provider**: `ExaProvider` (`app/tools/search/provider.py`)
- **Key Settings**: `EXA_API_KEY`, `EXA_BASE_URL`, `SEARCH_TIMEOUT`
- **Output Model**: `SearchResult` containing normalized `SearchResultItem` items (`title`, `url`, `snippet`, `published_at`, `score`, `metadata`).

### 2. Content Tool Module (`app/tools/content/`)

The **Content Tool** (`ContentTool`) extracts clean web page content and Markdown via the `FirecrawlProvider` HTTP REST integration (`POST https://api.firecrawl.dev/v1/scrape`).

- **Provider**: `FirecrawlProvider` (`app/tools/content/provider.py`)
- **Key Settings**: `FIRECRAWL_API_KEY`, `FIRECRAWL_BASE_URL`, `CONTENT_TIMEOUT`
- **Output Model**: `ExtractedDocument` containing `url`, `title`, `markdown`, `plain_text`, and `metadata`.

---

## Reviewer Agent Module

The **Reviewer Agent** (`app/agents/reviewer/`) evaluates generated reports against the original `PlannerResult` strategy and `ResearchResult` evidence collection.

---

## Writer Agent Module

The **Writer Agent** (`app/agents/writer/`) receives a `PlannerResult` plan and a structured `ResearchResult` evidence collection, then synthesizes a comprehensive Markdown Research Report.

---

## Multi-Agent Orchestrator Module

The **Multi-Agent Orchestrator** (`app/orchestrator/`) sequences agent workflows across four steps (`PlannerAgent` -> `ResearchAgent` -> `WriterAgent` -> `ReviewerAgent`), tracking execution metrics and aggregating `PlannerResult`, `ResearchResult`, `ReportResult`, and `ReviewResult` into a unified `WorkflowResult` response.

---

## Research Agent Module

The **Research Agent** (`app/agents/research/`) receives a `PlannerResult` plan from the Planner Agent, requests necessary tools strictly through `ToolRegistry`, gathers raw research findings, and structures them into a formal `ResearchResult` evidence collection.

---

## Universal Tool Registry Module

The **Tool Registry** (`app/tools/`) is the central catalog of every capability available to AI agents. It acts as a metadata directory that tracks tool identities, specifications, input/output JSON schemas, versioning, enabling status, and supported agent roles.

---

## Universal LLM Platform (OpenRouter Integration)

Desearch AI integrates **OpenRouter** (`app/core/llm/`) as its decoupled, universal LLM platform provider using direct HTTP REST calls (`httpx`).

---

## Development Quality Workflow

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
