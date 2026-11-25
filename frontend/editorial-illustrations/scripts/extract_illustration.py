#!/usr/bin/env python3
"""Extract a generated editorial illustration onto a seamless transparent PNG.

Uses perimeter-only BFS flood-fill anchored to the sampled corner background so
enclosed light interiors (calendar pages, envelopes, cups, clothing) remain intact,
followed by gentle anti-aliased edge softening and tight padding-aware cropping.
"""

from __future__ import annotations

import argparse
import json
import os
from collections import deque
from statistics import median
from PIL import Image


def sample_corner_bg(im: Image.Image) -> tuple[int, int, int]:
    w, h = im.size
    inset_x = min(4, max(0, w // 40))
    inset_y = min(4, max(0, h // 40))
    pts = [
        (inset_x, inset_y),
        (w - 1 - inset_x, inset_y),
        (inset_x, h - 1 - inset_y),
        (w - 1 - inset_x, h - 1 - inset_y),
    ]
    samples = [im.getpixel(pt)[:3] for pt in pts]
    return (
        int(median(s[0] for s in samples)),
        int(median(s[1] for s in samples)),
        int(median(s[2] for s in samples)),
    )


def channel_dist(rgb: tuple[int, int, int], bg: tuple[int, int, int]) -> int:
    return max(abs(rgb[0] - bg[0]), abs(rgb[1] - bg[1]), abs(rgb[2] - bg[2]))


def extract(
    src: str,
    dst: str,
    tolerance: int = 24,
    fringe_passes: int = 2,
    pad: int = 24,
    max_width: int | None = None,
) -> dict[str, object]:
    im = Image.open(src).convert("RGBA")
    orig_size = im.size
    w, h = orig_size
    bg = sample_corner_bg(im)
    px = im.load()

    visited = bytearray(w * h)
    queue: deque[tuple[int, int]] = deque()

    def try_seed(x: int, y: int) -> None:
        idx = y * w + x
        if visited[idx]:
            return
        r, g, b, _ = px[x, y]
        if channel_dist((r, g, b), bg) <= tolerance:
            visited[idx] = 1
            queue.append((x, y))

    for x in range(w):
        try_seed(x, 0)
        try_seed(x, h - 1)
    for y in range(h):
        try_seed(0, y)
        try_seed(w - 1, y)

    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < w and 0 <= ny < h:
                idx = ny * w + nx
                if not visited[idx]:
                    r, g, b, _ = px[nx, ny]
                    if channel_dist((r, g, b), bg) <= tolerance:
                        visited[idx] = 1
                        queue.append((nx, ny))

    for y in range(h):
        row = y * w
        for x in range(w):
            if visited[row + x]:
                px[x, y] = (bg[0], bg[1], bg[2], 0)

    fringe_limit = max(tolerance + 16, int(tolerance * 2.2))
    span = max(1, fringe_limit - tolerance)
    for _ in range(max(0, fringe_passes)):
        updates: list[tuple[int, int, tuple[int, int, int, int]]] = []
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                r, g, b, a = px[x, y]
                if a == 0:
                    continue
                if any(
                    px[nx, ny][3] == 0
                    for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
                ):
                    dist = channel_dist((r, g, b), bg)
                    if dist < fringe_limit:
                        ratio = max(0.0, min(1.0, (dist - tolerance * 0.65) / span))
                        new_a = int(round(ratio * 255))
                        updates.append((x, y, (r, g, b, min(a, new_a))))
        for x, y, rgba in updates:
            px[x, y] = rgba

    bbox = im.getbbox()
    if bbox is None:
        raise RuntimeError(
            "All pixels became transparent; lower --tolerance and retry."
        )

    crop_box = (
        max(0, bbox[0] - pad),
        max(0, bbox[1] - pad),
        min(w, bbox[2] + pad),
        min(h, bbox[3] + pad),
    )
    out = im.crop(crop_box)

    if max_width and out.width > max_width:
        scale = max_width / out.width
        out = out.resize(
            (max_width, max(1, int(round(out.height * scale)))),
            Image.Resampling.LANCZOS,
        )

    parent = os.path.dirname(os.path.abspath(dst))
    if parent:
        os.makedirs(parent, exist_ok=True)
    out.save(dst, "PNG", optimize=True)

    return {
        "source": src,
        "output": dst,
        "corner_bg": "#%02x%02x%02x" % bg,
        "original": list(orig_size),
        "bbox": list(bbox),
        "width": out.width,
        "height": out.height,
        "bytes": os.path.getsize(dst),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract an editorial illustration onto a seamless transparent PNG."
    )
    parser.add_argument("input", help="Path to source generated image (.jpg/.png)")
    parser.add_argument("output", help="Path to output transparent PNG")
    parser.add_argument(
        "--tolerance",
        type=int,
        default=24,
        help="Max per-channel RGB distance from corner background to remove (default: 24)",
    )
    parser.add_argument(
        "--fringe-passes",
        type=int,
        default=2,
        help="Anti-aliased edge smoothing passes adjacent to transparency (default: 2)",
    )
    parser.add_argument(
        "--pad",
        type=int,
        default=24,
        help="Transparent padding around cropped artwork bounds in px (default: 24)",
    )
    parser.add_argument(
        "--max-width",
        type=int,
        default=None,
        help="Optional maximum output width in px (preserves aspect ratio)",
    )
    args = parser.parse_args()

    result = extract(
        src=args.input,
        dst=args.output,
        tolerance=args.tolerance,
        fringe_passes=args.fringe_passes,
        pad=args.pad,
        max_width=args.max_width,
    )
    print(json.dumps(result))


if __name__ == "__main__":
    main()
