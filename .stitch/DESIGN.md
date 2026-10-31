---
name: CivicFlow
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#434655'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#737686'
  outline-variant: '#c3c6d7'
  surface-tint: '#0053db'
  primary: '#004ac6'
  on-primary: '#ffffff'
  primary-container: '#2563eb'
  on-primary-container: '#eeefff'
  inverse-primary: '#b4c5ff'
  secondary: '#565e74'
  on-secondary: '#ffffff'
  secondary-container: '#dae2fd'
  on-secondary-container: '#5c647a'
  tertiary: '#006243'
  on-tertiary: '#ffffff'
  tertiary-container: '#007d57'
  on-tertiary-container: '#bdffdc'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dbe1ff'
  primary-fixed-dim: '#b4c5ff'
  on-primary-fixed: '#00174b'
  on-primary-fixed-variant: '#003ea8'
  secondary-fixed: '#dae2fd'
  secondary-fixed-dim: '#bec6e0'
  on-secondary-fixed: '#131b2e'
  on-secondary-fixed-variant: '#3f465c'
  tertiary-fixed: '#85f8c4'
  tertiary-fixed-dim: '#68dba9'
  on-tertiary-fixed: '#002114'
  on-tertiary-fixed-variant: '#005137'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.025em
  headline-lg:
    fontFamily: Inter
    fontSize: 30px
    fontWeight: '600'
    lineHeight: 38px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Inter
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: -0.005em
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
    letterSpacing: 0em
  label-md:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.03em
  code-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-sm: 1rem
  margin: 2rem
  margin-sm: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
  space-2xl: 3rem
---

## Brand & Style

This design system blends institutional civic credibility with the efficiency and clarity of enterprise AI SaaS. It targets public sector administrators, civil servants, and civic constituents requiring reliable, clear operational oversight.

The visual style is **Corporate / Modern** anchored by structural discipline:
- High contrast, pristine white cards set against cool slate foundations.
- Strict visual hierarchy designed to lower cognitive strain in high-stakes public administration.
- Purposeful visual cues: solid informational stability in navigational chrome, paired with surgical precision in data visualization and AI inference readouts.
- Zero ornamental skeuomorphism or harsh dark-mode panels; every container prioritizes readability, accessibility, and institutional trust.

## Colors

The palette establishes an immediate institutional balance: high-authority deep slates for navigation, clinical blue-grey backdrops, authoritative royal blue for interactive focus, and precise semantic indicators for civil workflows.

- **Primary (`#2563eb`, `#1d4ed8`):** Royal Blue drives primary actions, selected navigation nodes, active focus borders, and interactive links.
- **Secondary (`#0f172a`, `#1e293b`):** Deep Navy/Slate is reserved exclusively for the persistent application frame, sidebar chrome, and deep modal headers to project stability and authority.
- **Tertiary / Success (`#059669`, `#0d9488`):** Emerald & Teal signal completed actions, resolved public cases, compliant statutes, and healthy automation states.
- **Warning / Progress (`#d97706`, `#f59e0b`):** Warm Amber denotes queued requests, administrative reviews, pending citizen disclosures, and in-flight AI processing.
- **Neutral Canvas (`#f8fafc`, `#f1f5f9`):** Ground level page canvas background providing gentle contrast beneath white foreground cards.
- **Border & Dividers (`#e2e8f0`):** Defines rigid surface edges, column borders, and card boundaries without introducing visual clutter.
- **Text & Foreground:** Primary text sits at `#0f172a` (Slate 900) for strict WCAG AAA compliance, supported by `#475569` (Slate 600) for descriptive metadata and `#94a3b8` (Slate 400) for structural iconography and disabled labels.

## Typography

The type system is powered entirely by **Inter**, leveraging its dense tabular figures, neutral grotesque structure, and exceptional legibility across dense data tables and administrative forms.

- **Scale Rationale:** Numerical line-heights correspond to an 8px baseline rhythm (16px, 20px, 24px, 28px, 32px, 44px).
- **Tracking:** Headlines utilize negative letter spacing (`-0.01em` to `-0.025em`) to compact civic titles and system headers, maintaining an editorial, high-end SaaS feel. Small metadata tags and status chips use slight positive tracking (`+0.01em` to `+0.03em`) for optical separation.
- **Numbers & Metrics:** Tabular figures (`tnum`) must be enforced across all analytics boards, processing tallies, and financial data grids.

## Layout & Spacing

The system implements a structured **Fluid Grid** anchored inside a standard administrative cockpit shell:
- **Navigation Shelf:** Fixed-width vertical sidebar (`260px` collapsed to `72px` on tablet viewports) on the left side of the screen using dark slate tones.
- **Canvas Body:** Fluid main area bound to a maximum viewport constraint of `1600px` for ultra-wide monitors, maintaining a consistent `2rem` (`32px`) screen margin.
- **Column System:** 12-column layout on desktop (`>= 1024px`) with `1.5rem` (`24px`) gutters; collapses to an 8-column layout on tablet (`768px - 1023px`), and a 4-column stack on mobile (`< 768px`) with `1rem` (`16px`) gutters.
- **Card-Internal Density:** Operational cards use `space-lg` (`24px`) internal padding by default, scaling down to `space-md` (`16px`) inside dense analytics tables and dynamic parameter inspectors.

## Elevation & Depth

Visual depth is achieved through **Tonal Surface Layering** combined with **Low-Contrast Outlines**, avoiding heavy drop shadows to keep government dashboards clean and glare-free.

- **Level 0 (Canvas Base):** Background canvas rendered in `#f8fafc`. Completely flat, non-elevated.
- **Level 1 (Default Containers & Cards):** Pure white (`#ffffff`) surfaces bounded by a crisp 1px stroke of `#e2e8f0`. Shadow is microscopic: `0 1px 2px 0 rgba(15, 23, 42, 0.04)`.
- **Level 2 (Hoverable Entities & Dropdowns):** Elevated surfaces receive `0 4px 6px -1px rgba(15, 23, 42, 0.07), 0 2px 4px -2px rgba(15, 23, 42, 0.05)`, encased with `#cbd5e1` to indicate interactive readiness.
- **Level 3 (Modals, Overlays, and Drawer Panels):** Floated directly over a tinted semi-transparent backdrop (`#0f172a` at 40% opacity). Elevation shadow: `0 20px 25px -5px rgba(15, 23, 42, 0.1), 0 8px 10px -6px rgba(15, 23, 42, 0.06)`.
- **AI Suggestion State:** Surfaces containing AI workflow predictions or citizen query analysis receive a subtle 1px border colored with `#93c5fd` (Blue 300) combined with an ultra-faint interior wash of `#f0fdf4` or `#eff6ff`. No intense glowing or particle effects.

## Shapes

The interface embraces a refined curved aesthetic, counterbalancing institutional rigidity with human-centered approachability:

- **Primary Cards & Containers:** Standardized at `16px` border-radius (`1rem` to `1.125rem` scale), creating softened modular enclosures.
- **Interactive Controls (Inputs, Buttons, Menus):** Standardized at `8px` (`0.5rem`) for crisp actionable intent and clean alignment next to table rows.
- **Badges, Status Indicators, and Pill Chips:** Full circular radius (`9999px`) to create clear distinct silhouette contrast against rectangular layout cards.
- **Micro UI (Checkboxes, Tooltips):** Scaled at `4px` to `6px` to maintain corner clarity at compact scales.

## Components

### Buttons
- **Primary:** Filled `#2563eb` with white text. Hover transitions to `#1d4ed8`. Focused with a 2px offset ring of `#93c5fd`. Border-radius: `8px`. Height: `40px` (standard), `32px` (compact table action).
- **Secondary / Outline:** White background with 1px border `#e2e8f0` and `#0f172a` text. Hover shifts background to `#f1f5f9` with border `#cbd5e1`.
- **Ghost:** Transparent background, `#475569` text. Hover shifts to `#f1f5f9`.
- **Destructive:** Subtle `#fef2f2` background with `#b91c1c` text and `#fecaca` border, escalating to solid red only on secondary confirmation.

### Badges & Status Chips
- Rendered in pill form (`rounded-full`) with a height of `24px`, padding `0 10px`, and `label-sm` typography:
  - **Success / Validated:** Background `#ecfdf5`, border `#a7f3d0`, text `#065f46`.
  - **In Progress / Pending:** Background `#fffbeb`, border `#fde68a`, text `#92400e`.
  - **Action Required / Escalation:** Background `#fef2f2`, border `#fecaca`, text `#991b1b`.
  - **AI Synthesized:** Background `#eff6ff`, border `#bfdbfe`, text `#1e40af`, with a small leading spark icon.

### Form Inputs & Selects
- Pure white background with a 1px border in `#e2e8f0`. Height `40px`, horizontal padding `12px`, radius `8px`.
- Placeholder text in `#94a3b8`.
- Focus state: border color `#2563eb`, plus an external glow ring: `0 0 0 3px rgba(37, 99, 235, 0.15)`.
- Input fields accompanied by explicit floating or top-aligned labels in `label-md` (`#334155`).

### Cards & Layout Panels
- Background `#ffffff`, border 1px solid `#e2e8f0`, border-radius `16px`.
- Card Headers contain a crisp bottom border divider in `#f1f5f9`, separating title and utility actions from the content block.
- Zero dark background variants within the main work canvas; all cards remain bright and legible.

### Tables & Data Grids
- Row height: `48px` default, `40px` dense.
- Table headers: Background `#f8fafc`, text `#475569` in `label-sm` uppercase, bottom border 1px `#e2e8f0`.
- Zebra striping is omitted; separation is maintained via subtle `#f1f5f9` row borders and `#f8fafc` row-hover states.

### AI Insight Callout Panel
- A civic-specific component used for automated statute lookups, constituent query summaries, or triage recommendations.
- Light blue-slate container (`#f8fafc`) featuring a left border accent of `3px solid #2563eb`.
- Header paired with an outline icon, an accuracy confidence pill badge (e.g., "98% Match"), and explicit "Approve" or "Modify" quick-action controls.