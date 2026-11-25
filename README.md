# AI Agent Skills

Reusable, project-agnostic skills for building high-craft software and editorial web interfaces.

## Available Skills

### Frontend & Design
- **[frontend-design](frontend/SKILL.md)** — Umbrella frontend design entry point combining layout philosophy, typography, color blocking, motion, and visual verification.
- **[editorial-design-system](frontend/editorial-design-system/SKILL.md)** — Complete editorial product design system: anti-slop subtraction rules, two-voice typography (poster vs. calm), semantic CSS token structure, colour-blocked sections, proportional pill bars, calm utility forms, resilient GSAP motion, and desktop/mobile visual QA.
  - [Tokens & Two-Voice Typography](frontend/editorial-design-system/references/tokens-and-typography.md)
  - [Layout Patterns & Component Architecture](frontend/editorial-design-system/references/layout-and-components.md)
  - [Motion & Scroll Architecture (GSAP)](frontend/editorial-design-system/references/motion-architecture.md)
- **[editorial-illustrations](frontend/editorial-illustrations/SKILL.md)** — 2022-era flat-editorial illustration workflow: discovering project CSS tokens, strict art-direction guardrails, dual-concept bake-off, seamless transparent PNG extraction ([extract_illustration.py](frontend/editorial-illustrations/scripts/extract_illustration.py)), and LCP-safe web integration.
- **[human-ui-copy](frontend/human-ui-copy/SKILL.md)** — Plain-English, jargon-free UI copy rules for headings, buttons, labels, and microcopy.

### Architecture
- **[clean-code](architecture/clean-code/SKILL.md)** — Enforces SOLID, DRY, KISS, and YAGNI principles with pre-commit quality checklists.

## Using in Another Project

Copy any self-contained skill folder (for example `frontend/editorial-design-system`, `frontend/editorial-illustrations`, or `frontend/human-ui-copy`) into your target repository's `.agents/skills/` directory, or link it globally in your agent skills directory.

For `editorial-illustrations`, Python 3 with Pillow (`pip install pillow`) is required to run `scripts/extract_illustration.py`.
