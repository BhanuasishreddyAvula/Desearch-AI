# Desearch AI Backend

> Production-grade FastAPI backend service powering the Desearch AI Multi-Agent Workbench.

---

## 🌟 Overview & Architecture

The backend service coordinates application lifecycle events, modular domain settings, standardized API response envelopes, centralized exception handling, HTTP middleware, observability (logging, tracing, metrics, events), dependency injection, abstract repository persistence layers, Supabase PostgreSQL database integration, research session management, production multi-agent AI pipelines (Planner Agent, Research Agent, Writer Agent, Reviewer Agent, Multi-Agent Orchestrator), real search & web content extraction tools (`SearchTool` via Exa, `ContentTool` via Firecrawl), universal tool registration (`ToolRegistry`), real-time research progress streaming with Server-Sent Events (`POST /api/v1/orchestrator/stream`), deterministic report exports (Markdown `.md` and PDF `.pdf`), and routing for the **Desearch AI** research workbench.

---

## 🏛️ Control Flow Hierarchy & Architectural Rules

```text
API Layer (FastAPI Routers in app/orchestrator/, app/sessions/, app/export/)
         │
         ▼
Multi-Agent Orchestrator (app/orchestrator/orchestrator.py)
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

### Architectural Principles:
1. **Orchestrator Boundary**: The `MultiAgentOrchestrator` is the sole coordinator of multi-agent execution flows. Agents never invoke each other directly.
2. **Writer Agent Boundary**: The Writer Agent MUST NOT access `ToolRegistry` or call search tools. Its sole input is the gathered `ResearchResult` evidence.
3. **Reviewer Agent Boundary**: The Reviewer Agent evaluates claim-to-evidence alignment. If the relevance score $< 0.75$, the orchestrator triggers an automatic 1-pass re-search loop.
4. **3-Tier Multi-Provider Safety Net**:
   - **Tier 1**: Groq Cloud (`llama-3.3-70b-versatile`)
   - **Tier 2**: NVIDIA NIM (`meta/llama-3.3-70b-instruct`)
   - **Tier 3**: OpenRouter (`google/gemini-2.0-flash-lite-preview-02-05:free`)
5. **Turn Index Truncation Engine**:
   - `SupabaseConversationRepository.delete_from_index(session_id, turn_index)` purges downstream messages starting at offset `turn_index * 2` when an earlier question is edited.

---

## 🛠️ Module Breakdown

### 1. Agents Module (`app/agents/`)
- `planner/`: Scopes user query into execution tasks and extracts core entity keywords.
- `research/`: Executes web search & scraping, deduplicating URLs and enforcing a 26,000-character context budget (~6,500 tokens).
- `writer/`: Synthesizes evidence using **Pure Intent RAG Synthesis** with dynamic prompt-aware sections and bonus technical insights.
- `reviewer/`: Evaluates report quality, scoring relevance and approving/rejecting synthesis.

### 2. Core Module (`app/core/`)
- `llm/client.py`: 3-Tier Multi-Provider failover engine (`LLMClient`).
- `database.py`: Supabase client initialization.
- `config.py` & `settings/`: Pydantic settings loading `.env`.

### 3. Conversations Module (`app/conversations/`)
- `supabase_repository.py`: Message CRUD operations, session listing, and `delete_from_index` downstream truncation.

### 4. Export Module (`app/export/`)
- `service.py`: Generates downloadable `.md` and `.pdf` files (powered by ReportLab).

---

## 📡 API Endpoints Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/orchestrator/run` | Execute synchronous multi-agent research workflow. |
| `POST` | `/api/v1/orchestrator/stream` | Stream real-time agent workflow progress via SSE (`text/event-stream`). |
| `POST` | `/api/v1/orchestrator/cancel` | Cancel running agent workflow for a session. |
| `POST` | `/api/v1/sessions` | Create a new research session. |
| `GET`  | `/api/v1/sessions` | List research sessions. |
| `GET`  | `/api/v1/sessions/{id}` | Get research session details & metadata. |
| `DELETE`| `/api/v1/sessions/{id}` | Delete a research session. |
| `GET`  | `/api/v1/sessions/{id}/messages` | List conversation message turns. |
| `GET`  | `/api/v1/reports/{id}/export` | Export report as `.md` or `.pdf`. |

---

## ⚡ Local Setup

```bash
cd backend
python -m venv venv
# Activate virtualenv (Windows: venv\Scripts\activate | Linux: source venv/bin/activate)
pip install -r requirements.txt

# Start FastAPI server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
