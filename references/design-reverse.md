# Module C: Design System Reverse Engineering

## Problem

Stage 4 UI Design creates Design Tokens from scratch. But often users want to **match an existing product's design style** rather than design something new. How do we extract design tokens from existing products or DESIGN.md files?

## Source: awesome-design-md (90K stars)

[VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) is a curated collection of DESIGN.md files from popular products. Each file contains the complete design system specification used by that product's coding agents to match its visual identity.

## Reverse Engineering Process

### Input: Any existing product/design reference

```
User: "I want my app to look like Linear.app" or "Here's a screenshot of a dashboard I like"
```

### Step 1: Extract Visual Properties

From screenshot or reference, identify:

| Category | What to Extract | Tool Method |
|----------|---------------|-------------|
| Colors | Primary, secondary, background, text, border colors | Eyedropper or color picker |
| Typography | Font family, sizes (h1-h6, body, small), weights, line heights | Inspect element or estimate |
| Spacing | Base unit, padding scale, margin rhythm | Measure relative proportions |
| Border radius | Scale (none/small/medium/large/full) | Visual inspection |
| Shadows | Elevation levels (0-4 typically) | Observe depth layers |
| Icons | Style (outline/filled), size, stroke width | Visual classification |
| Motion (optional) | Transition duration, easing curve | If animated reference available |

### Step 2: Map to Design Token Structure

```css
/* Extracted from reference: Linear.app-inspired light theme */
:root {
  /* === Colors === */
  --color-bg-primary: #FAFAFA;
  --color-bg-secondary: #FFFFFF;
  --color-bg-tertiary: #F7F7F8;
  --color-text-primary: #0D0D0D;
  --color-text-secondary: #6B6B6B;
  --color-text-tertiary: #9F9F9F;
  --color-accent: #5E6AD2;        /* Indigo/purple primary */
  --color-accent-hover: #4E5AC2;
  --color-success: #17BF53;
  --color-warning: #F5AB00;
  --color-danger: #E03131;
  --color-info: #228BE6;

  /* === Typography === */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  /* Text Scale (Major Second: 1.250) */
  --text-xs: 11px;
  --text-sm: 12px;
  --text-base: 14px;     /* body default */
  --text-lg: 16px;
  --text-xl: 18px;
  --text-2xl: 20px;
  --text-3xl: 24px;

  /* === Spacing (4px base unit) */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;

  /* === Borders === */
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;
  --radius-xl: 12px;
  --radius-full: 9999px;

  /* === Shadows (Elevation) */
  --shadow-xs: 0 1px 2px rgba(0,0,0,0.04);
  --shadow-sm: 0 2px 4px rgba(0,0,0,0.06);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
  --shadow-lg: 0 8px 24px rgba(0,0,0,0.10);
}
```

### Step 3: Create Component Mapping

Map the extracted tokens to actual components you'll build:

| Reference Component | Your Equivalent | Key Tokens Used |
|--------------------|---------------|-----------------|
| Sidebar nav | `.sidebar-nav` | `--color-bg-secondary`, `--radius-lg`, `--shadow-sm` |
| Card container | `.card` | `--color-bg-primary`, `--radius-md`, `--shadow-xs` |
| Primary button | `.btn-primary` | `--color-accent`, `--text-sm`, `--font-sans` |
| Input field | `.input` | `--border-color`, `--radius-md`, `--text-base` |
| Table row | `.table-row` | `--color-bg-tertiary` on hover |
| Badge/tag | `.badge` | `--radius-full`, `--text-xs`, padding token |

### Step 4: Validate Fidelity

After implementing with reversed tokens:

```
Fidelity Score = (Matched Tokens / Total Reference Tokens) x 100

Target: >=85% for "clearly inspired by" recognition
Target: >=95% for "could pass as same design system" recognition
```

## Integration with Stage 4

Add alternative path to Stage 4:

```
Standard Path (existing):
  User describes desired look -> Designer + AI create tokens from scratch

NEW Reverse Path (this module):
  User provides reference (screenshot/product name/url) ->
    Extract visual properties ->
    Map to Design Token structure ->
    Component mapping ->
    Output same Design Token document as standard path
```

Both paths produce identical output format (`docs/04-ui-design.md`), so downstream stages (5-7) are unaffected.

## Quick Reference: Pre-Extracted Style Templates

For common design styles, use these starting points:

| Style | Characteristic | Primary Color | Vibe |
|-------|---------------|---------------|------|
| **Linear-style** | Clean, minimal, indigo accent | `#5E6AD2` | Professional SaaS |
| **Notion-style** | Warm gray, structured, subtle | `#2383E2` | Knowledge work |
| **Stripe-style** | Bold, colorful, high contrast | `#635BFF` | Fintech/modern |
| **Vercel-style** | Black & white, geometric | `#000000` | Developer-focused |
| **Apple-style** | Generous whitespace, SF Pro | `#007AFF` | Premium consumer |
| **Discord-style** | Dark-first, blurred surfaces | `#5865F2` | Community/chat |

Each can be provided as a starting point that users customize.

## See Also

- [advanced-qa.md](advanced-qa.md) — Module A: Meta-Mentor CPI
- [rule-pack.md](rule-pack.md) — Module B: Rule Package Version Management
