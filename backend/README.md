# Desearch AI Backend

> Production-grade FastAPI backend foundation for Desearch AI.

---

## Purpose

The backend service coordinates application lifecycle events, modular domain settings, standardized API response envelopes, centralized exception handling, HTTP middleware, observability (logging, tracing, metrics, events), dependency injection, research session management, and routing for the **Desearch AI** research workbench.

---

## Research Session Module

The Research Session domain (`app/sessions/`) manages the complete lifecycle of research queries across 9 states using an in-memory repository pattern, domain service layer, Pydantic schemas, and FastAPI endpoints.

```text
backend/app/sessions/
├── __init__.py            # Package exports
├── enums.py               # SessionStatus enum (DRAFT, PLANNING, WAITING_APPROVAL, etc.)
├── models.py              # ResearchSession domain dataclass entity
├── repository.py          # SessionRepository (In-memory storage)
├── router.py              # API router (/api/v1/sessions)
├── schemas.py             # Pydantic v2 schemas (CreateSessionRequest, SessionResponse, etc.)
└── service.py             # SessionService business logic & state transition validation
```

### Research Session Lifecycle State Machine

```text
[DRAFT] --> [PLANNING] --> [WAITING_APPROVAL] --> [RESEARCHING] --> [REVIEWING] --> [COMPLETED]
   │             │                 │                  │               │                │
   └──(cancel)───┴────(cancel)─────┴─────(cancel)─────┴────(cancel)───┴────(cancel)────┼──> [ARCHIVED]
                 │                                    │               │                │
                 └──────(fail)────────────────────────┴────(fail)─────┴────(fail)──────┘
```

#### Valid Transitions Matrix
- **`DRAFT`**: → `PLANNING`, `CANCELLED`
- **`PLANNING`**: → `WAITING_APPROVAL`, `FAILED`, `CANCELLED`
- **`WAITING_APPROVAL`**: → `RESEARCHING`, `CANCELLED`
- **`RESEARCHING`**: → `REVIEWING`, `FAILED`, `CANCELLED`
- **`REVIEWING`**: → `COMPLETED`, `RESEARCHING`, `FAILED`, `CANCELLED`
- **`COMPLETED`**: → `ARCHIVED`
- **`FAILED`**: → `ARCHIVED`
- **`CANCELLED`**: → `ARCHIVED`
- **`ARCHIVED`**: Terminal state (no further transitions allowed)

### API Endpoints (`/api/v1/sessions`)

- **`POST /api/v1/sessions`**: Create a new research session in `DRAFT` state.
- **`GET /api/v1/sessions`**: List all research sessions.
- **`GET /api/v1/sessions/{session_id}`**: Retrieve session details by ID.
- **`PATCH /api/v1/sessions/{session_id}`**: Update session title, metadata, or transition lifecycle status.

---

## Application Container

Desearch AI implements a lightweight service container (`app/core/container.py`) to centralize shared infrastructure singletons without global mutable state or heavy third-party DI frameworks.

```text
backend/app/core/
├── container.py           # Container class centralizing Settings, Logger, Tracer, & Metrics
```

---

## Dependency Injection Architecture

Dependency Injection in Desearch AI uses FastAPI's native `Depends()` mechanism (`app/dependencies/`). Reusable dependency providers decouple API handlers from infrastructure implementations and enable seamless unit test mocking.

```text
backend/app/dependencies/
├── __init__.py            # Package exports
├── common.py              # Request-scoped providers (request_id, trace_id, execution_time)
├── providers.py           # Core infrastructure providers (container, settings, logger, tracer, metrics)
└── services.py            # Business service providers container placeholder
```

---

## OpenAPI & API Tags Customization

OpenAPI schema generation (`app/core/openapi.py`) is customized with project metadata, contact info, license specification, and structured API tags.

```text
Interactive OpenAPI Documentation: http://127.0.0.1:8000/docs
ReDoc Schema Documentation:        http://127.0.0.1:8000/redoc
```

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
