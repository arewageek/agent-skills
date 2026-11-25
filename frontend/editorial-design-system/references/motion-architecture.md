# Motion & Scroll Architecture (GSAP)

Motion must explain data or reward direct interaction—bars growing to their real proportion, figures counting up, an interactive tool revealing on scroll, or a card rail tracking vertical scroll. Motion never decorates for its own sake; hero illustrations stay calm and grounded.

## 1. Core Principles

- **Animate compositor properties only**: Restrict animations to `transform`, `opacity`, and `clip-path`. Never animate `width`, `height`, `top`, or `left`.
- **Keep GSAP out of the initial JS bundle**: Dynamically import GSAP inside a reusable hook (`useMotion`) used only by `"use client"` leaf components.
- **No-JS & Reduced-Motion resilience**: Server-rendered HTML must already contain the final readable values and full layout. Under `prefers-reduced-motion: reduce`, skip all tweens and pins and render the final state immediately.
- **Clean lifecycle management**: Run every setup inside `gsap.matchMedia()` and return its cleanup so React Strict Mode and route transitions revert cleanly.

## 2. Dynamic `useMotion` Hook & `motion.ts` Helper

### `use-motion.ts`

```ts
import { useEffect, useRef } from "react";

export type Motion = typeof import("./motion");

export function useMotion<T extends HTMLElement>(
  query: string,
  setup: (motion: Motion, root: T) => void | (() => void),
) {
  const ref = useRef<T>(null);

  useEffect(() => {
    const root = ref.current;
    if (!root) return;

    let live = true;
    let stop: (() => void) | undefined;

    import("./motion").then((motion) => {
      if (!live) return;
      const media = motion.gsap.matchMedia();
      media.add(query, () => setup(motion, root));
      stop = () => media.revert();
    });

    return () => {
      live = false;
      stop?.();
    };
  }, [query, setup]);

  return ref;
}
```

### `motion.ts` (Centralized GSAP Registration & Primitives)

```ts
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);
// Prevent mobile browser address-bar show/hide from triggering pin jitter
ScrollTrigger.config({ ignoreMobileResize: true });

export { gsap, ScrollTrigger };

const EMPTY = "inset(0% 100% 0% 0% round 9999px)";
const FULL = "inset(0% 0% 0% 0% round 9999px)";

export function countTo(
  el: HTMLElement,
  to: number,
  duration: number,
  format: (n: number) => string,
) {
  const state = { value: 0 };
  el.textContent = format(0);
  return gsap.to(state, {
    value: to,
    duration,
    ease: "power3.out",
    onUpdate: () => {
      el.textContent = format(state.value);
    },
  });
}

export function growBars(
  timeline: gsap.core.Timeline,
  bars: HTMLElement[],
  at: number,
  step: number,
  format: (n: number) => string,
) {
  bars.forEach((bar, index) => {
    const start = at + index * step;
    timeline.fromTo(
      bar,
      { clipPath: EMPTY },
      { clipPath: FULL, duration: 0.9, ease: "power3.out" },
      start,
    );
    const figure = bar.querySelector<HTMLElement>("[data-count]");
    if (figure) {
      timeline.add(
        countTo(figure, Number(figure.dataset.count), 0.9, format),
        start,
      );
    }
  });
}
```

Notice how `growBars` animates `clip-path: inset(...)` instead of `width`: layout geometry stays locked at the final width from frame zero, preventing reflow and keeping the pill radius crisp throughout the reveal.

## 3. Scroll-Pinned Horizontal Card Rail

When pinning a horizontal card track to vertical scroll:

- Run at all viewport widths inside `"(prefers-reduced-motion: no-preference)"`.
- Dynamically choose `start`: `"top top"` if the section is taller than `window.innerHeight`, otherwise `"center center"` so shorter sections stay centered while pinned.
- Observe layout/font shifts with `ResizeObserver` and `document.fonts?.ready` to call `ScrollTrigger.refresh()`, and reset `rail.scrollLeft = 0` on refresh.

```ts
function pinRail({ gsap, ScrollTrigger }: Motion, rail: HTMLElement) {
  const track = rail.querySelector<HTMLElement>("[data-track]");
  const section = rail.closest("section");
  if (!track || !section) return;

  const distance = () => {
    const last = track.lastElementChild as HTMLElement | null;
    if (!last || rail.clientWidth === 0) return 0;
    return Math.max(0, last.offsetLeft + last.offsetWidth - rail.clientWidth);
  };

  rail.scrollLeft = 0;
  rail.setAttribute("data-pinned", "");

  const tween = gsap.to(track, {
    x: () => -distance(),
    ease: "none",
    scrollTrigger: {
      trigger: section,
      start: () =>
        section.offsetHeight > window.innerHeight ? "top top" : "center center",
      end: () => `+=${Math.max(1, distance())}`,
      pin: true,
      scrub: true,
      anticipatePin: 1,
      invalidateOnRefresh: true,
      onRefresh: () => {
        rail.scrollLeft = 0;
      },
    },
  });

  const observer = new ResizeObserver(() => {
    if (tween.scrollTrigger) ScrollTrigger.refresh();
  });
  observer.observe(rail);
  observer.observe(track);

  let active = true;
  document.fonts?.ready.then(() => {
    if (active) ScrollTrigger.refresh();
  });

  return () => {
    active = false;
    observer.disconnect();
    rail.removeAttribute("data-pinned");
  };
}
```
