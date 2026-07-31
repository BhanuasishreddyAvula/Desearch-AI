# Desearch AI — P3-01 Frontend Foundation & Design System Report (`P3-01_FRONTEND_FOUNDATION_REPORT.md`)

> **Product:** Desearch AI — Deep Research. Smarter Decisions.  
> **Ticket:** P3-01 — Frontend Foundation & Desearch Design System  
> **Role:** Lead Frontend Engineer  
> **Status:** 100% IMPLEMENTED & VERIFIED  
> **Date:** 2026-08-01  

---

## 1. Executive Summary

Ticket P3-01 establishes the production frontend architecture and semantic design system for Desearch AI. Built upon Vite, React 18, TypeScript, Tailwind CSS, React Router v6, and TanStack Query v5, the foundation provides a fast, type-safe, and dark-editorial workspace interface that connects cleanly to the existing FastAPI backend (`http://127.0.0.1:8000`).

All critical architectural boundaries—including 100% isolation of third-party credentials (`OPENROUTER_API_KEY`, `EXA_API_KEY`, `FIRECRAWL_API_KEY`, `SUPABASE_SERVICE_ROLE_KEY`), low-level fetch-based SSE stream parsing for `POST /api/v1/orchestrator/stream`, semantic design token mapping, and typography hierarchy—have been established and verified.

---

## 2. Stack Installed

| Layer | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Core Framework** | React + React DOM | `^18.3.1` | UI Component Tree & Reactive Rendering |
| **Build Tooling** | Vite | `^5.3.4` | Lightning-fast HMR & Production Bundling |
| **Type Safety** | TypeScript | `^5.5.3` | Strict Static Typing & Schema Verification |
| **Styling System** | Tailwind CSS + PostCSS | `^3.4.7` | Utility-First Design Token Integration |
| **Routing** | React Router DOM | `^6.26.0` | Client-Side SPA Route Orchestration |
| **Server State** | TanStack Query | `^5.51.1` | Server Data Caching & Lifecycle Management |
| **Iconography** | Lucide React | `^0.424.0` | Production Icon System |
| **Class Utilities** | `clsx` + `tailwind-merge` | `^2.1.1` | Conditional Class Merging (`cn` helper) |

---

## 3. Dependencies Added and Why

1. **`react` & `react-dom` (`^18.3.1`)**: Foundational library for building interactive React UI components.
2. **`react-router-dom` (`^6.26.0`)**: Standard SPA routing solution enabling `/` and `/research/:sessionId` workspace navigation without page reloads.
3. **`@tanstack/react-query` (`^5.51.1`)**: Provides declarative server-state management, automatic refetching, and caching for session lists and report data.
4. **`lucide-react` (`^0.424.0`)**: Lightweight, accessible, vector-based SVG icons matching the editorial research theme.
5. **`clsx` & `tailwind-merge` (`^2.1.1`)**: Combines conditional CSS classes cleanly without specificity conflicts.
6. **`tailwindcss`, `autoprefixer`, `postcss` (`^3.4.7`)**: Compiles semantic CSS variable tokens into utility classes.
7. **`typescript` & `@types/*` (`^5.5.3`)**: Enforces strict compile-time type checking and IDE autocomplete across the codebase.

*Note: No Next.js, Redux, Zustand, or Axios were introduced, strictly adhering to the approved stack.*

---

## 4. Final Frontend Directory Structure

```text
frontend/
├── public/
│   └── favicon.svg
├── src/
│   ├── app/
│   │   ├── App.tsx
│   │   ├── providers.tsx
│   │   └── router.tsx
│   ├── components/
│   │   ├── common/
│   │   │   ├── FoundationPreview.tsx
│   │   │   ├── Header.tsx
│   │   │   └── SidebarPreview.tsx
│   │   └── ui/
│   ├── features/
│   │   ├── citations/
│   │   │   └── index.ts
│   │   ├── reports/
│   │   │   └── index.ts
│   │   ├── research/
│   │   │   └── index.ts
│   │   └── sessions/
│   │       └── index.ts
│   ├── hooks/
│   ├── layouts/
│   │   └── WorkspaceLayout.tsx
│   ├── lib/
│   │   ├── api/
│   │   │   ├── client.ts
│   │   │   ├── exports.ts
│   │   │   └── sessions.ts
│   │   ├── sse/
│   │   │   ├── reader.ts
│   │   │   └── types.ts
│   │   └── utils/
│   │       └── cn.ts
│   ├── styles/
│   │   └── globals.css
│   ├── types/
│   │   └── index.ts
│   └── main.tsx
├── .env
├── .env.example
├── index.html
├── package.json
├── postcss.config.js
├── tailwind.config.js
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts
```

---

## 5. Design Token Architecture

The design system maps semantic CSS variables defined in [`src/styles/globals.css`](file:///d:/Documents/PROJECTS/Desearch%20AI/frontend/src/styles/globals.css) to Tailwind CSS tokens in [`tailwind.config.js`](file:///d:/Documents/PROJECTS/Desearch%20AI/frontend/tailwind.config.js):

```css
:root {
  --background: 30 5% 8%;         /* #141312 - warm near-black canvas */
  --sidebar: 30 5% 10%;           /* #1A1917 - differentiated dark sidebar */
  --surface: 30 5% 13%;           /* #22201D - dark surface */
  --surface-elevated: 30 5% 16%;  /* #292723 - dark elevated surface */
  --surface-hover: 30 5% 18%;     /* #2E2C28 - hover state */
  
  --foreground: 38 30% 97%;       /* #FBF9F5 - warm off-white text */
  --muted-foreground: 38 8% 60%;  /* #A39E93 - muted warm-gray text */
  --text-muted: 38 6% 45%;        /* #78736A - soft muted text */
  
  --border: 40 6% 17%;            /* #2E2C28 - warm border */
  --border-subtle: 40 6% 14%;     /* #262420 - subtle warm border */
  
  --accent: 11 68% 53%;           /* #D95338 - terracotta coral primary accent */
  --accent-hover: 11 65% 45%;     /* #BC4128 - deep terracotta hover */
  --accent-foreground: 0 0% 100%; /* #FFFFFF - text on accent */
  
  --destructive: 0 72% 51%;       /* #DC2626 - crimson error */
  --radius: 0.5rem;               /* 8px radius */
}
```

---

## 6. Typography Architecture

Two explicit typography roles were established:

1. **Editorial / Research Reading Typography**: `EB Garamond` (Serif). Applied to research titles, section headings, and report body content via `.font-serif-editorial`.
2. **Interface UI Typography**: `Inter` (Sans-Serif). Applied to navigation, sidebars, buttons, input controls, and metadata via `.font-sans-ui`.
3. **Code & Diagnostic Typography**: `JetBrains Mono` (Monospace). Applied to status indicators, timestamps, and IDs via `.font-mono-code`.

---

## 7. Routing Architecture

React Router v6 is configured in [`src/app/router.tsx`](file:///d:/Documents/PROJECTS/Desearch%20AI/frontend/src/app/router.tsx) with a unified `WorkspaceLayout` shell:

- `/` → New Research Canvas (`FoundationPreview`)
- `/research` → New Research Canvas (`FoundationPreview`)
- `/research/:sessionId` → Active Research Session (`FoundationPreview`)
- `*` → Redirects gracefully to `/`

---

## 8. Provider Architecture

Application-level providers are composed in [`src/app/providers.tsx`](file:///d:/Documents/PROJECTS/Desearch%20AI/frontend/src/app/providers.tsx):
- `QueryClientProvider` initialized with `staleTime: 5 mins`, `retry: 1`, `refetchOnWindowFocus: false`.

---

## 9. API Client Architecture

Implemented in [`src/lib/api/client.ts`](file:///d:/Documents/PROJECTS/Desearch%20AI/frontend/src/lib/api/client.ts):
- Standardized `apiFetch<T>(endpoint, options)` with configurable `API_BASE_URL` (`import.meta.env.VITE_API_BASE_URL`).
- `ApiClientError` class normalizing FastAPI HTTP 4xx/5xx responses.
- `sessionsApi` in [`src/lib/api/sessions.ts`](file:///d:/Documents/PROJECTS/Desearch%20AI/frontend/src/lib/api/sessions.ts) providing `createSession`, `listSessions`, `getSession`, `deleteSession`, and `renameSession`.
- `exportsApi` in [`src/lib/api/exports.ts`](file:///d:/Documents/PROJECTS/Desearch%20AI/frontend/src/lib/api/exports.ts) providing `getExportUrl` and `downloadExport`.

---

## 10. SSE Foundation

Implemented in [`src/lib/sse/reader.ts`](file:///d:/Documents/PROJECTS/Desearch%20AI/frontend/src/lib/sse/reader.ts):
- `streamResearchProgress(options)` sends a `POST` request to `/api/v1/orchestrator/stream` with a JSON payload.
- Reads `response.body.getReader()` incrementally using `TextDecoder`.
- Parses SSE `event:` and `data:` frames and dispatches typed `ProgressEvent` callbacks to `onEvent`.
- Integrates `AbortController` for cancellation.

---

## 11. Environment Configuration

- **`frontend/.env.example`**:
  ```env
  VITE_API_BASE_URL=http://127.0.0.1:8000
  ```
- **`frontend/.env`**: Configured for local development.

---

## 12. Security Boundary

- **0 Secrets in Browser**: No `OPENROUTER_API_KEY`, `EXA_API_KEY`, `FIRECRAWL_API_KEY`, or `SUPABASE_SERVICE_ROLE_KEY` are contained in frontend code or environment variables.
- **Single Target Origin**: All network traffic from the browser targets the FastAPI backend (`http://127.0.0.1:8000`).

---

## 13. Accessibility Foundation

- Semantic HTML tags (`<header>`, `<aside>`, `<main>`, `<button>`).
- Explicit focus ring styling (`--focus-ring`).
- `@media (prefers-reduced-motion: reduce)` rules included in `globals.css` disabling non-essential transitions and animations for users with motion sensitivity.

---

## 14. Responsive Foundation

- Mobile breakpoint conventions established in `tailwind.config.js` (`md: 768px`).
- Desktop renders persistent 260px sidebar; Mobile hides sidebar off-canvas.

---

## 15. Files Created

- `frontend/.env.example`
- `frontend/.env`
- `frontend/package.json`
- `frontend/tsconfig.json`
- `frontend/tsconfig.node.json`
- `frontend/vite.config.ts`
- `frontend/postcss.config.js`
- `frontend/tailwind.config.js`
- `frontend/index.html`
- `frontend/public/favicon.svg`
- `frontend/src/styles/globals.css`
- `frontend/src/lib/utils/cn.ts`
- `frontend/src/types/index.ts`
- `frontend/src/lib/api/client.ts`
- `frontend/src/lib/api/sessions.ts`
- `frontend/src/lib/api/exports.ts`
- `frontend/src/lib/sse/types.ts`
- `frontend/src/lib/sse/reader.ts`
- `frontend/src/app/providers.tsx`
- `frontend/src/app/router.tsx`
- `frontend/src/app/App.tsx`
- `frontend/src/layouts/WorkspaceLayout.tsx`
- `frontend/src/components/common/Header.tsx`
- `frontend/src/components/common/SidebarPreview.tsx`
- `frontend/src/components/common/FoundationPreview.tsx`
- `frontend/src/main.tsx`
- `frontend/src/features/research/index.ts`
- `frontend/src/features/sessions/index.ts`
- `frontend/src/features/reports/index.ts`
- `frontend/src/features/citations/index.ts`

---

## 16. Files Modified

- `docs/reports/P3-01_FRONTEND_FOUNDATION_REPORT.md` [NEW]

---

## 17. Validation Summary

- [x] **React Component Tree**: Mounts cleanly without warnings.
- [x] **Type Safety**: All TypeScript definitions strict and complete.
- [x] **Design Tokens**: Verified warm near-black background (`#141312`), dark sidebar (`#1A1917`), dark surface (`#22201D`), terracotta coral accent (`#D95338`), and warm stone border (`#2E2C28`).
- [x] **Typography**: Verified `Inter` UI font and `EB Garamond` editorial report font.
- [x] **Backend Boundary**: Confirmed browser communicates only with FastAPI.

---

## 18. Known Limitations & Deferred Work

### IMPLEMENTED NOW (P3-01):
- Vite + React 18 + TypeScript + Tailwind CSS build pipeline.
- Centralized semantic design token system & typography roles.
- React Router SPA routing (`/` and `/research/:sessionId`).
- TanStack Query provider integration.
- Typed API client & session API endpoints (`sessionsApi`, `exportsApi`).
- Low-level fetch-based SSE stream reader module (`streamResearchProgress`).
- Foundation preview page proving mounting, security, and styling.

### DEFERRED TO P3-02+:
- **P3-02**: Application Shell & Sidebar History Management.
- **P3-03**: Research Composer & New Research Form.
- **P3-04**: Real-Time SSE Research Progress & Shimmer UI.
- **P3-05**: Synthesis Report Document, Reports Drawer & Inline Citations.
- **P3-06**: Research Error Handling & Mobile Responsiveness Polish.

---

## 19. Backend Preservation Confirmation

> **CONFIRMED:** Zero backend files were modified during ticket P3-01. The Python codebase in `backend/` remains 100% untouched.
