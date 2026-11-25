---
name: editorial-design-system
description: >-
  Guides UI/UX architecture, visual design philosophy, typography voices,
  colour-blocked layouts, calm forms, purposeful motion, and visual QA for
  modern editorial web products. Activate before designing, building, styling,
  or modifying any landing page, product page, interactive tool, or CSS.
---

# Editorial Design System

Say little, say it loud, and let one real interactive tool or clear action carry the page. High-craft product interfaces come from disciplined subtraction, crisp typographic contrast, bold full-bleed colour blocking, and empirical visual verification—never from generic SaaS templates.

## Core Design Rules

1. **No eyebrow pills, glowing dots, or badge soup.** Headlines stand naked. Never stamp a status pill, category chip, or pulsing dot above a heading or in a card corner.
2. **Two typographic voices only.**
   - *Poster* (`.display`): Condensed, heavy (`800`), uppercase, tight leading (`~0.88`) strictly for short 3–6 word punchlines. Numbers use `.numeral` (same display face, tabular figures, never uppercased).
   - *Calm* (`.heading`): Sentence-case (`700`) for explanatory sections and product sections. Do not make every section shout.
3. **Subtract ruthlessly in the hero.** A hero holds a headline, one concise sentence (max ~36–38ch), one primary button, and optional unframed artwork. Zero quote callouts, zero stat bars, zero secondary competing buttons.
4. **Let one real tool carry the page.** Put an interactive calculator, estimator, or live preview in its own dedicated full-bleed tinted section with clear edit affordances and immediate visual feedback—not buried inside a heavy dark roof slab or boxed icon grid.
5. **No boxes around simple groups.** Three-item step or benefit groups sit as borderless columns directly on the canvas: circle icon, bold title, 2-line caption.
6. **Colour blocking over card grids.** Alternate full-bleed section canvases (e.g., light canvas, subtle neutral tint, bright brand accent, deep anchor). Use solid-fill cards instead of repetitive white cards with gray borders.
7. **Show comparisons as proportional pill bars.** Render widths proportional to actual values with the figure inside the bar—never as three paragraphs inside three identical cards.
8. **Calm utility forms, not miniature heroes.** Standalone form pages (`/login`, `/signup`, `/reset`, `/waitlist`) sit on the main light canvas under a minimal hairline top bar, with a calm sentence-case `<h1>`, crisp inputs, and one full-width primary CTA. Never top forms with a heavy dark hero slab or uppercase `.display` banner.
9. **Honest numbers and plain English.** Every example figure on the page must mathematically follow from the stated rule. Use conversational plain English (pair with [human-ui-copy](../human-ui-copy/SKILL.md)).

## Reference Guides

- **Tokens, Surfaces & Typography**: [references/tokens-and-typography.md](references/tokens-and-typography.md)
- **Layout Patterns & Components**: [references/layout-and-components.md](references/layout-and-components.md)
- **Motion & Scroll Architecture (GSAP)**: [references/motion-architecture.md](references/motion-architecture.md)

## Illustrations

For hero artwork, section spots, empty states, onboarding visuals, or email graphics, use [editorial-illustrations](../editorial-illustrations/SKILL.md). Never hand-code complex multi-object SVG scenes or drop glossy 3D AI stock graphics.

## Code Architecture Rules

- **Co-located styles**: Keep feature components paired with co-located stylesheets (e.g., `components/<name>.tsx` + `<name>.module.css`) instead of a single giant stylesheet. Keep only design tokens and shared primitives (`.container`, `.display`, `.numeral`, `.heading`, `.btn`, `.circle`) in `globals.css`.
- **Server-first components**: Keep pages and layout sections as Server Components by default. Push `"use client"` down to the smallest interactive leaf (calculator, animated chart, scroll rail).

## Mandatory Visual Verification

Typechecks and builds do not prove a design works. Before calling any UI work complete:

1. Build and serve the production app.
2. Capture screenshots at **desktop (`1440px`)** and **mobile (`390px`)** viewports.
3. Inspect the rendered screenshots directly (e.g., via `read_file`) to verify hierarchy, contrast, spacing, alignment, illustration blending, and zero horizontal overflow.
