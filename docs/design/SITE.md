# Desearch AI — Site Architecture & Information System (`SITE.md`)

> **Product:** Desearch AI — Deep Research. Smarter Decisions.  
> **Role:** Master Site Architecture & Screen State Information System  
> **Status:** APPROVED ARCHITECTURAL SPECIFICATION  
> **Version:** 1.1.0  
> **Target Environment:** Single-Page Persistent Research Workspace  

---

## 1. Product Shell Architecture

Desearch AI is architected as a persistent, single-page **Research Workspace** rather than a traditional multi-page SaaS web application. The core product experience revolves around three primary spatial zones:

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ App Header / Brand Navigation                                                                    │
├──────────────────────┬───────────────────────────────────────────────────┬───────────────────────┤
│ Zone 1: Left Sidebar │ Zone 2: Center Research Workspace                 │ Zone 3: Right Drawer  │
│ (Persistent 260px)   │ (68–75ch Constrained Editorial Reading Canvas)    │ (Contextual 420px)    │
│                      │                                                   │                       │
│ + New Research       │ User Research Query                               │ Canonical Report      │
│                      │                                                   │                       │
│ Research History     │ Real-Time Semantic Progress (SSE)                 │ Source URLs           │
│  - Today             │                                                   │                       │
│  - Yesterday         │ Synthesized Research Answer + Inline Citations    │ PDF / MD Exports      │
│  - 7 Days            │                                                   │                       │
│                      │ Supporting Evidence Sources                       │                       │
│ Settings (Shell)     │                                                   │                       │
│ Account (Shell)      │ Research Composer (Auto-resizing input)           │                       │
└──────────────────────┴───────────────────────────────────────────────────┴───────────────────────┘
```

### 1.1 Spatial Zone Definitions
- **Zone 1: Persistent Left Sidebar (`260px` Expanded / `56px` Collapsed Rail)**: Session navigation, new research initialization, sidebar history search filter, grouped historical research sessions, and shell utility affordances.
- **Zone 2: Center Research Workspace (`Flex 1`, `max-width: 720px` reading container)**: The primary research thread displaying user query, real-time SSE progress stages, synthesized editorial answer, inline citations `[1]`, supporting sources, and the bottom composer.
- **Zone 3: Contextual Right Reports Drawer (`420px` Sliding Panel / `60%` Expanded Viewer)**: Floating evidence panel overlaying the workspace to browse session reports, inspect source URLs, and execute PDF/Markdown report downloads.

---

## 2. Screen & State Navigation Map

```text
                               ┌───────────────────────────┐
                               │  SCREEN 01: New Research  │
                               │   (Empty Shell + Hero)    │
                               └─────────────┬─────────────┘
                                             │ User submits query
                                             ▼
                               ┌───────────────────────────┐
                               │   SCREEN 02: Active SSE   │
                               │    (Planning Stage)       │
                               └─────────────┬─────────────┘
                                             │ Stage progression
                                             ▼
                               ┌───────────────────────────┐
                               │   SCREEN 03: Active SSE   │
                               │   (Evidence Collection)   │
                               └─────────────┬─────────────┘
                                             │ Workflow completed
                                             ▼
                               ┌───────────────────────────┐
                               │ SCREEN 04: Finished State │
                               │ (Report Answer + Sources) │
                               └──────┬──────────┬───┬─────┘
                                      │          │   │
           ┌──────────────────────────┘          │   └──────────────────────────┐
           ▼                                     ▼                              ▼
┌───────────────────────────┐      ┌───────────────────────────┐    ┌───────────────────────────┐
│ SCREEN 05: Citation Hover │      │  SCREEN 06: Reports Drawer│    │ SCREEN 08: History Action │
│   (Popover preview)       │      │   (420px Sliding Overlay) │    │  (Rename/Delete Session)  │
└───────────────────────────┘      └─────────────┬─────────────┘    └───────────────────────────┘
                                                 │ Click "Open Report"
                                                 ▼
                                   ┌───────────────────────────┐
                                   │  SCREEN 07: Report Viewer │
                                   │  (60% Viewport Modal)     │
                                   └───────────────────────────┘

[Mobile Viewport Variations]
  ├── SCREEN 10: Mobile Core Experience (390px Viewport)
  └── SCREEN 11: Mobile Reports Sheet (Full-Screen Overlay)
```

---

## 3. Information Architecture

### 3.1 Desktop Information Architecture (≥ 1024px)
1. **Persistent Header Bar**:
   - Brand Identity: `Desearch AI` logo mark & workspace indicator.
   - Contextual Reports Action: Top-right `Reports` trigger with active source count badge.
2. **Left Navigation Sidebar**:
   - Primary Action: `+ New Research` CTA button.
   - History Search Filter: Real-time client-side session title filter in sidebar.
   - Grouped Session List: `Today`, `Yesterday`, `Previous 7 Days`, `Older`.
   - Session Row: Title, relative timestamp, hover actions (`Rename`, `Delete`).
   - Bottom Utilities: Settings & User Account shell triggers (`BACKEND-DEPENDENT / TO VERIFY`).
3. **Main Reading Area**:
   - User Query Block: Clean heading displaying original user prompt.
   - SSE Stage Progress: Real-time semantic progress indicator with active-stage shimmer.
   - Synthesized Answer: Constrained editorial typography container (`68–75ch` line-length).
   - Inline Citations: Interactive numeric badges (`[1]`, `[2]`).
   - Supporting Sources: Compact source list with favicons, domain names, and excerpts.
   - Report Artifact Card: Summary badge linking directly to the full report.
   - Composer: Bottom-anchored auto-resizing text input (`"Start another research question"` in completed state).

### 3.2 Mobile Information Architecture (< 768px)
1. **Compact Navigation Bar**: Top bar displaying hamburger menu trigger, logo mark, and Reports badge.
2. **Off-Canvas Navigation Drawer**: Slides from left covering 85% screen width, housing `+ New Research` button, sidebar search, and session history.
3. **Full-Width Workspace Canvas**: Single-column layout maximizing text readability across mobile viewports.
4. **Full-Screen Mobile Reports Sheet**: Reports drawer opens as an interactive full-screen sheet overlay with straightforward `[Done]` / `[Close]` controls.

---

## 4. Navigation & Workspace Behaviors

### 4.1 Left Sidebar Controls
- **Default State**: Expanded on desktop (`260px`).
- **Collapse Mechanism**: Manual user toggle button or `Cmd/Ctrl + [` keyboard shortcut collapses sidebar to a mini-rail (`56px`).
- **NO Hover Expansion**: Hovering over the collapsed rail does NOT expand the sidebar, avoiding unintended layout shifting.
- **Active Session State**: Indicated by a subtle warm surface background (`#F5F2EC`) and left border accent line (`#D95338`). Primary coral color is **not** wasted as a full row fill.

### 4.2 History Management Actions
- **Supported Actions**: `Rename Session` (inline editable title text input) and `Delete Session` (destructive confirmation popover calling `DELETE /api/v1/sessions/{id}`).
- **Excluded Unbacked Actions**: `Pin`, `Share`, `Duplicate`, and `Archive` actions are excluded as they have no underlying backend API support in V1.

---

## 5. Research Lifecycle & Real-Time Progress UX

```text
[User Submits Query] ──► [workflow.started] ──► [planner.started (Shimmer)] ──► [research.searching (Shimmer)]
                                                                                       │
[workflow.completed] ◄── [reviewer.completed] ◄── [writer.started (Shimmer)] ◄── [research.extracting (Shimmer)]
```

### 5.1 Real-Time Stage Progression Rules
1. **Semantic-First Labels**: Raw backend SSE events are translated into clear human-readable stages (`Planning...`, `Searching sources...`, `Reading sources...`, `Writing report...`, `Reviewing findings...`). Numerical percentage progress bars are excluded from primary UI.
2. **Active Stage Shimmer**: Luminous left-to-right text shimmer animation applies strictly to **only the single currently active stage**. Completed stages display static green checkmarks (`✓`); future stages remain muted grey (`#8C877E`).
3. **Completion Collapse**: Upon reaching `workflow.completed`, the progress list collapses into a clean summary bar (`✓ Research completed · 8 sources · 1m 42s`) with an `[Expand Trace]` toggle.
4. **Failure Handling**: If `workflow.failed` is emitted, execution halts cleanly, displaying neutral failure copy `"Research couldn't be completed. Please try again."` and a `Retry` action. Stack traces and raw API error details are strictly hidden.

---

## 6. Evidence System & Reports Architecture

### 6.1 Unified Evidence Triad
Citations, Sources, and Reports form an interconnected evidence graph:

```text
┌────────────────────────┐      ┌────────────────────────┐      ┌────────────────────────┐
│  Inline Citation [1]   │ ────►│   Citation Popover     │ ────►│    Reports Drawer      │
│  (Interactive Badge)   │      │  (Title, Domain, Text) │      │ (Full Metadata & List) │
└────────────────────────┘      └────────────────────────┘      └───────────┬────────────┘
                                                                            │ Click "Open"
                                                                            ▼
                                                                ┌────────────────────────┐
                                                                │  Expanded Viewer Modal │
                                                                │ (Serif Reading Canvas) │
                                                                └────────────────────────┘
```

1. **Inline Citation (`[1]`)**: Hovering displays `CitationPopover` with source title, domain name, snippet excerpt, and external `[Open Source ↗]` link. No synthetic authority/confidence percentages or verification badges are shown.
2. **Reports Drawer (`420px`)**: Clicking any citation or `Reports` button slides out the drawer overlay, highlighting the corresponding source item.
3. **Expanded Viewer (`60% Width`)**: Clicking `Open Full Report` launches the modal viewer formatted in editorial serif typography (`EB Garamond`) for deep long-form report reading.
4. **Report Export Actions**: Direct triggers for backend export endpoints:
   - `GET /api/v1/reports/{id}/export?format=pdf`
   - `GET /api/v1/reports/{id}/export?format=markdown`

---

## 7. Responsive Behavior & Viewport Breakpoints

- **Desktop Large (≥ 1280px)**: 260px expanded sidebar + 720px centered reading area + 420px floating drawer overlay.
- **Desktop Standard (1024px – 1279px)**: 260px sidebar + flex reading area + 400px drawer overlay.
- **Tablet (768px – 1023px)**: 56px collapsed mini-rail + 100% flex reading area + 50% width overlay sheet.
- **Mobile (< 768px)**: Hidden off-canvas sidebar + 100% viewport width reading area + 100% full-screen reports sheet overlay with explicit `[Done]` close button.

---

## 8. Screen Target Inventory (11 Generations)

| Screen ID | Target Viewport | Screen Purpose & State | Key Components Established |
| :--- | :--- | :--- | :--- |
| **SCREEN 01** | Desktop (`1440x900`) | New Research Empty Workspace | AppShell, Sidebar (260px), Hero Composer, Example Prompts |
| **SCREEN 02** | Desktop (`1440x900`) | Active Research: Planning Stage | User Query Block, Semantic Progress (`Planning...` shimmer), Busy Composer |
| **SCREEN 03** | Desktop (`1440x900`) | Active Research: Evidence Collection | Completed Planning (`✓`), Active Searching/Extracting shimmer, Discovered sources |
| **SCREEN 04** | Desktop (`1440x900`) | Completed Research Finished Answer | Collapsed Progress Bar, Editorial Report Answer, Citations `[1]`, Sources List, Composer (`"Start another research question"`) |
| **SCREEN 05** | Desktop (`1440x900`) | Inline Citation Popover Hover | CitationPopover overlay, Source Title, Excerpt, Domain link (No fake scores) |
| **SCREEN 06** | Desktop (`1440x900`) | Reports & Evidence Drawer Open | Contextual 420px sliding drawer, Report Info, Research Sources List, PDF/MD Exports |
| **SCREEN 07** | Desktop (`1440x900`) | Expanded Long-Form Report Viewer | Distraction-free 60% modal overlay, Serif typography, TOC, Export buttons |
| **SCREEN 08** | Desktop (`1440x900`) | Session History Management | Sidebar focus, History search, Session group hover (`Rename`, `Delete` actions) |
| **SCREEN 09** | Desktop (`1440x900`) | Graceful Research Execution Failure | Clean failure banner, Neutral error copy (`"Research couldn't be completed. Please try again."`), Retry trigger |
| **SCREEN 10** | Mobile (`390x844`) | Mobile Core Completed Workspace | Mobile Top Navigation, Off-Canvas Trigger, Full-Width Reading Canvas, Mobile Composer |
| **SCREEN 11** | Mobile (`390x844`) | Mobile Reports Full-Screen Sheet | Full-Screen Sheet overlay, Touch-friendly Sources List, PDF & MD Export buttons, Close control |

---

## 9. Programmatically Derived States (No Dedicated Generation Wasted)

To ensure maximum generation efficiency, the following minor variations are documented to be programmatically derived from the 11 primary Stitch screens:
- `Writing report...` & `Reviewing findings...` active shimmer states (derived from SCREEN 02/03).
- Composer typing auto-resize animation (derived from SCREEN 01/04).
- Sidebar collapsed 56px rail (derived from SCREEN 01).
- Sidebar search filtering empty result state (derived from SCREEN 08).
- Intermediate source count variations (1 source, 4 sources, 12 sources).
- PDF vs. Markdown download triggering toast states.

---

## 10. Backend Boundary Matrix

| Feature / UI Component | Backend Status | Backend Endpoint / Technical Mapping |
| :--- | :--- | :--- |
| **Create Research Session** | `SUPPORTED NOW` | `POST /api/v1/sessions` |
| **Real-Time Progress SSE** | `SUPPORTED NOW` | `POST /api/v1/orchestrator/stream` |
| **Fetch Session History** | `SUPPORTED NOW` | `GET /api/v1/sessions` (Supabase PostgreSQL) |
| **Rename / Delete Session** | `SUPPORTED NOW` | `PATCH` / `DELETE /api/v1/sessions/{id}` |
| **PDF Export** | `SUPPORTED NOW` | `GET /api/v1/reports/{id}/export?format=pdf` |
| **Markdown Export** | `SUPPORTED NOW` | `GET /api/v1/reports/{id}/export?format=markdown` |
| **Multi-turn In-Session Memory**| `BACKEND-DEPENDENT` | Requires session thread context retention (`"Start another research question"` in V1) |
| **File / Document Attachment** | `BACKEND-DEPENDENT` | Requires document ingestion pipeline (`DESIGNED / FUTURE-DEPENDENT`) |
| **Stop / Cancel Research** | `BACKEND-DEPENDENT` | Requires SSE task cancellation (Busy state in V1) |
| **Settings & User Account** | `BACKEND-DEPENDENT` | Shell affordances only; no auth/billing invented |
