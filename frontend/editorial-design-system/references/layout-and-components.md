# Layout Patterns & Component Architecture

Build pages out of high-contrast visual rhythm rather than repetitive card grids.

## 1. Full-Bleed Canvas Alternation

Structure landing and marketing pages as an intentional cadence of full-bleed background canvases so sections separate naturally without heavy borders:

1. **Header** — Minimal top bar on `--bg-canvas`
2. **Hero** (`--bg-canvas`) — Poster headline, short lead (~36–38ch), 1 CTA, and an unframed editorial illustration
3. **Steps / How It Works** (`--bg-canvas`) — 3 borderless columns (`.circle` icon, bold title, 2-line caption)
4. **Interactive Tool** (`--bg-surface-subtle`) — Calm heading + concise bullet points alongside one focused, interactive white card (~440px) with preset pills, inline editable controls, live slider, and a compact deep payoff strip at the bottom
5. **Visual Comparison** (`--color-brand-accent`) — Proportional pill bars inside one crisp container showing the before/after delta
6. **Multi-Lane / Feature Showcase** (`--bg-canvas`) — Stacked solid-fill pills + 3 borderless columns
7. **Horizontal Story Rail** (`--bg-surface-subtle`) — Solid-fill cards (accent, deep, warm signal) in a scrubbed horizontal scroll track
8. **Cost / Math Breakdown** (`--color-anchor-deep`) — Dark canvas with proportional pill bars and clear summary totals
9. **Closing CTA** (`--color-brand-accent`) — Centered white panel with one clear call to action
10. **Footer**

## 2. Proportional Pill Bars (Instead of Text Cards)

When comparing quantities, timelines, or before/after outcomes, show the math directly using horizontal pill bars whose width is driven by a CSS custom property (`--w`):

```tsx
function barWidth(amount: number, widest: number): CSSProperties {
  return { "--w": `${(amount / widest) * 100}%` } as CSSProperties;
}
```

```css
.bar {
  inline-size: var(--w);
  min-inline-size: max-content;
  padding: 0.36rem 0.9rem;
  border-radius: var(--radius-pill);
  background-color: var(--bg-surface-subtle);
  font-size: 0.925rem;
  font-weight: 700;
  text-align: right;
}
```

- Place the numeric figure **inside** the bar (`text-align: right`).
- Pair a muted neutral bar for the baseline ("Before / On your own") with a vibrant accent bar for the product state.
- Ensure `min-inline-size: max-content` so small or zero-value labels stay readable inside their pill.

## 3. Borderless Feature Columns

Avoid putting 3 bordered cards around simple 3-step explanations. Sit them directly on the page:

```css
.columns {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 2.5rem;
}

@media (max-width: 820px) {
  .columns {
    grid-template-columns: 1fr;
    gap: 1.75rem;
  }
}
```

Each item contains only:
- `.circle` icon badge
- Short bold title
- 1–2 line plain-English caption

## 4. Calm Utility & Form Pages

Never wrap authentication, onboarding, or waitlist forms in miniature dark hero banners or shouting `.display` typography. Utility pages must feel calm, focused, and trustworthy:

- Background: `--bg-canvas`
- Header: minimal top bar with a `1px solid var(--border-subtle)` bottom hairline
- Heading: calm sentence-case `<h1>`
- Inputs: crisp `--bg-surface-card` (`#ffffff`) with `--border-subtle` borders and generous padding
- Submit action: one full-width primary pill button (`.btn.btnPrimary`)
- Optional spot illustration: unframed 2022 editorial spot sitting cleanly beside or above the form on `--bg-canvas`

## 5. Honest Numbers & Copy Discipline

- **Verify every example figure**: If a section states "1,500,000 across 3 months", every derived allowance, monthly bar, and fee figure on the page must calculate cleanly from that rule.
- **Avoid AI template artifacts**: Never add fake testimonial carousels, glowing "Live" status dots, eyebrow pills (`NEW FEATURE`), or floating glassmorphism stats over hero artwork.
