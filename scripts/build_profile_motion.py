#!/usr/bin/env python3
"""Generate personal identity and distinct applied-AI/research process animations.

The isometric hero reflects Goh Kun Ming's creative computing identity. Process
cards describe a personal approach, not a claim that every project is deployed.
All geometry is original and schematic. Static versions retain the full story.
"""

from __future__ import annotations

import argparse
import math
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ITEMS = ("hero", "applied", "research")
FPS = 12
LOOP_SECONDS = 8
SCALE = 2
NAVY = "#08111C"
PAPER = "#F4F0E8"
TEAL = "#64E2CB"
CORAL = "#FFA58A"
VIOLET = "#B8ADFF"
MUTED = "#A5B4BF"
LINE = "#2A3C4C"
Point = tuple[float, float]

# The ordering is meaningful: applied work closes the product feedback loop;
# research closes the evidence/question loop. Neither sequence implies success.
STEPS = {
    "applied": (
        ("Engage stakeholders", "& frame needs", "Success criteria + constraints", TEAL),
        ("Inspect data", "", "Quality, leakage, coverage", VIOLET),
        ("Baseline", "& evaluate", "Metrics, trade-offs, review", CORAL),
        ("Integrate product", "", "Co-design, interfaces, serving", TEAL),
        ("Validate", "& release", "Tests, usability, handover", VIOLET),
        ("Monitor", "& iterate", "Stakeholder + system feedback", CORAL),
    ),
    "research": (
        ("Literature", "& gap", "Prior work and open problems", VIOLET),
        ("Question", "& hypothesis", "A testable research claim", TEAL),
        ("Design", "controlled study", "Controls, splits, protocol", CORAL),
        ("Run baselines", "& experiments", "Fair comparisons, ablations", VIOLET),
        ("Analyse uncertainty", "& limitations", "Variation and failure modes", TEAL),
        ("Reproduce", "& communicate", "Methods, evidence, boundaries", CORAL),
    ),
}


def dimensions(item: str, *, mobile: bool = False) -> tuple[int, int]:
    """Return the output dimensions for an identity or process visual."""
    if item == "hero":
        return (600, 690) if mobile else (1200, 480)
    return (600, 970) if mobile else (1200, 500)


def mix(a: str, b: str, amount: float) -> str:
    """Blend two hexadecimal colours into an opaque colour."""
    amount = max(0.0, min(1.0, amount))
    return "#" + "".join(
        f"{round(int(a[i : i + 2], 16) * (1 - amount) + int(b[i : i + 2], 16) * amount):02x}"
        for i in (1, 3, 5)
    )


@lru_cache(maxsize=32)
def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Use Pillow's bundled font so geometry does not depend on system fonts."""
    return ImageFont.load_default(size=size * SCALE)


def label(
    draw: ImageDraw.ImageDraw,
    xy: Point,
    value: str,
    size: int = 20,
    color: str = PAPER,
    *,
    anchor: str = "lt",
) -> None:
    """Draw text in output-pixel coordinates."""
    draw.text(
        tuple(round(v * SCALE) for v in xy), value, font=font(size), fill=color, anchor=anchor
    )


def path(draw: ImageDraw.ImageDraw, points: list[Point], color: str, width: float = 1) -> None:
    """Draw a continuous antialiased path in logical pixels."""
    if len(points) > 1:
        draw.line(
            [(round(x * SCALE), round(y * SCALE)) for x, y in points],
            fill=color,
            width=max(1, round(width * SCALE)),
            joint="curve",
        )


def polygon(draw: ImageDraw.ImageDraw, points: list[Point], color: str) -> None:
    """Draw a filled isometric face."""
    draw.polygon([(round(x * SCALE), round(y * SCALE)) for x, y in points], fill=color)


def circle(draw: ImageDraw.ImageDraw, point: Point, radius: float, color: str) -> None:
    """Draw a filled logical-pixel circle."""
    x, y = point
    draw.ellipse(
        tuple(round(v * SCALE) for v in (x - radius, y - radius, x + radius, y + radius)),
        fill=color,
    )


def glow(draw: ImageDraw.ImageDraw, point: Point, color: str, radius: float = 3) -> None:
    """Draw a restrained luminous marker without large blurred regions."""
    for multiplier, strength in ((3.2, 0.07), (2.3, 0.15), (1.5, 0.4), (1, 1)):
        circle(draw, point, radius * multiplier, mix(NAVY, color, strength))
    circle(draw, point, radius * 0.4, PAPER)


def rect(
    draw: ImageDraw.ImageDraw,
    box: tuple[float, float, float, float],
    color: str = LINE,
    *,
    fill: str = NAVY,
    radius: float = 12,
    width: float = 1,
) -> None:
    """Draw a rounded frame or process card."""
    draw.rounded_rectangle(
        tuple(round(v * SCALE) for v in box),
        radius=round(radius * SCALE),
        fill=fill,
        outline=color,
        width=max(1, round(width * SCALE)),
    )


def route(draw: ImageDraw.ImageDraw, points: list[Point], color: str) -> None:
    """Draw a route with a directional arrow that does not overlap its destination."""
    path(draw, points, color, 1.5)
    a, b = points[-2:]
    angle = math.atan2(b[1] - a[1], b[0] - a[0])
    path(
        draw,
        [
            (b[0] - 7 * math.cos(angle - 0.5), b[1] - 7 * math.sin(angle - 0.5)),
            b,
            (b[0] - 7 * math.cos(angle + 0.5), b[1] - 7 * math.sin(angle + 0.5)),
        ],
        color,
        1.5,
    )


def packet(draw: ImageDraw.ImageDraw, points: list[Point], phase: float, color: str) -> None:
    """Move a light packet at constant speed along a piecewise-linear route."""
    lengths = [math.dist(a, b) for a, b in zip(points[:-1], points[1:], strict=True)]
    distance = (phase % 1) * sum(lengths)
    for a, b, length in zip(points[:-1], points[1:], lengths, strict=True):
        if distance <= length:
            fraction = distance / length if length else 0
            glow(draw, (a[0] + (b[0] - a[0]) * fraction, a[1] + (b[1] - a[1]) * fraction), color)
            return
        distance -= length


def canvas(item: str, *, mobile: bool) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    """Create a supersampled navy canvas with a subtle boundary."""
    width, height = dimensions(item, mobile=mobile)
    image = Image.new("RGB", (width * SCALE, height * SCALE), NAVY)
    draw = ImageDraw.Draw(image)
    rect(draw, (0.5, 0.5, width - 0.5, height - 0.5), radius=18)
    return image, draw


def landscape(draw: ImageDraw.ImageDraw, progress: float, *, mobile: bool, static: bool) -> None:
    """Render isometric building blocks and flowing mathematical field lines."""
    origin = (300, 375) if mobile else (927, 157)
    scale = 1.06 if mobile else 0.97

    def project(x: float, y: float, z: float = 0) -> Point:
        return origin[0] + (x - y) * 25 * scale, origin[1] + ((x + y) * 12.5 - z * 27) * scale

    for i in range(9):
        path(draw, [project(i, 0, -2.2), project(i, 8, -2.2)], mix(NAVY, LINE, 0.8))
        path(draw, [project(0, i, -2.2), project(8, i, -2.2)], mix(NAVY, LINE, 0.8))
    for x in range(7):
        for y in range(7):
            if (x * 3 + y) % 5 == 0 or (x in (2, 3, 4) and y in (2, 3, 4)):
                height = 0.35 + (math.sin(x * 0.8) * math.cos(y * 0.65) + 1) * 0.6
                color = (TEAL, VIOLET, CORAL)[(x + y) % 3]
                top = [
                    project(a, b, height - 2.2)
                    for a, b in ((x, y), (x + 0.92, y), (x + 0.92, y + 0.92), (x, y + 0.92))
                ]
                base = [
                    project(a, b, -2.2)
                    for a, b in ((x + 0.92, y), (x + 0.92, y + 0.92), (x, y + 0.92))
                ]
                pulse = 0.5 + 0.5 * math.sin(2 * math.pi * (progress - (x + y) / 16))
                polygon(draw, [top[1], top[2], base[1], base[0]], mix(NAVY, color, 0.14))
                polygon(draw, [top[2], top[3], base[2], base[1]], mix(NAVY, color, 0.08))
                polygon(draw, top, mix(NAVY, color, 0.22 if static else 0.16 + pulse * 0.17))
                path(draw, [*top, top[0]], mix(NAVY, color, 0.55), 1)
                path(draw, [top[2], base[1]], mix(NAVY, color, 0.3))

    def surface(u: float, v: float) -> Point:
        z = 1.2 * math.sin(u * 0.65) * math.cos(v * 0.6) + 0.3 * math.sin(v)
        return project(u, v, z + 1.7)

    for index in range(25):
        position = 7 * index / 24
        color = TEAL if index < 8 else VIOLET if index < 17 else CORAL
        points = [surface(position, step * 7 / 36) for step in range(37)]
        path(draw, points, mix(NAVY, color, 0.6), 1)
    for index in range(17):
        position = 7 * index / 16
        path(draw, [surface(step * 7 / 36, position) for step in range(37)], mix(NAVY, PAPER, 0.17))
    for u, v, color in ((0, 2, TEAL), (4, 7, CORAL), (7, 0, VIOLET)):
        x, y = surface(u, v)
        path(draw, [(x, y), (x, y + 55)], mix(NAVY, color, 0.35))
        circle(draw, (x, y + 55), 2, color)
        glow(draw, (x, y), color, 3)
    if not static:
        for index, color in ((4, TEAL), (12, VIOLET), (21, CORAL)):
            points = [surface(7 * index / 24, step * 7 / 60) for step in range(61)]
            packet(draw, points, progress * 2 + index / 25, color)


def hero_frame(progress: float, *, mobile: bool, static: bool) -> Image.Image:
    """Render the name, personal positioning, and animated research landscape."""
    image, draw = canvas("hero", mobile=mobile)
    if mobile:
        label(draw, (34, 34), "SINGAPORE / APPLIED AI & ANALYTICS", 15, TEAL)
        label(draw, (34, 80), "Goh Kun Ming", 35)
        label(draw, (32, 145), "Researching intelligence.", 43)
        label(draw, (32, 200), "Building useful AI.", 47, TEAL)
        label(draw, (34, 258), "From rigorous questions to working systems.", 21, MUTED)
        landscape(draw, progress, mobile=mobile, static=static)
        path(draw, [(34, 638), (566, 638)], LINE)
        label(draw, (34, 658), "RESEARCH + ENGINEERING + CURIOSITY", 15)
    else:
        label(draw, (52, 37), "SINGAPORE / APPLIED AI & ANALYTICS", 15, TEAL)
        label(draw, (52, 88), "Goh Kun Ming", 37)
        label(draw, (49, 161), "Researching intelligence.", 49)
        label(draw, (49, 224), "Building useful AI.", 55, TEAL)
        label(draw, (52, 305), "From rigorous questions", 25, MUTED)
        label(draw, (52, 339), "to working systems.", 25, MUTED)
        path(draw, [(665, 82), (665, 375)], LINE)
        landscape(draw, progress, mobile=mobile, static=static)
        label(draw, (1148, 40), "GOH KUN MING / PORTFOLIO", 12, MUTED, anchor="rt")
        path(draw, [(52, 397), (1148, 397)], LINE)
        label(draw, (52, 427), "RESEARCH + ENGINEERING + CURIOSITY", 16)
        label(draw, (1148, 430), "IDEAS INTO UNDERSTANDING", 12, MUTED, anchor="rt")
    return image


def process_geometry(*, mobile: bool) -> tuple[list[tuple[int, int, int, int]], list[list[Point]]]:
    """Place six cards and six separate routes without crossing text."""
    if mobile:
        boxes = [(74, 143 + index * 121, 560, 243 + index * 121) for index in range(6)]
        routes = [[(317, box[3]), (317, boxes[i + 1][1] - 1)] for i, box in enumerate(boxes[:-1])]
        routes.append([(74, 798), (34, 798), (34, 193), (72, 193)])
    else:
        xs, ys = (54, 433, 812), (143, 295)
        boxes = [
            (xs[i], ys[j], xs[i] + 334, ys[j] + 108)
            for i, j in ((0, 0), (1, 0), (2, 0), (2, 1), (1, 1), (0, 1))
        ]
        routes = [
            [(388, 197), (431, 197)],
            [(767, 197), (810, 197)],
            [(979, 251), (979, 293)],
            [(812, 349), (769, 349)],
            [(433, 349), (390, 349)],
            [(54, 349), (26, 349), (26, 197), (52, 197)],
        ]
    return boxes, routes


def stage_icon(draw: ImageDraw.ImageDraw, xy: Point, index: int, color: str) -> None:
    """Render a tiny six-position progress glyph instead of a generic badge."""
    x, y = xy
    for position in range(6):
        angle = -math.pi / 2 + position * math.tau / 6
        circle(
            draw,
            (x + math.cos(angle) * 15, y + math.sin(angle) * 15),
            3.5 if position == index else 2,
            color if position == index else mix(NAVY, color, 0.25),
        )
    label(draw, (x, y - 7), str(index + 1).zfill(2), 13, color, anchor="mt")


def process_frame(item: str, progress: float, *, mobile: bool, static: bool) -> Image.Image:
    """Render one distinct process as progressive stages and a feedback loop."""
    image, draw = canvas(item, mobile=mobile)
    width, height = dimensions(item, mobile=mobile)
    research = item == "research"
    accent = VIOLET if research else TEAL
    label(draw, (34 if mobile else 44, 28), "Research" if research else "Applied AI", 38, PAPER)
    label(
        draw,
        (34 if mobile else 45, 80),
        "From an open question to defensible evidence."
        if research
        else "From shared success criteria to a useful system.",
        19 if mobile else 21,
        MUTED,
    )
    if not mobile:
        label(draw, (1156, 42), "HOW I WORK", 13, accent, anchor="rt")
    boxes, routes = process_geometry(mobile=mobile)
    active = min(5, int(progress * 6))
    phase = (progress * 6) % 1
    for i, points in enumerate(routes):
        route(draw, points, mix(NAVY, STEPS[item][i][3], 0.5))
        if not static and i == active:
            packet(draw, points, phase, STEPS[item][i][3])
    for index, (box, (title, continuation, detail, color)) in enumerate(
        zip(boxes, STEPS[item], strict=True)
    ):
        x1, y1, x2, y2 = box
        selected = index == active and not static
        strength = 0.75 if static else 1 if selected else 0.4
        rect(
            draw,
            box,
            mix(NAVY, color, strength),
            fill=mix(NAVY, color, 0.06 if selected else 0.018),
            width=1.7 if selected else 1,
        )
        stage_icon(draw, (x1 + 35, y1 + 39), index, color)
        tx = x1 + 66
        if continuation:
            label(draw, (tx, y1 + 15), title, 24 if mobile else 22)
            label(draw, (tx, y1 + 43), continuation, 24 if mobile else 22)
            label(draw, (tx, y1 + 77), detail, 17 if mobile else 15, MUTED)
        else:
            label(draw, (tx, y1 + 26), title, 24 if mobile else 22)
            label(draw, (tx, y1 + 65), detail, 17 if mobile else 15, MUTED)
        if selected:
            path(draw, [(x1 + 13, y2 - 7), (x1 + 13 + (x2 - x1 - 26) * phase, y2 - 7)], color, 2)
    footer_y = height - 48
    path(
        draw,
        [(34 if mobile else 44, footer_y), (width - 34 if mobile else width - 44, footer_y)],
        LINE,
    )
    footer = (
        "New evidence refines the next research question."
        if research
        else "Stakeholder feedback informs each iteration."
    )
    label(draw, (34 if mobile else 44, footer_y + 17), footer, 17 if mobile else 18, accent)
    if not mobile:
        label(draw, (1156, footer_y + 20), "ITERATIVE BY DESIGN", 12, MUTED, anchor="rt")
    return image


def render_frame(
    item: str, progress: float, *, mobile: bool = False, static: bool = False
) -> Image.Image:
    """Render one identity or process illustration at native output resolution.

    Args:
        item: One of ITEMS: hero, applied, or research.
        progress: Finite normalised loop time in the closed interval [0, 1].
        mobile: Whether to compose a narrow-screen layout.
        static: Whether to show the complete diagram without active motion.

    Returns:
        An antialiased RGB image with all public labels retained.

    Raises:
        ValueError: If the item or normalised loop time is invalid.
    """
    if item not in ITEMS:
        raise ValueError(f"item must be one of {ITEMS}")
    if not math.isfinite(progress) or not 0 <= progress <= 1:
        raise ValueError("progress must be finite and within [0, 1]")
    time = 0.35 if static else progress
    image = (
        hero_frame(time, mobile=mobile, static=static)
        if item == "hero"
        else process_frame(item, time, mobile=mobile, static=static)
    )
    return image.resize(dimensions(item, mobile=mobile), Image.Resampling.LANCZOS)


def build(output: Path = ASSETS) -> dict[str, int]:
    """Generate six looping GIFs and their six reduced-motion PNG fallbacks."""
    output.mkdir(parents=True, exist_ok=True)
    sizes = {}
    frame_count = FPS * LOOP_SECONDS
    durations = [
        round((i + 1) * 100 / FPS) * 10 - round(i * 100 / FPS) * 10 for i in range(frame_count)
    ]
    for item in ITEMS:
        for mobile in (False, True):
            stem = ("profile-hero" if item == "hero" else f"process-{item}") + (
                "-mobile" if mobile else ""
            )
            still = render_frame(item, 0.35, mobile=mobile, static=True)
            still.save(output / f"{stem}-static.png", optimize=True)
            palette = still.quantize(colors=128, method=Image.Quantize.MEDIANCUT)
            frames = [
                render_frame(item, i / frame_count, mobile=mobile).quantize(
                    palette=palette, dither=Image.Dither.NONE
                )
                for i in range(frame_count)
            ]
            frames[0].save(
                output / f"{stem}.gif",
                save_all=True,
                append_images=frames[1:],
                duration=durations,
                loop=0,
                optimize=True,
                disposal=1,
            )
            for suffix in (".gif", "-static.png"):
                file = output / f"{stem}{suffix}"
                sizes[file.name] = file.stat().st_size
    return sizes


def main() -> None:
    """Build assets into the requested directory."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ASSETS)
    args = parser.parse_args()
    for name, size in build(args.output).items():
        print(f"{name}: {size:,} bytes")


if __name__ == "__main__":
    main()
