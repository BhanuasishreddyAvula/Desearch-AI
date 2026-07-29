# Implementation Report — Ticket P2-06

> **Ticket ID:** `P2-06`  
> **Title:** Research Agent  
> **Project:** Desearch AI  
> **Organization:** BhanuasishreddyAvula's Org  
> **Role:** Lead Backend Engineer  
> **Status:** COMPLETED & VERIFIED  
> **Date:** 2026-07-28  

---

## 1. Files Created

- [`backend/app/agents/research/__init__.py`](../../backend/app/agents/research/__init__.py) — Package re-exports for Research Agent components.
- [`backend/app/agents/research/models.py`](../../backend/app/agents/research/models.py) — Domain models `ResearchTask`, `Evidence`, `EvidenceCollection`, and `ResearchResult`.
- [`backend/app/agents/research/schemas.py`](../../backend/app/agents/research/schemas.py) — Pydantic v2 schemas (`ResearchRunRequest`, `EvidenceSchema`, `ResearchResultSchema`, `ResearchEnvelope`).
- [`backend/app/agents/research/prompts.py`](../../backend/app/agents/research/prompts.py) — `RESEARCH_AGENT_SYSTEM_PROMPT` and `build_research_user_prompt()`.
- [`backend/app/agents/research/research.py`](../../backend/app/agents/research/research.py) — `ResearchAgent` orchestrating tool requests via `ToolRegistry` and evidence processing via `LLMClient`.
- [`backend/app/agents/research/service.py`](../../backend/app/agents/research/service.py) — `ResearchService` validating research session and executing agent workflow.
- [`backend/app/agents/research/router.py`](../../backend/app/agents/research/router.py) — FastAPI router declaring `POST /api/v1/research/run`.

---

## 2. Files Modified

- [`backend/app/tools/builtin/web_search.py`](../../backend/app/tools/builtin/web_search.py) — Added deterministic mock `execute()` implementation.
- [`backend/app/tools/builtin/web_fetch.py`](../../backend/app/tools/builtin/web_fetch.py) — Added deterministic mock `execute()` implementation.
- [`backend/app/tools/builtin/document_reader.py`](../../backend/app/tools/builtin/document_reader.py) — Added deterministic mock `execute()` implementation.
- [`backend/app/tools/builtin/citation_extractor.py`](../../backend/app/tools/builtin/citation_extractor.py) — Added deterministic mock `execute()` implementation.
- [`backend/app/api/router.py`](../../backend/app/api/router.py) — Registered `research_router` under `/research`.
- [`backend/README.md`](../../backend/README.md) — Updated to document `Research Agent` module, evidence collection, tool usage, and API endpoint.

---

## 3. Research Agent Architecture

```text
       FastAPI Router (POST /api/v1/research/run)
                         │
                         ▼
          ResearchService (app/agents/research/service.py)
                         │
                         ▼
           ResearchAgent (app/agents/research/research.py)
                         │
        ┌────────────────┴────────────────┐
        ▼                                 ▼
  ToolRegistry                       LLMClient
  (app/tools/registry.py)            (app/core/llm/client.py)
        │                                 │
        ▼                                 ▼
Registered Tools                 OpenRouter Platform
(web_search, web_fetch, ...)     (Evidence Structuring)
```

---

## 4. Tool Interaction Flow

1. `ResearchAgent` receives a `PlannerResult` execution plan.
2. For each task in `plan.tasks`, `ResearchAgent` requests tools **exclusively** through `ToolRegistry` (`tool_registry.get(tool_id)`).
3. Tools are validated for existence and enabled state (`tool.enabled == True`). Missing or disabled tools raise standard application errors.
4. `ResearchAgent` invokes `tool.execute(**kwargs)`. Placeholder built-in tools return deterministic mock data payloads.
5. `ResearchAgent` passes tool outputs to `LLMClient` to format and structure evidence findings into an `EvidenceCollection`.

---

## 5. Evidence Model

Every evidence item conforms to the strict `Evidence` domain model:

```python
@dataclass
class Evidence:
    id: str             # e.g., "ev_1"
    title: str          # e.g., "Technical Specification Findings"
    summary: str        # Objective evidence text summary
    source: str         # Source URL or document path
    tool_used: str      # ID of tool used (e.g., "web_search")
    confidence: float   # Score between 0.0 and 1.0
    metadata: dict      # Additional metadata attributes
```

---

## 6. Verification Steps

1. **Backend Startup Verification**:
   - Server starts cleanly (`Research Agent` router registered under `/api/v1/research`).
2. **HTTP API Execution (`POST /api/v1/research/run`)**:
   - Submit request payload with `session_id` and a valid `plan` object.
   - Endpoint verifies session in Supabase, requests tools via `ToolRegistry`, processes tool outputs through `LLMClient`, and returns `ResearchEnvelope` wrapping `ResearchResultSchema`.
3. **Observability Verification**:
   - Console logs emit `Research Started`, `Tool Requested`, `Tool Returned`, `Evidence Added`, and `Research Completed`.

---

## 7. Manual Checklist

- [x] **ToolRegistry Boundary**: Research Agent obtains tools exclusively via `ToolRegistry`. Does NOT call tools directly.
- [x] **Decoupled LLM Client**: Research Agent uses `LLMClient` interface for structuring evidence.
- [x] **No Question Answering**: Agent solely gathers, organizes, and returns evidence without writing final answers or reports.
- [x] **Evidence Models & Schemas**: Implemented `ResearchTask`, `Evidence`, `EvidenceCollection`, `ResearchResult`, and Pydantic schemas.
- [x] **Observability**: Emits `Research Started`, `Tool Requested`, `Tool Returned`, `Evidence Added`, and `Research Completed` logs.
- [x] **Error Handling**: Standardized errors for missing tools, disabled tools, and invalid input payloads.
- [x] **Updated Documentation**: Added `Research Agent` section to `backend/README.md`.

---

## 8. Out-of-Scope Items

No actual web scraping, live web search HTTP API calls, PDF parsing, Writer Agent, Reviewer Agent, streaming, or orchestrator loops were implemented outside the scope of this ticket.
