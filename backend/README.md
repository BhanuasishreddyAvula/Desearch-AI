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

---

## Report Export Module (`app/export/`)

The **Report Export Service** (`ReportExportService`) formats completed research reports into downloadable Markdown (`.md`) or PDF (`.pdf`) documents.

- **Endpoint**: `GET /api/v1/reports/{session_id}/export?format=markdown` or `format=pdf`
- **Formatters**:
  - `MarkdownExportFormatter`: Formats canonical report text into UTF-8 encoded `.md` documents.
  - `PdfExportFormatter`: Formats report title, executive summary, headings, paragraphs, and citations into professional binary `.pdf` documents using ReportLab.

---

## Real Search & Content Tool Architecture

### 1. Search Tool Module (`app/tools/search/`)
The **Search Tool** (`SearchTool`) executes web search queries via the `ExaProvider` HTTP REST integration (`POST https://api.exa.ai/search`).

### 2. Content Tool Module (`app/tools/content/`)
The **Content Tool** (`ContentTool`) extracts clean web page content and Markdown via the `FirecrawlProvider` HTTP REST integration (`POST https://api.firecrawl.dev/v1/scrape`).

---

## Setup & Deployment

### 1. Create Virtual Environment
```cmd
cd backend
python -m venv venv
venv\Scripts\activate
```

### 2. Install Production Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run Server
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
