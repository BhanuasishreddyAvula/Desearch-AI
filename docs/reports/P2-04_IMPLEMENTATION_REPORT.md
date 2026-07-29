# Implementation Report — Ticket P2-04

> **Ticket ID:** `P2-04`  
> **Title:** Planner Agent  
> **Project:** Desearch AI  
> **Organization:** BhanuasishreddyAvula's Org  
> **Supabase Project:** Desearch AI (`reezzcgbguduazaynjkw`)  
> **Role:** Lead Backend Engineer  
> **Status:** COMPLETED & VERIFIED  
> **Date:** 2026-07-27  

---

## 1. Files Created

- [`backend/app/agents/planner/__init__.py`](../../backend/app/agents/planner/__init__.py) — Package re-exports for Planner Agent components.
- [`backend/app/agents/planner/models.py`](../../backend/app/agents/planner/models.py) — Domain models `PlannerResult` and `TaskModel`.
- [`backend/app/agents/planner/schemas.py`](../../backend/app/agents/planner/schemas.py) — Pydantic v2 schemas (`PlanRequest`, `PlannerResultSchema`, `TaskSchema`, `PlanEnvelope`).
- [`backend/app/agents/planner/prompts.py`](../../backend/app/agents/planner/prompts.py) — `PLANNER_SYSTEM_PROMPT` and `build_planner_user_prompt()`.
- [`backend/app/agents/planner/planner.py`](../../backend/app/agents/planner/planner.py) — `PlannerAgent` implementing Google Gemini 1.5 Flash LLM API integration with structured JSON generation and fallback handling.
- [`backend/app/agents/planner/service.py`](../../backend/app/agents/planner/service.py) — `PlannerService` fetching `ResearchSession` from Supabase and orchestrating plan generation.
- [`backend/app/agents/planner/router.py`](../../backend/app/agents/planner/router.py) — FastAPI router declaring `POST /api/v1/planner/plan`.

---

## 2. Files Modified

- [`backend/requirements.txt`](../../backend/requirements.txt) — Added `google-generativeai>=0.8.0` SDK dependency.
- [`backend/app/api/router.py`](../../backend/app/api/router.py) — Registered `planner_router` under `/planner`.
- [`backend/README.md`](../../backend/README.md) — Updated to document `Planner Agent` module, responsibilities, prompt strategy, and API usage.

---

## 3. Planner Architecture

The Planner Agent operates within a decoupled layered architecture:

```text
HTTP Request (POST /api/v1/planner/plan)
                 │
       FastAPI Router (app/agents/planner/router.py)
                 │
       PlannerService (app/agents/planner/service.py)
                 │  (Fetches query from Supabase via AbstractSessionRepository)
                 ▼
        PlannerAgent (app/agents/planner/planner.py)
                 │  (Formats prompts & configures response_mime_type: "application/json")
                 ▼
      Google Gemini 1.5 Flash API (Google AI Studio)
                 │
                 ▼
          PlannerResult JSON Payload
```

---

## 4. Prompt Strategy (`app/agents/planner/prompts.py`)

- **System Instruction (`PLANNER_SYSTEM_PROMPT`)**: Enforces sole persona (Planner Agent), prohibits web searches, fetching pages, fabrication, or direct query answering. Instructs 2–5 sequential tasks with attributes (`id`, `title`, `description`, `priority`, `reason`), ambiguity detection, and strict JSON output format matching `PlannerResult`.
- **User Prompt (`build_planner_user_prompt`)**: Wraps session query string in structured instruction demarcations.

---

## 5. Google Gemini Integration

- **SDK**: `google-generativeai` (Google AI Studio API key).
- **Model**: `gemini-1.5-flash`.
- **Generation Config**: `"response_mime_type": "application/json"`, `temperature: 0.2`.
- **Error Recovery & Observability**:
  - Emits observability events (`AGENT_STARTED`, `AGENT_COMPLETED`).
  - Catches LLM timeouts, empty responses, rate limits, and JSON decode errors, raising standardized `ExternalServiceException` or `ValidationException`.
  - Includes a deterministic structured fallback planner when API key is unconfigured.

---

## 6. Verification Steps

1. **Python Shell Integration Verification**:
   ```cmd
   python -c "from app.agents.planner import PlannerAgent; agent = PlannerAgent(); res = agent.generate_plan('Compare Supabase vs Firebase for Enterprise SaaS'); print('Goal:', res.goal); print('Tasks:', len(res.tasks))"
   ```

2. **HTTP API Verification (`POST /api/v1/planner/plan`)**:
   - Create a session: `POST /api/v1/sessions` → Body `{"query": "Compare Supabase vs Firebase for Enterprise SaaS"}` → Returns `session_id`.
   - Call planner API: `POST /api/v1/planner/plan` → Body `{"session_id": "<session_id>"}`.
   - Response: Returns HTTP 200 OK with `PlanEnvelope` wrapping `PlannerResultSchema` containing 3 structured tasks, dependencies, complexity, and expected output description.

---

## 7. Manual Checklist

- [x] **Google Gemini Integration**: Single LLM provider using Google AI Studio API (`gemini-1.5-flash`).
- [x] **No Web Research**: Planner Agent solely plans and decomposes queries without executing web searches.
- [x] **Domain Models & Schemas**: Implemented `PlannerResult`, `TaskModel`, `PlannerResultSchema`, `PlanRequest`, `PlanEnvelope`.
- [x] **Engineered Prompts**: Created `PLANNER_SYSTEM_PROMPT` enforcing persona, rules, and JSON output schema.
- [x] **Supabase Integration**: `PlannerService` reads `ResearchSession` from Supabase without mutating state.
- [x] **Observability Logs**: Emits `AGENT_STARTED`, `AGENT_COMPLETED`, and prompt/response log lines.
- [x] **Error Handling**: Gracefully handles LLM timeouts, empty responses, invalid JSON, and rate limits.
- [x] **Updated Documentation**: Added `Planner Agent` section to `backend/README.md`.

---

## 8. Out-of-Scope Items

No Research Agent web searching, page fetching, Writer Agent report drafting, Reviewer Agent evaluation, tool execution, session state mutation, or real-time streaming were implemented outside the scope of this ticket.
