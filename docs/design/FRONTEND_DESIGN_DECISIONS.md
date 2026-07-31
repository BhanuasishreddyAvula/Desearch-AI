# Frontend Design Architectural Decisions (`FRONTEND_DESIGN_DECISIONS.md`)

> **Project:** Desearch AI  
> **Organization:** BhanuasishreddyAvula's Org  
> **Role:** Frontend Design Systems Architect  
> **Status:** APPROVED DECISION LOG  
> **Version:** 1.1.0  
> **Date:** 2026-07-30  

---

## 1. Executive Summary

This document records the core design and architectural decisions made while creating the **Desearch AI** frontend design system foundation ([`docs/design/DESIGN.md`](./DESIGN.md)). Each decision details the rationale, trade-offs, and backend integration alignment.

---

## 2. Decision Log

### Decision 1: Persistent 3-Column Research Workspace over Generic SaaS Dashboard
- **Decision**: Design the application as a persistent 3-column research workspace (`Sidebar` | `Research Canvas` | `Reports Drawer`) rather than a multi-page dashboard with cards, deals, or analytics widgets.
- **Rationale**: Desearch AI is a deep research tool. Users start with a question and expect an intensive, cited synthesis. A dashboard layout creates unnecessary navigation overhead and distracts from reading and analysis.
- **Trade-off**: Requires careful viewport management and responsive drawer overlays for smaller screen sizes.

### Decision 2: Desktop Sidebar Expanded by Default with Manual Toggle (No Hover Expansion)
- **Decision**: Keep the desktop sidebar expanded (`260px`) by default, allowing explicit manual collapse to a mini-rail (`56px`). Prohibit hover-to-expand behavior.
- **Rationale**: Research history is a core product feature. Hover-to-expand sidebars trigger accidental viewport shifting while reading long reports. Explicit user control respects user intent and reading focus.
- **Trade-off**: Consumes 260px of horizontal viewport width on desktop, requiring constrained line-lengths for the main reading area.

### Decision 3: Editorial Research Documents over Speech Chat Bubbles
- **Decision**: Present AI research responses as structured, editorial research documents rather than rounded messaging speech bubbles.
- **Rationale**: Multi-page, multi-section research reports containing findings, risks, evidence tables, and citations look unreadable inside narrow chat bubbles. An editorial document layout with constrained reading width (`68–75ch`) optimizes deep reading comprehension.
- **Trade-off**: Requires separate styling for user query blocks vs. AI report documents.

### Decision 4: Claude-Derived Warm Cream Foundation without Cloning Claude
- **Decision**: Use a warm cream/off-white canvas (`#FBF9F5`), deep charcoal text (`#1F1E1C`), and terracotta coral accent (`#D95338`), pairing `Inter` (sans) with `EB Garamond` (serif). Strictly prohibit Anthropic/Claude branding, logos, or font dependencies.
- **Rationale**: A warm, low-contrast cream canvas reduces eye strain during long reading sessions compared to stark cold white or dark mode. Using open fonts (`Inter` and `EB Garamond`) establishes an independent, high-end editorial identity for Desearch AI.
- **Trade-off**: Requires custom color token mappings rather than standard out-of-the-box utility defaults.

### Decision 5: Open Composition Over Card Heaviness
- **Decision**: The warm cream canvas (`#FBF9F5`) must remain visually dominant. Do NOT wrap every response paragraph, source item, sidebar row, and progress stage inside white card boxes. White/elevated surfaces (`#FFFFFF`) are restricted to genuine interactive boundaries (composer, drawer, popovers, report artifact cards).
- **Rationale**: Wrapping every content element in white cards creates a visual grid nightmare, making the app look like a generic SaaS dashboard. Open composition with subtle dividers and generous whitespace establishes an editorial research character.
- **Trade-off**: Requires strict discipline in surface token usage.

### Decision 6: Semantic-First Progress Streaming (No Large Percentage Bars)
- **Decision**: Primary progress UI displays human-readable semantic stages (`Planning...`, `Searching sources...`, `Reading sources...`, `Writing report...`, `Reviewing findings...`). Numerical percentage values are treated as backend metadata rather than large numerical progress bars.
- **Rationale**: Users care about what the AI is currently doing (searching, reading, writing), not abstract percentage numbers. Semantic stage text provides meaningful feedback.
- **Trade-off**: Requires translating raw SSE events into clean UI stage strings.

### Decision 7: Single Active SSE Stage Shimmer
- **Decision**: Apply a subtle left-to-right luminous text shimmer animation strictly to ONLY the currently executing research stage. Completed stages display static green checkmarks (`✓`), while future stages remain muted grey.
- **Rationale**: Multiple simultaneous glowing or pulsing elements create visual chaos and user anxiety. Single-stage shimmer clearly communicates real-time progress while maintaining a calm interface.
- **Trade-off**: Requires tracking exact active stage state from incoming SSE event streams.

### Decision 8: Removal of Synthetic Citation Scores
- **Decision**: Citation popovers (`CitationPopover`) display only supported source metadata: source title, domain, short excerpt/snippet (when available), and external URL link. Synthetic confidence percentages, authority scores, or verification badges are strictly prohibited.
- **Rationale**: The current backend does not produce an empirical citation confidence metric. Fabricating synthetic scores misleads users and undermines trust.
- **Trade-off**: Citation previews rely purely on clean source metadata.

### Decision 9: Busy/Disabled Composer State (Stop/Cancel is Backend-Dependent)
- **Decision**: During active research, the composer displays a busy/disabled state (`Research in progress...`). A Stop/Cancel research button is marked as `FUTURE / BACKEND-DEPENDENT` and is not visually promised in initial Stitch screens.
- **Rationale**: True execution workflow cancellation is not currently supported by backend services. Promising a stop button in the UI that cannot cancel backend processing would create broken user expectations.
- **Trade-off**: Users must wait for the workflow to complete or fail.

### Decision 10: Restrained Settings and Account Shell Affordances
- **Decision**: Settings and Account triggers in the sidebar footer exist strictly as restrained shell affordances marked `BACKEND-DEPENDENT / TO VERIFY`. Stitch must NOT invent billing, subscriptions, teams, authentication flows, or API key management screens.
- **Rationale**: Desearch AI backend V1 focuses on core research session execution, evidence synthesis, and report export. Inventing complex auth/billing UI flows introduces scope creep unbacked by backend logic.
- **Trade-off**: Settings and account triggers display clean placeholder states in V1.

### Decision 11: Two-Tier Reports Drawer + Expanded Viewer Architecture
- **Decision**: Use a 2-tier report viewing system: a sliding right drawer (`420px`) for contextual browsing and source inspection, and an expanded overlay viewer (`60%` width) for long-form report reading.
- **Rationale**: A 420px drawer is too narrow for comfortable long-form reading, but navigating users away to an external page breaks research session context. The 2-tier architecture provides both fast contextual inspection and deep reading.
- **Trade-off**: Requires managing two distinct drawer/modal state overlays in the application shell.

---

## 3. Backend Capability Alignment Matrix

| Feature / UI Component | Backend Status | Backend Endpoint / Technical Mapping |
| :--- | :--- | :--- |
| **Session Creation** | `SUPPORTED NOW` | `POST /api/v1/sessions` |
| **Real-Time Progress SSE** | `SUPPORTED NOW` | `POST /api/v1/orchestrator/stream` (`workflow.started` to `workflow.completed`) |
| **Session History List** | `SUPPORTED NOW` | `GET /api/v1/sessions` (persisted in Supabase PostgreSQL) |
| **Rename / Delete Session** | `SUPPORTED NOW` | `PATCH` / `DELETE /api/v1/sessions/{session_id}` |
| **PDF Export** | `SUPPORTED NOW` | `GET /api/v1/reports/{session_id}/export?format=pdf` |
| **Markdown Export** | `SUPPORTED NOW` | `GET /api/v1/reports/{session_id}/export?format=markdown` |
| **Multi-Turn Chat Memory** | `BACKEND-DEPENDENT` | Requires session thread context retention in backend |
| **File / Document Upload** | `BACKEND-DEPENDENT` | Requires file upload & chunking pipeline |
| **Stop Execution Button** | `BACKEND-DEPENDENT` | Requires SSE stream task termination (Busy state in V1) |
| **Settings & User Account** | `BACKEND-DEPENDENT` | Shell affordances only; no auth/billing invented |
| **In-Session History Search**| `BACKEND-DEPENDENT` | Implemented client-side initially |

---

## 4. Stitch Screen-Prompt Delimiter Rule

To ensure reliable screen generation during the upcoming Stitch iteration phase, the following prompt formatting constraint is strictly enforced for all Stitch prompt roadmap files (`SITE.md`, `next-prompt.md`):

> **STITCH PROMPT DELIMITER CONSTRAINT**:  
> Every independent screen prompt MUST be separated by **EXACTLY ONE BLANK LINE**.

### Correct Format:
```text
SCREEN 01: <Complete detailed prompt for Screen 1>

SCREEN 02: <Complete detailed prompt for Screen 2>

SCREEN 03: <Complete detailed prompt for Screen 3>
```

### Rationale:
The Stitch generation runner parses prompt files by splitting on double newlines (`\n\n`). If two screen prompts are directly adjacent without an empty blank line, the parser will treat them as a single combined instruction, corrupting screen generation targets.

Therefore, all future Stitch generation prompt files generated for Desearch AI MUST preserve blank-line separation between screen targets without exception.
