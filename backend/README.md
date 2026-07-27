# Desearch AI Backend

> Production-grade FastAPI backend foundation for Desearch AI.

---

## Purpose

The backend service coordinates application lifecycle events, modular domain settings, standardized API response envelopes, centralized exception handling, HTTP middleware, observability (logging, tracing, metrics, events), dependency injection, abstract repository persistence layers, Supabase PostgreSQL database integration, research session management, and routing for the **Desearch AI** research workbench.

---

## Supabase Persistence

Desearch AI integrates **Supabase PostgreSQL** as its production persistence layer (`app/sessions/supabase_repository.py`). The domain service layer remains 100% untouched due to the repository abstraction pattern established in Ticket P2-02.

```text
backend/app/
├── core/
│   └── database.py                  # Singleton Supabase client getter (get_supabase_client)
└── sessions/
    ├── repository.py                # InMemorySessionRepository (Fallback)
    └── supabase_repository.py       # SupabaseSessionRepository (Production Supabase PostgreSQL)
```

### Database Schema (`public.research_sessions`)

```sql
CREATE TABLE IF NOT EXISTS public.research_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    query TEXT NOT NULL,
    status TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Production Indexes
CREATE INDEX IF NOT EXISTS idx_research_sessions_status ON public.research_sessions (status);
CREATE INDEX IF NOT EXISTS idx_research_sessions_created_at ON public.research_sessions (created_at DESC);
```

### Row Level Security (RLS)

Row Level Security is enabled on `public.research_sessions` with a strict authenticated access policy:

```sql
ALTER TABLE public.research_sessions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow authenticated access to research_sessions"
ON public.research_sessions
FOR ALL
TO authenticated, service_role
USING (true)
WITH CHECK (true);
```

---

## Repository Architecture

Desearch AI strictly separates domain business logic from data storage mechanisms using abstract repository interfaces (`app/core/repositories/`). This adheres to SOLID principles (Dependency Inversion), allowing seamless swapping of persistence providers (e.g. from in-memory dictionary storage to Supabase PostgreSQL) without altering service layer code.

```text
       FastAPI Router Endpoint (POST /api/v1/sessions)
                            │
                            ▼
              SessionService (app/sessions/service.py)
                            │  (Depends ONLY on AbstractSessionRepository)
                            ▼
           AbstractSessionRepository (Interface)
                            ▲
                            │  (Implements interface)
         SupabaseSessionRepository (app/sessions/supabase_repository.py)
```

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

## OpenAPI & API Tags Customization

OpenAPI schema generation (`app/core/openapi.py`) is customized with project metadata, contact info, license specification, and structured API tags.

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

#### Windows (PowerShell / Command Prompt)
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
