---
name: Core System
colors:
  surface: '#faf8ff'
  surface-dim: '#d8d9e6'
  surface-bright: '#faf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f3ff'
  surface-container: '#ededfa'
  surface-container-high: '#e7e7f4'
  surface-container-highest: '#e1e1ef'
  on-surface: '#191b24'
  on-surface-variant: '#424656'
  inverse-surface: '#2e303a'
  inverse-on-surface: '#eff0fd'
  outline: '#737688'
  outline-variant: '#c3c5d9'
  surface-tint: '#0051e1'
  primary: '#0047c8'
  on-primary: '#ffffff'
  primary-container: '#025cfd'
  on-primary-container: '#eaecff'
  inverse-primary: '#b5c4ff'
  secondary: '#505f76'
  on-secondary: '#ffffff'
  secondary-container: '#d0e1fb'
  on-secondary-container: '#54647a'
  tertiary: '#992d00'
  on-tertiary: '#ffffff'
  tertiary-container: '#c33b00'
  on-tertiary-container: '#ffe8e2'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dce1ff'
  primary-fixed-dim: '#b5c4ff'
  on-primary-fixed: '#00164d'
  on-primary-fixed-variant: '#003cad'
  secondary-fixed: '#d3e4fe'
  secondary-fixed-dim: '#b7c8e1'
  on-secondary-fixed: '#0b1c30'
  on-secondary-fixed-variant: '#38485d'
  tertiary-fixed: '#ffdbd0'
  tertiary-fixed-dim: '#ffb59e'
  on-tertiary-fixed: '#390b00'
  on-tertiary-fixed-variant: '#842500'
  background: '#faf8ff'
  on-background: '#191b24'
  surface-variant: '#e1e1ef'
typography:
  h1:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.02em
  h2:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  mono:
    fontFamily: monospace
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 20px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  container-padding: 24px
  element-gap: 16px
  sidebar-width: 260px
  gutter: 16px
---

## Brand & Style

This design system is engineered for backend-heavy environments where utility is paramount. It adopts a **Corporate / Modern** style characterized by extreme clarity, structural integrity, and a focus on information density. The goal is to reduce cognitive load for developers and operators by using a predictable, logical interface.

The aesthetic is "quiet"—it fades into the background to let the data speak. It relies on a rigorous grid, subtle borders, and a limited color palette to establish hierarchy. The emotional response is one of reliability, precision, and efficiency.

## Colors

The color palette is anchored by a professional "Electric Blue" primary color used for actions and indications of focus. The background uses a very light gray to reduce eye strain and differentiate the canvas from white surface containers (like cards or table rows).

- **Primary:** Used for primary buttons, active states, and progress indicators.
- **Secondary:** A neutral slate used for secondary actions and icon states.
- **Neutral/Background:** A scale of grays from white (surfaces) to deep slate (text) ensures high legibility and clear structural boundaries.
- **Status:** Use standard semantic colors (Red for error, Amber for warning, Green for success) but keep them desaturated to match the professional tone.

## Typography

The design system utilizes **Inter** for its exceptional legibility and systematic feel. The type scale is compact to support high data density.

- **Headlines:** Use semi-bold weights with slight negative letter spacing for a modern, "tucked-in" look.
- **Body Text:** The default size is 14px (body-md), which strikes the best balance for data-heavy dashboards.
- **Labels:** Small, uppercase labels are used for table headers and section titles to provide clear categorization without occupying much vertical space.
- **Monospace:** Use a standard monospace font for IDs, code snippets, and terminal outputs.

## Layout & Spacing

The layout follows a **Fluid Grid** model with fixed sidebar constraints. It is designed to maximize the visible area for data tables and logs.

- **Sidebar:** A fixed-width (260px) left-hand navigation ensures consistent access to top-level sections.
- **Grid:** Use a 12-column fluid grid for page content.
- **Rhythm:** All spacing is based on a 4px baseline unit. 16px is the standard gap between elements, while 24px is used for global container padding.
- **Density:** Provide "Compact" and "Comfortable" modes for tables, where the compact mode reduces vertical cell padding from 12px to 6px.

## Elevation & Depth

This system avoids heavy shadows and complex layering. Depth is communicated through **Tonal Layers** and **Low-contrast Outlines**.

- **Level 0 (Background):** The page background (#F8FAFC).
- **Level 1 (Surface):** White cards and containers (#FFFFFF) with a 1px solid border (#E2E8F0).
- **Level 2 (Interaction):** Subtle, small-blur shadows (0px 1px 2px rgba(0,0,0,0.05)) are only applied to floating elements like dropdowns, tooltips, or modals to separate them from the underlying surface.

## Shapes

The shape language is **Soft** and professional. A standard radius of 4px (0.25rem) is used for almost all UI components, including buttons, input fields, and cards. This provides a subtle modern feel while maintaining a structured, "boxy" layout that feels appropriate for a backend tool.

## Components

### Tables
The core component of the system. Use a white background, 1px horizontal borders, and no vertical borders. Table headers should be sticky with a light gray background (#F1F5F9) and uppercase labels.

### Buttons
- **Primary:** Solid blue (#025CFD) with white text.
- **Secondary:** White background with a slate border and slate text.
- **Tertiary/Ghost:** No background or border; blue text. Use for low-emphasis actions.

### Navigation Sidebar
A dark slate or very light gray sidebar with a clear vertical list. Active items should be indicated by a subtle background highlight and a 3px primary blue left border.

### Input Fields
Standardized height (36px or 40px). Use a 1px border (#E2E8F0) that turns primary blue on focus. Help text should be placed below the input in `body-sm`.

### Cards
Simple containers with a white background and a 1px border. Avoid using cards within cards; use simple dividers to separate internal content.

### Chips/Badges
Small, rounded rectangles used for status. Use a subtle tinted background (e.g., light green for "Success") with a darker version of the same color for the text to maintain contrast.