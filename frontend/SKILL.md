---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill for UI tasks that build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

# Frontend Design

Use this skill to design and implement bold, production-ready frontends when the request involves UI. Combine it with repository UI/UX requirements, existing design tokens, and the specialized frontend modules in this directory:

- **[editorial-design-system](editorial-design-system/SKILL.md)** — Anti-slop subtraction, two-voice typography (poster vs. calm), colour-blocked sections, proportional pill bars, calm utility forms, resilient GSAP motion, and desktop/mobile visual QA.
- **[editorial-illustrations](editorial-illustrations/SKILL.md)** — 2022-era flat-editorial illustration workflow: palette-locked art direction, dual-concept bake-off, seamless transparent PNG extraction, and LCP-safe web integration.
- **[human-ui-copy](human-ui-copy/SKILL.md)** — Plain-English, jargon-free labels, headings, and microcopy.

## Design Thinking

Before coding, lock in a clear, memorable direction:
- **Purpose**: What problem does the interface solve, and what single interactive tool or action should carry the page?
- **Tone**: Commit to a strong aesthetic (e.g., editorial product, brutalist/raw, luxury/refined, industrial/utilitarian). Avoid timid mixes.
- **Constraints**: Framework (Server Components first, `"use client"` only on interactive leaves), performance, accessibility, reduced motion.
- **Subtraction**: Strip eyebrow pills, glowing dots, badge soup, and repetitive bordered card grids before adding polish.

## Frontend Aesthetics Guidelines

- **Typography**: Pick characterful, non-default fonts; pair a distinctive display voice (with tabular numerals) for punchlines and figures with a calm, legible sans-serif for explanatory sections and UI.
- **Color & Theme**: Lock to a tight set of semantic CSS variables (surface, subtle tint, deep anchor, 1–2 brand signals). Alternate full-bleed canvases rather than boxing everything into gray-bordered cards.
- **Motion**: Use purposeful animations (scroll-triggered data reveals, scrubbed rails, live interactive state) animating only `transform`, `opacity`, and `clip-path`. Always respect `prefers-reduced-motion` and keep JS-off server HTML intact.
- **Illustrations & Visuals**: Use palette-locked bespoke editorial spots floating seamlessly on the canvas—never hand-coded multi-object SVG scenes or glossy 3D stock graphics.
- **Verify Visually**: Build, serve, screenshot desktop (`1440px`) and mobile (`390px`), and inspect the rendered UI directly before calling the task done.
