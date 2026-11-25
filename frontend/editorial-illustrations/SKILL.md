---
name: editorial-illustrations
description: >-
  Art-directs, generates, extracts, and integrates authentic 2022-era flat-editorial
  product illustrations tailored to the active project's exact brand palette and visual
  identity. Activate whenever adding or replacing a hero illustration, section artwork,
  onboarding graphic, empty-state illustration, or email spot asset — never hand-code
  vibecoded SVG scenes or drop generic glossy 3D AI stock graphics.
---

# Editorial Illustrations (2022 Craft Protocol)

Produce natural, timeless, art-directed product illustrations in the peak 2021–2022 editorial style (Wise, Notion, Intercom, Monzo, Stripe Press, New Yorker spot art) that blend effortlessly into the product canvas. Never hand-code complex multi-object SVG scenes from scratch and never settle for generic glossy 3D AI art or Corporate Memphis clichés.

## 1. Discover the Project Palette First (Zero Assumptions)

Before writing any image brief, inspect the repository's actual design tokens and brand files (e.g., `globals.css`, theme config, design-system skill, existing brand assets) to extract:

- **Canvas background** where the illustration will sit (e.g., `#FAFBF9`, `#FFFFFF`, `#0D1F17`)
- **Primary ink color** for outlines and deep contrast (never harsh pure `#000000` unless the brand explicitly uses pure black)
- **Hero brand accent** (1 primary highlight color)
- **Secondary warm/supporting accent** (1 accent max, if the brand has one)
- **Neutral surface tint(s)** for grounding objects and subtle fills

Lock the art brief strictly to those 3–5 project tones. Explicitly forbid stray unbranded hues.

## 2. The 2022 Editorial Art-Direction Formula

Every prompt sent to the `image-generator` subagent must specify:

- **Style anchor**: Authentic 2021–2022 modern editorial ink-and-flat-color spot illustration. Confident uniform ink outlines in the project's deep ink color, matte flat color blocking, subtle organic risograph/print paper grain, open airy negative space.
- **Visual storytelling over literal UI**: Express the feature's *core mental model* through a witty, immediately readable object/rhythm metaphor or calm human scene (e.g., uneven coins funneling into calm evenly-spaced calendar paydays) — never draw fake software dashboards, floating neon glass cards, or generic people pointing at charts.
- **Seamless floating vignette**: Specify a pure flat solid background matching the target canvas with generous clean margin on all four edges so extraction leaves zero cut-off lines.
- **Strict negative guardrails (mandatory in every brief)**:
  - **ZERO text, letters, numbers, or currency symbols** anywhere inside the artwork (use clean geometric calendar grids, dots, checkmarks, stripes, and silhouettes instead — never risk garbled AI typography).
  - **ZERO** 3D rendering, glossy plastic specular highlights, soft airbrush gradients, neon glows, or photorealism.
  - **ZERO** rectangular border, card frame, vignette box, or drop shadow around the artwork.
  - **ZERO** bloated/distorted Corporate Memphis proportions when depicting people (keep natural, tasteful, human proportions).

## 3. Dual-Concept Generation & Selection

1. Invoke **two** `image-generator` subagents in parallel with distinct conceptual angles (for example: one witty conceptual object/still-life metaphor and one calm human-led editorial scene, or two distinct visual metaphors) locked to the exact same palette and line-weight spec.
2. Inspect **both** generated outputs directly using `read_file` (alongside any existing project benchmark illustration to verify family consistency).
3. Judge ruthlessly on: instant conceptual clarity (< 1 second read), authentic hand-inked 2022 print character, strict palette adherence, zero garbled text/artifacts, and clean closed outer silhouettes.
4. Pick the strongest candidate — or iterate once with targeted refinements if neither hits studio quality. Never ship the first mediocre output.

## 4. Seamless Transparent Extraction & Tight Cropping

Raw generated JPEGs almost always have a background shade 2–6 RGB points off from the page canvas, creating an amateur faint box seam on high-DPI displays, plus excessive empty border padding.

Run the bundled extractor script [extract_illustration.py](./scripts/extract_illustration.py) (requires Python 3 + Pillow):

```bash
python3 .agents/skills/editorial-illustrations/scripts/extract_illustration.py \
  <source-image> \
  <destination-png> \
  --pad 24
```

*(Adjust the script path if running directly from your shared skills directory.)*

What it does:
- Automatically samples the outer corner background color and runs a **perimeter-only BFS flood-fill** from the image edges (preserving enclosed light interiors inside calendars, envelopes, cups, clothing, etc.).
- Runs 2-pass anti-aliased fringe softening along edges adjacent to transparency so ink outlines blend cleanly without a gray/white halo.
- Crops tightly to the artwork bounding box plus `--pad` pixels and prints JSON metadata including exact final `width` and `height`.

**Mandatory check:** Open the extracted PNG with `read_file` immediately after running the script to confirm:
- Zero background leaks into enclosed light shapes.
- Zero visible fringe halos or clipped artwork edges.

If an open outline caused an interior leak, reduce `--tolerance` (e.g., `--tolerance 16`) and re-run.

## 5. Production Web Integration & Verification

- Save final assets in the project's public illustrations directory (e.g., `public/illustrations/<short-atomic-name>.png`).
- Always render with explicit `width` and `height` matching the script's reported output dimensions (zero CLS) and accurate responsive `sizes`.
- **Loading priority** (follow modern web LCP best practices):
  - **Above-the-fold hero illustration**: set `fetchPriority="high"` (and `priority` in Next.js `Image`); never set `loading="lazy"`.
  - **Below-the-fold section / empty-state illustration**: omit `fetchPriority` and allow standard lazy loading.
- Float the illustration directly on the section surface with zero wrapper border or card box unless the design intentionally frames it.
- Keep it grounded and editorial — avoid cheesy perpetual bounce/float animations.
- Build, serve, screenshot both desktop (`1440px`) and mobile (`390px`), and visually inspect with `read_file` to verify seamless background blending, crisp scaling, and balanced proportion beside surrounding copy.
