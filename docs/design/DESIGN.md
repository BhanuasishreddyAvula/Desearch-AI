# Desearch AI — Master Frontend Design System Specification (`DESIGN.md`)

> **Product:** Desearch AI — Deep Research. Smarter Decisions.  
> **Role:** Master Visual & Interaction Design System Source of Truth  
> **Status:** APPROVED DESIGN SPECIFICATION  
> **Version:** 1.1.0  
> **Target Framework:** React + TailwindCSS + Radix/shadcn Primitives  

---

## 1. Product Identity & Design Atmosphere

### 1.1 Product Character
Desearch AI is an evidence-backed AI research workspace designed for engineers, analysts, and decision-makers who require rigorous, cited synthesis rather than conversational chat.

The visual character is governed by nine core attributes:
- **CALM**: Low-friction neutral palette, generous whitespace, zero visual clutter.
- **SERIOUS**: Editorial typography, precise layout grids, dignified hierarchy.
- **RESEARCH-ORIENTED**: Document-first layout, explicit inline citations, prominent source attribution.
- **INTELLIGENT**: Clear state transitions, real-time stage progress visibility, structured evidence.
- **EDITORIAL**: High-contrast serif headings paired with humanist sans body typography.
- **MODERN**: Sleek micro-interactions, subtle borders, restrained radii.
- **FAST**: Instant feedback, optimistic UI updates, smooth streaming progress transitions.
- **PRECISE**: Exact data formatting, clear time/token metrics, deterministic export surfaces.
- **TRUSTWORTHY**: No hidden model state, clear source lineage, explicit failure boundaries.

### 1.2 Anti-Patterns & Prohibited Styling
To maintain product distinction and avoid generic AI tropes, the following are strictly prohibited:
- ❌ **NO** purple/blue AI gradients or neon glowing borders.
- ❌ **NO** glassmorphism overlays or frosted blur backgrounds across main surfaces.
- ❌ **NO** generic SaaS dashboard widgets, deal cards, or analytics grid blocks.
- ❌ **NO** rounded messaging chat bubbles for long-form research answers.
- ❌ **NO** Claude or Anthropic logos, wordmarks, brand colors, or copied layout artifacts.
- ❌ **NO** model/provider dropdown selectors (`openrouter/free`, `gpt-4o`) in standard user workflows.
- ❌ **NO** multiple simultaneous shimmering/glowing loading states.
- ❌ **NO** hover-to-expand sidebar behaviors.
- ❌ **NO** decorative floating blobs or continuous looping animations.
- ❌ **NO** card heaviness: Do not wrap every response paragraph, source row, and progress stage in white cards.
- ❌ **NO** synthetic authority/confidence scores, relevance percentages, or fake verification badges.

---

## 2. Color Tokens & Surface Palette

The color system uses a warm, editorial cream/off-white canvas with deep charcoal typography and a restrained terracotta coral accent. Colors are specified in natural language, HSL, and HEX for exact implementation precision.

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ Canvas: Warm Cream (#FBF9F5) — Dominant Background                      │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │ Interactive Surface: Clean White (#FFFFFF)                      │   │
│   │   Border: Warm Subtle Border (#E6E2D8)                          │   │
│   │   Accent Action: Terracotta Coral (#D95338)                     │   │
│   └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.1 Core Palette Tokens

| Token Name | Descriptive Character | HSL Value | HEX Code | Functional Role |
| :--- | :--- | :--- | :--- | :--- |
| `--bg-canvas` | Warm Cream Canvas | `hsl(38, 30%, 97%)` | `#FBF9F5` | Main application background canvas (DOMINANT) |
| `--bg-surface` | Clean Off-White Surface | `hsl(0, 0%, 100%)` | `#FFFFFF` | Interactive boundaries: Composer, Popover, Drawer, Cards |
| `--bg-subtle` | Warm Tinted Grey | `hsl(40, 20%, 94%)` | `#F5F2EC` | Hover states, code block backgrounds, tags |
| `--text-primary` | Deep Charcoal | `hsl(30, 5%, 11%)` | `#1F1E1C` | Primary headings, body copy, active text |
| `--text-secondary` | Warm Medium Grey | `hsl(38, 5%, 33%)` | `#57544F` | Subheadings, labels, secondary metadata |
| `--text-muted` | Soft Muted Grey | `hsl(38, 6%, 52%)` | `#8C877E` | Timestamps, placeholder text, disabled icons |
| `--border-subtle` | Warm Subtle Border | `hsl(40, 16%, 87%)` | `#E6E2D8` | Structural dividing lines, subtle borders |
| `--border-strong` | Medium Warm Border | `hsl(40, 12%, 75%)` | `#C4BEB4` | Input focus borders, active panel outlines |
| `--accent-primary` | Terracotta Coral | `hsl(11, 68%, 53%)` | `#D95338` | Primary CTA buttons, active indicators |
| `--accent-hover` | Deep Terracotta | `hsl(11, 65%, 45%)` | `#BC4128` | Hover state for primary buttons |
| `--accent-subtle` | Warm Coral Tint | `hsl(11, 60%, 95%)` | `#FDF3F1` | Selected badge background, citation highlights |
| `--state-success` | Deep Olive Green | `hsl(153, 40%, 30%)` | `#2D6A4F` | Completed status badges, valid exports |
| `--state-warning` | Warm Amber | `hsl(38, 92%, 45%)` | `#D97706` | Truncation warnings, retry notifications |
| `--state-error` | Deep Crimson | `hsl(0, 72%, 51%)` | `#DC2626` | Execution failure banners, validation errors |
| `--focus-ring` | Muted Coral Ring | `hsla(11, 68%, 53%, 0.25)` | `#D9533840` | Accessible keyboard focus outline |

---

## 3. Typography Hierarchy & Rules

The typographic system pairs an accessible humanist sans-serif for UI controls and body reading with a classic open serif for editorial headings, anchored by a clean monospace for code and metrics.

### 3.1 Font Families
- **UI / Controls / Body**: `Inter`, `-apple-system`, `BlinkMacSystemFont`, `sans-serif`
- **Editorial / Report Headings**: `EB Garamond`, `Cormorant Garamond`, `Georgia`, `serif`
- **Monospace / Metrics / Code**: `JetBrains Mono`, `Fira Code`, `Consolas`, `monospace`

### 3.2 Type Scale Specifications

| Element Role | Font Family | Size (px / rem) | Weight | Line Height | Letter Spacing |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Workspace Title (H1)** | EB Garamond | `28px / 1.75rem` | 600 (SemiBold) | 1.25 | `-0.02em` |
| **Report Title (H1)** | EB Garamond | `32px / 2.0rem` | 600 (SemiBold) | 1.2 | `-0.02em` |
| **Section Heading (H2)** | EB Garamond | `22px / 1.375rem` | 600 (SemiBold) | 1.3 | `-0.01em` |
| **Subsection (H3)** | Inter | `16px / 1.0rem` | 600 (SemiBold) | 1.4 | `0em` |
| **Body Reading** | Inter | `15px / 0.9375rem` | 400 (Regular) | 1.6 | `0em` |
| **UI Control / Button** | Inter | `14px / 0.875rem` | 500 (Medium) | 1.25 | `0em` |
| **Sidebar Item** | Inter | `14px / 0.875rem` | 400 (Regular) | 1.3 | `0em` |
| **Metadata / Timestamps** | Inter | `12px / 0.75rem` | 400 (Regular) | 1.4 | `0.01em` |
| **Citation Badge `[1]`** | Inter | `11px / 0.6875rem` | 600 (SemiBold) | 1.0 | `0.02em` |
| **Code / Data Snippet** | JetBrains Mono | `13px / 0.8125rem` | 400 (Regular) | 1.5 | `0em` |

---

## 4. Open Composition Rule & Surface Depth

### 4.1 Open Composition Principle
The warm cream canvas (`#FBF9F5`) must remain visually dominant across the application. 
- **DO NOT** encapsulate every response paragraph, source row, progress stage, or sidebar session item in individual white card boxes.
- Prefer open editorial composition, generous whitespace, clean typography, subtle warm dividers (`#E6E2D8`), and soft background tone shifts.
- White/elevated surfaces (`#FFFFFF`) are restricted to genuine structural or interactive boundaries:
  - Composer input container
  - Sliding Reports Drawer & Modals
  - Floating Popovers & Dropdown menus
  - Standalone Report Artifact cards

### 4.2 Spacing Scale (8pt Grid)
- `space-1`: `4px` (Tight padding, badge gaps)
- `space-2`: `8px` (Icon-to-text spacing, inline gaps)
- `space-3`: `12px` (Control padding, list spacing)
- `space-4`: `16px` (Standard container padding)
- `space-5`: `20px` (Header padding, drawer margins)
- `space-6`: `24px` (Section spacing, composer padding)
- `space-8`: `32px` (Major layout gaps, thread margins)
- `space-10`: `40px` (Empty state padding)
- `space-12`: `48px` (Workspace hero margins)

### 4.3 Radii & Elevation
- **Small Controls (`rounded-sm`)**: `4px` (Citations, tag badges, small buttons)
- **Medium Inputs / Rows (`rounded-md`)**: `6px` (Sidebar rows, composer, dropdowns)
- **Large Surfaces (`rounded-lg`)**: `8px` (Drawers, popovers, modals)
- **Depth**: Flat by default (`border: 1px solid var(--border-subtle)`). Subtle elevation shadow (`box-shadow: 0 2px 8px rgba(31, 30, 28, 0.04)`) used only for floating composer focus and dropdown overlays.

---

## 5. Main Application Architecture & Layout

The frontend is designed as a persistent, 3-column research workspace.

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ App Header / Brand                                                                     │
├──────────────────┬─────────────────────────────────────────────────┬───────────────────┤
│ Left Sidebar     │ Center Research Workspace                       │ Right Reports     │
│ (Expanded 260px) │ (68–75ch Line Length Reading Area)              │ Drawer (420px)    │
│                  │                                                 │                   │
│ + New Research   │ User Query Block                                │ Research Report   │
│                  │                                                 │                   │
│ Research History │ Real-Time Semantic Progress (Shimmer active)    │ Source URLs       │
│  - Today         │                                                 │                   │
│  - Yesterday     │ Synthesized Research Answer + Inline Citations │ PDF / MD Export   │
│  - 7 Days        │                                                 │                   │
│                  │ Supporting Sources                              │                   │
│ Settings (Shell) │                                                 │                   │
│ Account (Shell)  │ Composer (Auto-resizing input)                  │                   │
└──────────────────┴─────────────────────────────────────────────────┴───────────────────┘
```

### 5.1 Left Sidebar Architecture
- **Desktop State**: Expanded by default (`width: 260px`). Can be manually collapsed by the user to a mini-rail (`width: 56px`) via explicit toggle button.
- **Expansion Rule**: Manual toggle ONLY. **NO hover-to-expand** to prevent accidental viewport displacement.
- **Sidebar Structure**:
  1. **Header**: Brand logo mark (`Desearch AI`) + Sidebar collapse toggle icon (`Ctrl+[ / Cmd+[`).
  2. **Primary Action**: `+ New Research` button (`var(--accent-primary)` background or outlined surface).
  3. **History Filter**: Search history input field for client-side filtering.
  4. **Research History List**: Grouped chronologically (`Today`, `Yesterday`, `Previous 7 Days`, `Older`). Compact text rows displaying session title and hover actions (`Rename`, `Delete`).
  5. **Footer Utilities**: Settings and User Account triggers (Restrained shell affordances marked `BACKEND-DEPENDENT / TO VERIFY`).

### 5.2 Responsive Strategy
- **Desktop (≥ 1024px)**: Expanded 260px sidebar + center reading canvas + right overlay drawer.
- **Tablet (768px – 1023px)**: Collapsed 56px icon rail by default. Reports drawer opens as a 50% overlay sheet.
- **Mobile (< 768px)**: Sidebar hidden off-canvas (accessible via top-left menu). Main workspace occupies 100% viewport width.

---

## 6. Component System & Interaction Specifications

### 6.1 Research Composer (`ResearchComposer`)
The composer anchors at the bottom of the active workspace or acts as the centered hero on new research sessions.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ Ask a research question...                                                  │
│                                                                             │
│ [📎 Attach]                  [Deep Research mode]                 [ ↑ Send] │
└─────────────────────────────────────────────────────────────────────────────┘
```

- **States**:
  - `Empty`: Displays placeholder `"Ask a research question or enter a topic..."`.
  - `Typing`: Textarea auto-grows vertically up to `max-height: 200px` before internal scrolling activates.
  - `Submitting / Running`: Textarea disabled with busy message (`Research in progress...`). Submit button displays an active processing indicator. **Stop/Cancel button is NOT visually promised** (marked `FUTURE / BACKEND-DEPENDENT`).
  - `Disabled`: Soft muted background with clear tooltip explanation.
- **Keyboard Behavior**: `Enter` submits query; `Shift + Enter` inserts a line break.
- **Action Controls**:
  - **Attach Button**: Formally designed (`DESIGNED / FUTURE-BACKEND-DEPENDENT`).
  - **Mode Indicator**: Subtle product mode tag (`Deep Research`). Provider/model selector dropdowns are **hidden**.
  - **Submit Button**: Compact circular button with upward arrow (`width: 32px`, `height: 32px`, `background: var(--accent-primary)`).

### 6.2 Real-Time SSE Research Progress (`ResearchProgress`)
Translates backend Server-Sent Event (SSE) execution events (`POST /api/v1/orchestrator/stream`) into human-readable, **semantic stage progression**.

#### 6.2.1 Semantic Progress Matrix
| Raw Backend SSE Event | Primary UI Semantic Label | Progress Metadata | Visual Indicator |
| :--- | :--- | :--- | :--- |
| `workflow.started` | Initializing research workflow... | `0%` | Pulse Dot |
| `planner.started` | Planning research strategy... | `5%` | Luminous Text Shimmer (Active) |
| `planner.completed` | Planning complete | `15%` | Green Checkmark `✓` |
| `research.started` | Gathering evidence... | `20%` | Luminous Text Shimmer (Active) |
| `research.searching` | Searching sources... | `25%` | Luminous Text Shimmer (Active) |
| `research.extracting` | Reading sources... | `40%` | Luminous Text Shimmer (Active) |
| `research.completed` | Evidence collection complete | `60%` | Green Checkmark `✓` |
| `writer.started` | Writing report... | `65%` | Luminous Text Shimmer (Active) |
| `writer.completed` | Report written | `80%` | Green Checkmark `✓` |
| `reviewer.started` | Reviewing findings... | `85%` | Luminous Text Shimmer (Active) |
| `reviewer.completed` | Review complete | `95%` | Green Checkmark `✓` |
| `report.persisted` | Saving report... | `98%` | Green Checkmark `✓` |
| `workflow.completed` | Research complete | `100%` | Green Checkmark `✓` |
| `workflow.failed` | Research failed | `100%` | Red Error Badge `✕` |

#### 6.2.2 Semantic-First & Shimmer Rules
- **Semantic First**: The primary progress UI displays semantic text (`Planning...`, `Searching sources...`, `Reading sources...`, `Writing report...`, `Reviewing findings...`). Numerical percentages are backend metadata and **MUST NOT** be rendered as large numerical progress bars.
- **Active Stage Shimmer**: Only the single, currently active stage displays a subtle luminous left-to-right text shimmer. Completed stages show static text with a green checkmark (`✓`); future stages remain muted grey (`#8C877E`).
- **Completion Collapse**: Upon reaching `workflow.completed`, the progress list collapses into a summary bar: `✓ Research completed · 8 sources · 1m 42s` with an `[Expand Trace]` toggle.

### 6.3 Research Response & Readability Surface (`ResearchResponse`)
Synthesized research findings are presented as clean, editorial research documents.
- **Reading Width**: Constrained reading container (`max-width: 720px` / `68–75 characters per line`).
- **Inline Citations (`[1]`, `[2]`)**: Compact, interactive numeric badges (`font-size: 11px`, `color: var(--accent-primary)`).
  - **Hover**: Displays a floating preview popover (`CitationPopover`) showing:
    - Source Title
    - Domain Name
    - Short Excerpt / Snippet (when available)
    - `[Open Source ↗]` Link
  - **NO FAKE SCORES**: Previews MUST NOT display synthetic confidence percentages, authority scores, or verification badges.
  - **Click**: Opens the right-side Reports Drawer scrolled directly to the cited source item.

### 6.4 Reports Drawer & Expanded Artifact Viewer (`ReportsDrawer` & `ReportViewer`)
- **Drawer Surface (`ReportsDrawer`)**: Slides out from the right (`width: 420px`), floating above the workspace. Exposes canonical report overview, source list, and export buttons.
- **Expanded Viewer (`ReportViewer`)**: Triggered when clicking `Open Full Report`. Expands into a distraction-free 60% viewport modal overlay formatted in full editorial serif typography.
- **Export Triggers**: Direct integration with backend endpoints:
  - **PDF Export**: `GET /api/v1/reports/{session_id}/export?format=pdf` (downloads `desearch_report_<id>.pdf`).
  - **Markdown Export**: `GET /api/v1/reports/{session_id}/export?format=markdown` (downloads `desearch_report_<id>.md`).

---

## 7. Component Inventory

The frontend architecture consists of 28 core modular UI components:

```text
Application Shell
 ├── AppShell
 ├── TopHeader
 └── MobileNavigation

Sidebar System
 ├── Sidebar
 ├── SidebarHeader
 ├── NewResearchButton
 ├── HistorySearchInput
 ├── ResearchHistoryGroup
 └── ResearchSessionRow

Workspace System
 ├── ResearchWorkspace
 ├── WorkspaceHeader
 ├── ReportsHeaderButton
 ├── UserQueryBlock
 ├── ResearchProgress
 ├── ProgressStageRow
 └── ProgressSummaryBar

Response & Evidence System
 ├── ResearchResponse
 ├── InlineCitation
 ├── CitationPopover (No synthetic scores)
 ├── SourcesSection
 └── SourceCard

Reports & Artifact System
 ├── ReportArtifactCard
 ├── ReportsDrawer
 ├── ReportViewer Modal
 └── ExportControls (PDF / MD)

Composer System
 ├── ResearchComposer
 ├── AutoResizeTextarea
 ├── AttachmentButton
 ├── ModeBadge
 └── SubmitButton
```

---

## 8. Backend Capability Boundary Matrix

| Feature / UI Element | Integration Status | Backend Endpoint / Technical Mapping |
| :--- | :--- | :--- |
| **Create Research Session** | `SUPPORTED NOW` | `POST /api/v1/sessions` |
| **Real-Time Progress SSE** | `SUPPORTED NOW` | `POST /api/v1/orchestrator/stream` (`workflow.started` to `workflow.completed`) |
| **Session History List** | `SUPPORTED NOW` | `GET /api/v1/sessions` (persisted in Supabase PostgreSQL) |
| **Rename / Delete Session** | `SUPPORTED NOW` | `PATCH` / `DELETE /api/v1/sessions/{id}` |
| **PDF Export** | `SUPPORTED NOW` | `GET /api/v1/reports/{id}/export?format=pdf` |
| **Markdown Export** | `SUPPORTED NOW` | `GET /api/v1/reports/{id}/export?format=markdown` |
| **Multi-turn In-Session Chat**| `BACKEND-DEPENDENT` | Requires session thread context retention in backend |
| **File / Attachment Upload** | `BACKEND-DEPENDENT` | Requires file ingestion pipeline |
| **Stop / Cancel Research** | `BACKEND-DEPENDENT` | Requires SSE stream task termination (Busy state in V1) |
| **Settings & User Account** | `BACKEND-DEPENDENT` | Shell affordances only; no auth/billing invented |
| **Multi-Report Generation** | `FUTURE` | Multiple reports per session |
