# Desearch AI Backend

> Production-grade FastAPI backend foundation for Desearch AI.

---

## Purpose

The backend service coordinates application lifecycle events, settings management, logging, and routing for the **Desearch AI** research workbench. It provides a modular foundation designed to support multi-agent research orchestration, tool execution, session memory management, and observability.

---

## Folder Structure

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application initialization & lifespan context
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py        # Centralized API router mounting /api/v1
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── health.py    # Health check endpoint (/api/v1/health)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # BaseSettings environment configuration
│   │   └── logging.py       # Standard library console logging formatter & logger setup
│   ├── models/              # Data models package placeholder
│   ├── services/            # Business services package placeholder
│   ├── orchestrator/        # Orchestrator package placeholder
│   ├── agents/              # Agents package placeholder
│   ├── tools/               # External tools package placeholder
│   ├── memory/              # Session context memory package placeholder
│   └── utils/               # Utility functions package placeholder
├── pyproject.toml           # Project metadata
├── README.md                # Backend service documentation
└── requirements.txt         # Pinned Python dependencies
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
- **ReDoc Documentation**: `http://127.0.0.1:8000/redoc`

### Expected Health Check JSON Response

```json
{
  "status": "healthy",
  "service": "desearch-ai-backend",
  "version": "0.1.0"
}
```
