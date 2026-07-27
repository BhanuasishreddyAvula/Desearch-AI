# Desearch AI Backend

> Production-grade FastAPI backend foundation for Desearch AI.

---

## Purpose

The backend service coordinates application lifecycle events, modular domain settings, standardized API response envelopes, centralized exception handling, HTTP middleware, observability (logging, tracing, metrics, events), dependency injection, application service containers, and routing for the **Desearch AI** research workbench.

---

## Application Container

Desearch AI implements a lightweight service container (`app/core/container.py`) to centralize shared infrastructure singletons without global mutable state or heavy third-party DI frameworks.

```text
backend/app/core/
├── container.py           # Container class centralizing Settings, Logger, Tracer, & Metrics
```

The application container holds references only to core infrastructure primitives:
- `settings`: Centralized configuration instance (`Settings`).
- `logger`: Root application logger (`AppLogger`).
- `tracer`: In-memory tracing engine (`Tracer`).
- `metrics`: In-memory metrics collector (`MetricsCollector`).

*Note: The application container does NOT create Supabase, Redis, LLM clients, or Agent instances.*

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

### Reusable Dependency Providers

- `get_container()`: Provides the shared application `Container`.
- `get_settings_dep()`: Provides `Settings`.
- `get_logger_dep(name)`: Provides a named `AppLogger`.
- `get_tracer_dep()`: Provides `Tracer`.
- `get_metrics_dep()`: Provides `MetricsCollector`.
- `get_request_id_dep(request)`: Resolves current correlated request ID.
- `get_trace_id_dep(request)`: Resolves current correlated trace ID.
- `get_execution_time_dep(request)`: Resolves request execution duration in milliseconds.

---

## OpenAPI & API Tags Customization

OpenAPI schema generation (`app/core/openapi.py`) is customized with project metadata, contact info, license specification, and structured API tags.

```text
Interactive OpenAPI Documentation: http://127.0.0.1:8000/docs
ReDoc Schema Documentation:        http://127.0.0.1:8000/redoc
```

### Standard API Tags

- **`Health`**: Health check and diagnostic endpoints for operational monitoring.
- **`System`**: System status, environment parameters, and platform health.
- **`Research`**: Research query submission, execution plan, and report generation endpoints.
- **`Sessions`**: Research session lifecycle, context inspection, and trace logging.
- **`Agents`**: Multi-agent pipeline inspection, status, and role configurations.
- **`Tools`**: Tool registry, tool execution, and source gathering integrations.
- **`Administration`**: Platform management, quota monitoring, and system metrics.

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

#### Linux / macOS (Bash / Zsh)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
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

---

## Service Endpoints & Verification

- **Base Service URL**: `http://127.0.0.1:8000`
- **Health Check Endpoint**: `http://127.0.0.1:8000/api/v1/health`
- **Interactive OpenAPI Docs**: `http://127.0.0.1:8000/docs`

### Expected Health Check JSON Response

```json
{
  "success": true,
  "message": "Health check successful.",
  "timestamp": "2026-07-27T17:10:41.123456Z",
  "request_id": "c3f8e52a-91d4-47b2-b430-6712948e23f1",
  "data": {
    "status": "healthy",
    "service": "desearch-ai-backend",
    "version": "0.1.0"
  },
  "metadata": {
    "execution_time_ms": 0.45,
    "api_version": "0.1.0",
    "environment": "development",
    "pagination": null
  }
}
```
