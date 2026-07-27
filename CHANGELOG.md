# Changelog

All notable changes to the **Desearch AI** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Milestone 1: Core System Architecture & Specifications (`docs/`)
- Milestone 2: FastAPI Backend Setup & Foundation
- Milestone 3: Functional Research Orchestration & LLM Provider Layer
- Milestone 4: Research Agents with Tools & Session Memory
- Milestone 5: External Tool Integration (Web Search, Web Page Reader, Document Reader)
- Milestone 6: Research Session Memory Layer & Session Isolation
- Milestone 7: Human-in-the-Loop (HITL) Approval Checkpoint Layer
- Milestone 8: Structured Logging, Tracing & Observability
- Milestone 9: Next.js Research Workbench Frontend
- Milestone 10: Cloud Infrastructure & Deployment
- Milestone 11: Production Verification & End-to-End Validation

---

## [0.1.0] - 2026-07-27

### Added
- **Repository Foundation & Engineering Standards** (`TICKET: P1-01`):
  - Initialized canonical repository folder structure (`backend/`, `frontend/`, `docs/`, `infrastructure/`, `scripts/`, `.github/`, `.vscode/`).
  - Added comprehensive `README.md` with product vision, architecture overview, folder tree, roadmap, tech stack, and conventions.
  - Added open-source `LICENSE` (MIT License).
  - Added `.editorconfig` with professional code formatting rules for Python, TypeScript, JSON, Markdown, and YAML.
  - Added `.gitattributes` for line ending normalization across Linux, macOS, and Windows.
  - Added comprehensive `.gitignore` covering Python, Next.js, FastAPI, Node, TypeScript, IDEs, OS files, logs, coverage, and environment files.
  - Added `.env.example` template with configuration placeholders for Supabase, LLM providers, tools, and logging.
  - Added `CONTRIBUTING.md` defining git workflow, branch naming (`feature/*`, `bugfix/*`, etc.), Conventional Commit standards, and PR requirements.
  - Added `CODE_OF_CONDUCT.md` adopting Contributor Covenant v2.1.
  - Added `SECURITY.md` establishing vulnerability reporting procedures and security best practices.
  - Added `docs/P1-01_IMPLEMENTATION_REPORT.md` documenting ticket completion.
