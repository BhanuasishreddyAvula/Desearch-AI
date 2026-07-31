# Desearch AI — P3-02 Application Shell & Research Sidebar Report (`P3-02_APPLICATION_SHELL_REPORT.md`)

> **Product:** Desearch AI — Deep Research. Smarter Decisions.  
> **Ticket:** P3-02 — Application Shell & Research Sidebar  
> **Role:** Lead Frontend Engineer  
> **Status:** 100% IMPLEMENTED & VERIFIED  
> **Date:** 2026-08-01  

---

## 1. Executive Summary

Ticket P3-02 delivers the production application shell and dark research sidebar for Desearch AI, matching approved Screen 01 design specifications. The implementation includes:
- Canonical 3-column application shell filling the viewport without outer page scroll.
- Desktop research sidebar (`w-64` expanded ~260px, `w-16` collapsed rail) with brand mark, `+ New Research` CTA, and `Recent Research` history list.
- TanStack Query server-state integration (`useResearchSessions`) calling FastAPI `GET /api/v1/sessions` and unwrapping `BaseResponse<SessionListResponseData>`.
- Keyboard-navigable session list with active route selection (`/research/:sessionId`), title truncation, subtle loading skeleton, empty state (`"No research yet"`), and graceful error retry UI (`"Couldn't load recent research"`).
- Restrained workspace header with ONLY the `Reports` contextual control (inert/safe for P3-07).
- Cleanup of obsolete P3-01 preview components (`SidebarPreview`, `FoundationPreview`).

---

## 2. Existing P3-01 Architecture Reused

- **Design System & Semantic Tokens**: Utilized CSS variables (`--background` `#141312`, `--sidebar` `#1A1917`, `--surface` `#22201D`, `--accent` `#D95338`, `--border` `#2E2C28`) and typography utilities (`.font-serif-editorial` for Garamond headings, `.font-sans-ui` for Inter UI controls).
- **API Client Layer**: Reused `apiFetch<T>` and `ApiClientError` from `src/lib/api/client.ts`.
- **FastAPI Session API**: Reused and refined `sessionsApi.listSessions()` and `sessionsApi.getSession()`.
- **Providers & Router**: Reused TanStack `AppProviders` and React Router `createBrowserRouter`.

---

## 3. Components Created

- `src/features/sessions/hooks/useResearchSessions.ts`: TanStack Query hook fetching sessions list.
- `src/features/sessions/components/ResearchSidebar.tsx`: Canonical desktop sidebar with collapse/expand toggle.
- `src/features/sessions/components/SessionList.tsx`: Session list container handling loading, empty, error, and item rendering.
- `src/features/sessions/components/SessionItem.tsx`: Individual accessible session row supporting title truncation, active route selection, and collapsed rail view.
- `src/features/research/components/NewResearchView.tsx`: Screen 01 central workspace focal view (`"What are we researching today?"`).
- `src/features/research/components/SessionView.tsx`: Active research session workspace shell.

---

## 4. Components Removed / Cleaned Up

- `src/components/common/SidebarPreview.tsx`: Replaced by production `ResearchSidebar.tsx`.
- `src/components/common/FoundationPreview.tsx`: Replaced by production `NewResearchView.tsx` and `SessionView.tsx`.

---

## 5. Components Modified

- `src/components/common/Header.tsx`: Restrained header containing ONLY brand indicator (mobile) and `Reports` action button (desktop).
- `src/layouts/WorkspaceLayout.tsx`: Updated layout shell mounting production `ResearchSidebar`.
- `src/app/router.tsx`: Updated routes for `/` (New Research) and `/research/:sessionId` (Active Session View).
- `src/types/index.ts`: Added `BaseResponse<T>` and `SessionListResponseData` matching FastAPI response schemas.
- `src/lib/api/sessions.ts`: Updated `listSessions`, `getSession`, `createSession`, `renameSession`, `deleteSession` to unwrap `BaseResponse.data`.
- `backend/app/middleware/__init__.py`: Registered FastAPI `CORSMiddleware`.
- `backend/app/core/settings/security.py`: Expanded allowed development `CORS_ORIGINS`.

---

## 6. Sidebar Architecture

The desktop sidebar is rendered via `<aside aria-label="Research navigation sidebar">`:
- **Expanded Width**: 260px (`w-64`), full brand logo, collapse button (`PanelLeftClose`), `+ New Research` CTA button, `Recent Research` heading, and session title rows.
- **Collapsed Width**: 64px (`w-16`), brand icon, expand button (`PanelLeftOpen`), and `+ New Research` icon CTA.

---

## 7. Collapse/Expand Behavior

Managed via React local state (`isCollapsed`) within `ResearchSidebar.tsx`. Transitions smoothly via CSS `transition-all duration-200`. Title truncation prevents horizontal layout breaking in expanded mode. When collapsed, session lists, loading indicators, empty messages, error banners, and text labels are omitted completely.

---

## 8. Session Query Architecture

```text
SessionList
    ↓
useResearchSessions() [TanStack Query, key: ['research-sessions']]
    ↓
sessionsApi.listSessions()
    ↓
apiFetch<BaseResponse<SessionListResponseData>>('/api/v1/sessions')
    ↓
FastAPI Backend (http://127.0.0.1:8000/api/v1/sessions)
```

---

## 9. Session Navigation & Active Selection

- **Navigation**: Clicking `+ New Research` navigates to `/` via React Router `navigate('/')`. Clicking a session row navigates to `/research/:sessionId`.
- **Active State**: Handled via `useParams<{ sessionId?: string }>()`. If `activeSessionId === session.id`, row renders with `bg-surface text-foreground border-l-2 border-accent`.

---

## 10. Loading, Empty, and Error States

- **Loading State**: Rendered in `SessionList.tsx` when expanded via 3 subtle pulsing placeholder rows (`bg-surface/50 border border-border-subtle`). Respects `prefers-reduced-motion`.
- **Empty State**: Rendered when expanded and `sessions.length === 0` displaying restrained text `"No research yet"`.
- **Error State**: Rendered when expanded on fetch failure displaying `"Couldn't load recent research."` with a subtle `Retry` button calling `refetch()`. No raw stack traces or internal HTTP details are exposed.

---

## 11. Workspace Header

The header contains **ONLY** the `Reports` button in the top right. It is styled with `bg-surface border border-border-subtle hover:bg-surface-hover text-foreground/90 text-xs font-medium` and a `FileText` icon. The action is safe and inert in P3-02, awaiting full Reports Drawer implementation in P3-07.

---

## 12. Responsive Safeguards

`ResearchSidebar` uses `hidden md:block` in `WorkspaceLayout.tsx`, preventing the desktop sidebar from consuming viewport space on mobile (<768px). Header displays a compact brand mark on mobile viewports. Full mobile drawer integration is reserved for P3-11.

---

## 13. Accessibility & Focus Treatment

- Semantic tags (`<aside>`, `<nav>`, `<header>`, `<main>`, `<button>`).
- All buttons feature explicit `aria-label` and `title` attributes.
- Interactive rows support keyboard navigation (`tabIndex={0}`, `Enter` / `Space` key handlers).
- Visible focus rings (`focus:ring-2 focus:ring-focus-ring`) preserved.

---

## 14. Dependencies Added

**0 new dependencies added.** Used existing P3-01 foundation stack (`react-router-dom`, `@tanstack/react-query`, `lucide-react`, `clsx`, `tailwind-merge`).

---

## 15. Git & Secret Hygiene Audit

- `frontend/.env`: **IGNORED** (matches `.env` pattern in root `.gitignore`).
- `frontend/.env.example`: **TRACKED** (public reference configuration).
- `frontend/node_modules/`: **IGNORED** (matches `node_modules/` in `.gitignore`).
- `frontend/dist/`: **IGNORED** (matches `dist/` in `.gitignore`).
- **Secrets Audit**: 0 third-party API keys or provider secrets in browser environment or source code.

---

## 16. Summary of Files Changed

### Created
- `frontend/src/features/sessions/hooks/useResearchSessions.ts`
- `frontend/src/features/sessions/components/ResearchSidebar.tsx`
- `frontend/src/features/sessions/components/SessionList.tsx`
- `frontend/src/features/sessions/components/SessionItem.tsx`
- `frontend/src/features/research/components/NewResearchView.tsx`
- `frontend/src/features/research/components/SessionView.tsx`
- `docs/reports/P3-02_APPLICATION_SHELL_REPORT.md`

### Modified
- `frontend/src/types/index.ts`
- `frontend/src/lib/api/sessions.ts`
- `frontend/src/components/common/Header.tsx`
- `frontend/src/layouts/WorkspaceLayout.tsx`
- `frontend/src/app/router.tsx`
- `backend/app/middleware/__init__.py`
- `backend/app/core/settings/security.py`

### Cleaned Up
- `frontend/src/components/common/SidebarPreview.tsx`
- `frontend/src/components/common/FoundationPreview.tsx`

---

## 17. Validation & Verification

- [x] **Desktop 260px Expanded Sidebar**: Verified brand, `+ New Research` CTA button, `Recent Research` section, and session history list.
- [x] **Desktop Collapsed Rail Mode**: Verified toggle collapse to 64px rail with zero textual session/error clutter.
- [x] **New Research CTA Navigation**: Navigates cleanly to `/` without browser reload.
- [x] **Session Route Navigation**: Navigates cleanly to `/research/:sessionId`.
- [x] **Active Session Selection**: Selected session highlights with terracotta left border indicator.
- [x] **Title Truncation**: Ellipsis truncation prevents sidebar text overflow.
- [x] **Loading / Empty / Error States**: Handled cleanly with user-safe UI.
- [x] **Header Restrained**: Header contains ONLY the `Reports` action button.
- [x] **Mobile Safeguard**: Desktop sidebar hidden on mobile screens (`<768px`).

---

## 18. Deferred Work (Explicit P3-03+ Scope)

- **P3-03**: Production Research Composer & session creation on prompt submit.
- **P3-04**: Real-time SSE progress streaming & stage shimmer UI.
- **P3-05**: Synthesis report document renderer & inline citations.
- **P3-07**: Reports drawer panel & PDF/Markdown export execution.
- **P3-09**: Research session rename & delete actions.
- **P3-11**: Mobile drawer overlay & hamburger navigation.

---

## 19. Backend Preservation Confirmation

> **CONFIRMED:** No business logic, endpoints, or response schemas in `backend/` were changed. Only FastAPI middleware registration and security settings were updated to attach `CORSMiddleware`.

---

## 20. Post-Implementation Browser Integration Fixes

### Defect 1 — FastAPI CORS Preflight Failure (HTTP 405 Method Not Allowed)
- **Observed Failure**: When the frontend (`http://127.0.0.1:3000`) executed `GET /api/v1/sessions`, the browser sent an HTTP `OPTIONS /api/v1/sessions` preflight request. The backend responded with `HTTP 405 Method Not Allowed`, failing CORS preflight before execution.
- **Root Cause**: `CORSMiddleware` was defined in settings (`settings.CORS_ORIGINS`), but was omitted from FastAPI middleware registration in `backend/app/middleware/__init__.py`. Without `CORSMiddleware`, FastAPI attempted to route `OPTIONS` requests to a non-existent explicit options handler.
- **Fix Implemented**:
  1. Updated `backend/app/middleware/__init__.py` registering `CORSMiddleware`:
     ```python
     app.add_middleware(
         CORSMiddleware,
         allow_origins=settings.CORS_ORIGINS,
         allow_credentials=True,
         allow_methods=["*"],
         allow_headers=["*"],
     )
     ```
  2. Updated `backend/app/core/settings/security.py` ensuring permitted development origins include `http://localhost:3000`, `http://127.0.0.1:3000`, `http://localhost:8000`, and `http://127.0.0.1:8000`.
- **Validation**: Preflight `OPTIONS /api/v1/sessions` returns `200 OK` with CORS headers (`Access-Control-Allow-Origin: http://127.0.0.1:3000`). Subsequent `GET /api/v1/sessions` executes cleanly.

---

### Defect 2 — Collapsed Sidebar Error Content
- **Observed Defect**: When the desktop sidebar was collapsed (`isCollapsed === true`), error states (`"Couldn't load recent research."`) continued rendering inside the 64px rail, wrapping vertically and creating broken UI.
- **Root Cause**: `ResearchSidebar.tsx` and `SessionList.tsx` did not suppress session history subcomponents when collapsed.
- **Fix Implemented**:
  1. Updated `ResearchSidebar.tsx` so the `<nav>` container and `Recent Research` heading render **only** when `!isCollapsed`.
  2. Updated `SessionList.tsx` to return `null` immediately when `isCollapsed === true`.
  3. When collapsed, the rail contains exclusively: brand logo (`Compass`), expand toggle (`PanelLeftOpen`), and `+ New Research` icon button (`Plus`).
  4. Expanding the sidebar restores the full `Recent Research` section and list.
- **Validation**: Collapsed rail renders cleanly without wrapped error text or session labels. Expanding restores history list.
