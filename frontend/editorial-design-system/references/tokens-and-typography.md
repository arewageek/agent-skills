# Design Tokens & Two-Voice Typography

Define a restrained palette of semantic CSS variables in your global stylesheet (`globals.css`) and forbid ad-hoc hex values inside feature stylesheets.

## 1. Palette Structure (3-Signal Discipline)

Choose one deep anchor, one bright brand accent, and at most one warm supporting signal, supported by off-white/stone surfaces and soft ink tones:

```css
:root {
  /* Surfaces */
  --bg-canvas: #fafbf9;          /* Warm off-white primary canvas */
  --bg-surface-subtle: #eff2ed;  /* Soft neutral tint for alternating bands & tool sections */
  --bg-surface-card: #ffffff;    /* Pure crisp surface for interactive cards & inputs */

  /* Brand signals (customize per project) */
  --color-anchor-deep: #0d1f17;        /* Deep ink/dark section canvas */
  --color-anchor-deep-subtle: #163024; /* Elevated dark card surface */
  --color-brand-accent: #8ce668;       /* Primary vibrant accent */
  --color-brand-accent-hover: #7cd957;
  --color-sun: #f2c14e;                /* Optional secondary warm signal */

  /* Ink (never harsh pure #000000) */
  --ink-primary: #0e1411;
  --ink-secondary: #434c47;
  --ink-muted: #66706a;
  --ink-on-deep: #fafbf9;
  --ink-on-deep-muted: #b6c2bc;

  /* Lines */
  --border-subtle: #dce2d9;

  /* Shape & Motion */
  --radius-md: 16px;
  --radius-lg: 24px;
  --radius-xl: 32px;
  --radius-pill: 9999px;
  --ease-spring: cubic-bezier(0.22, 1, 0.36, 1);
  --duration-fast: 160ms;
}
```

### Contrast & Semantic Color Rules

- **Strict ink pairing**: Bright brand accent fills (like mint or lime buttons/bars) must carry deep anchor ink (`--color-anchor-deep`), never white text.
- **Consistent color meaning**: Assign each brand tone a consistent semantic role across the whole app (e.g., bright accent = active/primary flow, deep anchor = locked/serious/protected, warm signal = future/goal/highlight).
- **Accessible focus**: Provide an unmistakable `:focus-visible` ring (`3px solid var(--color-brand-accent); outline-offset: 2px;`).

## 2. Two-Voice Typography

Pair a clean geometric sans-serif for UI/body copy with a condensed display variable/grotesque typeface for poster headlines and numerals.

```css
body {
  background-color: var(--bg-canvas);
  color: var(--ink-primary);
  font-family: var(--font-sans), system-ui, sans-serif;
  font-feature-settings: "tnum" 1; /* Tabular figures everywhere */
  line-height: 1.5;
  overflow-x: clip;
}

/* Voice 1: Poster — short, loud, stacked 3-6 word punchlines */
.display {
  font-family: var(--font-display), sans-serif;
  font-weight: 800;
  font-stretch: 75%;
  text-transform: uppercase;
  line-height: 0.88;
  letter-spacing: -0.01em;
}

/* Same display face for big figures, never uppercased */
.numeral {
  font-family: var(--font-display), sans-serif;
  font-weight: 800;
  font-stretch: 75%;
  line-height: 1;
}

/* Voice 2: Calm — sentence-case section headings */
.heading {
  font-size: clamp(2.25rem, 4vw, 3.5rem);
  font-weight: 700;
  line-height: 1.02;
  letter-spacing: -0.03em;
}
```

### Typography Rules

- **Reserve `.display` for moments of punch.** If every heading screams in condensed uppercase, nothing stands out. Use `.heading` for explanatory sections, forms, and tools.
- **Keep tabular numerals (`tnum`) active** on `body` so animated counters, calculators, and comparison bars never jitter horizontally as digits change.

## 3. Shared Base Primitives

Keep global utility classes minimal and tactile:

```css
.container {
  inline-size: min(1240px, 100% - 3rem);
  margin-inline: auto;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.85rem 1.6rem;
  border-radius: var(--radius-pill);
  border: none;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition:
    transform var(--duration-fast) var(--ease-spring),
    background-color var(--duration-fast) var(--ease-spring);
}

.btn:hover { transform: scale(1.03); }
.btn:active { transform: scale(0.97); }

.btnPrimary {
  background-color: var(--color-brand-accent);
  color: var(--color-anchor-deep);
}

.btnDeep {
  background-color: var(--color-anchor-deep);
  color: var(--color-brand-accent);
}

.circle {
  display: grid;
  place-items: center;
  inline-size: 48px;
  block-size: 48px;
  border-radius: 50%;
  background-color: var(--bg-surface-subtle);
  color: var(--ink-primary);
}

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .btn { transition: none; }
}
```
