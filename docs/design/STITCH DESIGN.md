---
name: Terracotta Editorial Noir
colors:
  surface: '#131313'
  surface-dim: '#131313'
  surface-bright: '#393939'
  surface-container-lowest: '#0e0e0e'
  surface-container-low: '#1c1b1b'
  surface-container: '#201f1f'
  surface-container-high: '#2a2a2a'
  surface-container-highest: '#353534'
  on-surface: '#e5e2e1'
  on-surface-variant: '#e0bfb8'
  inverse-surface: '#e5e2e1'
  inverse-on-surface: '#313030'
  outline: '#a88a84'
  outline-variant: '#59413c'
  surface-tint: '#ffb4a4'
  primary: '#ffb4a4'
  on-primary: '#640c00'
  primary-container: '#f06447'
  on-primary-container: '#580a00'
  inverse-primary: '#ac331b'
  secondary: '#cac6c3'
  on-secondary: '#32302e'
  secondary-container: '#484644'
  on-secondary-container: '#b8b4b2'
  tertiary: '#cac6c2'
  on-tertiary: '#31302e'
  tertiary-container: '#93908d'
  on-tertiary-container: '#2b2a27'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdad3'
  primary-fixed-dim: '#ffb4a4'
  on-primary-fixed: '#3e0500'
  on-primary-fixed-variant: '#8b1b05'
  secondary-fixed: '#e6e2df'
  secondary-fixed-dim: '#cac6c3'
  on-secondary-fixed: '#1c1b1a'
  on-secondary-fixed-variant: '#484644'
  tertiary-fixed: '#e6e2de'
  tertiary-fixed-dim: '#cac6c2'
  on-tertiary-fixed: '#1c1b19'
  on-tertiary-fixed-variant: '#484644'
  background: '#131313'
  on-background: '#e5e2e1'
  surface-variant: '#353534'
typography:
  headline-xl:
    fontFamily: EB Garamond
    fontSize: 48px
    fontWeight: '400'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: EB Garamond
    fontSize: 36px
    fontWeight: '400'
    lineHeight: 44px
  headline-lg-mobile:
    fontFamily: EB Garamond
    fontSize: 28px
    fontWeight: '400'
    lineHeight: 34px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 8px
  container-padding: 24px
  gutter: 16px
  sidebar-width: 280px
  max-content-width: 800px
---

## Brand & Style

This design system embodies a **Premium Editorial** aesthetic, blending the precision of a high-end research tool with the classical elegance of traditional publishing. It is designed for an audience that values depth, intellectual rigor, and a distraction-free environment.

The visual language follows a **Minimalist** philosophy with a focus on:
- **Intellectual Sophistication:** The pairing of high-contrast serifs with utilitarian sans-serifs creates a "modern classic" feel.
- **Atmospheric Depth:** A dark-mode first approach using deep, warm charcoals rather than pure blacks to maintain a soft, paper-like quality in a digital space.
- **Purposeful Color:** The terracotta primary color is used sparingly as a "highlighter," guiding the user toward action without overwhelming the content.
- **Crafted Precision:** Fine lines, subtle tonal shifts between containers, and generous negative space evoke a sense of quality and deliberate design.

## Colors

The palette is anchored in warm neutrals to prevent the "digital coldness" often found in dark themes.

- **Surface & Background:** The primary background uses `#121212`. Structural elements like sidebars and persistent panels use the slightly warmer, lifted `#1F1E1C` to create subtle environmental separation.
- **Primary (Terracotta):** Used for call-to-action buttons, active navigation states, and critical interactive indicators. It provides a warm, organic contrast to the dark surroundings.
- **Typography:** Primary text uses `#FDF8F5` (Cream), which reduces eye strain compared to pure white. Secondary text and metadata use a muted grey-beige (`#8E8C8A`) to maintain clear information hierarchy.
- **Accents:** Borders and dividers should be low-contrast, typically using a 10-15% opacity version of the primary text color to remain felt but not seen.

## Typography

The typographic system relies on a dual-axis approach:
- **The Editorial Axis (EB Garamond):** Used exclusively for high-level headings and narrative entry points. It should always be set with "Optical Sizing" enabled to preserve the delicate serifs.
- **The Functional Axis (Inter):** Used for all UI controls, body text, and data-heavy components. It provides a clean, neutral counterpoint to the expressive headlines.

**Usage Notes:**
- Avoid bold weights in EB Garamond; use scale and italics for emphasis instead.
- Use `label-sm` with slight letter spacing for category headers and timestamps to give them a "metadata" feel.
- Maintain a generous line height for body text to ensure long-form readability.

## Layout & Spacing

The layout is designed to prioritize focus, using a **Fixed-Fluid Hybrid** model.

- **Sidebar:** A fixed-width column (`280px`) on the left for navigation and history. It uses a distinct background color (`#1F1E1C`) to separate utility from content.
- **Content Area:** The main stage is centered with a maximum content width of `800px` for optimal reading line lengths. 
- **Grid:** A 12-column grid is used for complex layouts, but simpler views should rely on vertical stacking with consistent `24px` margins.
- **Responsive Behavior:** On tablet, the sidebar can collapse into an icon-only rail or a hidden drawer. On mobile, the content fills the screen width with `16px` horizontal margins, and headlines scale down to `headline-lg-mobile`.

## Elevation & Depth

This design system avoids heavy shadows, instead using **Tonal Layering** and **Fine Outlines** to communicate hierarchy.

- **Level 0 (Base):** The core background (`#121212`).
- **Level 1 (Structural):** Sidebars and persistent containers (`#1F1E1C`).
- **Level 2 (Interactive/Floating):** Input fields and hover states. These use a 1px solid border (`rgba(253, 248, 245, 0.1)`) to define their boundaries.
- **Focus States:** High-contrast terracotta borders or subtle glows are used to indicate active keyboard focus or primary interaction points.
- **Glassmorphism:** Reserved for top navigation bars or modal overlays, using a `12px` backdrop blur and a semi-transparent version of the surface color.

## Shapes

The shape language is "Soft" (`0.25rem` to `0.75rem`), balancing modern approachability with the structured feel of a professional tool.

- **Standard Elements:** Buttons and small input fields use a `0.5rem` (8px) radius.
- **Containers:** Large cards or sections use a `0.75rem` (12px) radius.
- **Specialty Elements:** Search bars and specific action "pills" may use a fully rounded (pill-shaped) radius to distinguish them as high-level entry points.

## Components

### Buttons
- **Primary:** Filled Terracotta (`#D95338`) with Cream text (`#FDF8F5`). Bold and clear.
- **Secondary:** Transparent with a thin cream border or a subtle tonal fill (`#1F1E1C`).
- **Ghost:** No background or border, using Primary or On-Surface-Variant text.

### Input Fields
Large, expansive containers for research prompts. They use a darker nested background or a subtle border. The cursor and focus rings should always adopt the Terracotta color.

### Chips & Tags
Small, low-profile containers used for suggested topics or filters. They feature a 1px border and use `label-md` typography.

### Lists (Sidebar)
Items are stacked with subtle vertical spacing. The active item is indicated by a vertical terracotta indicator or a slight background highlight, using a high-contrast text color.

### Cards
Used for research results or data summaries. They should have no shadow, relying on a 1px border (`#1F1E1C` or slight light-grey) to separate them from the main surface.