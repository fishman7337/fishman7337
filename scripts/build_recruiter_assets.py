#!/usr/bin/env python3
"""Build compact, original SVG field notes for the recruiter-facing profile."""

from __future__ import annotations

import html
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
NAVY = "#08111C"
PAPER = "#F4F0E8"
TEAL = "#64E2CB"
CORAL = "#FFA58A"
VIOLET = "#B8ADFF"
MUTED = "#A5B4BF"
LINE = "#2A3C4C"


def text(
    x: float,
    y: float,
    value: str,
    size: int = 20,
    color: str = PAPER,
    *,
    weight: int = 400,
    spacing: float = 0,
    anchor: str = "start",
    mono: bool = False,
) -> str:
    """Return one escaped text node with explicit, portable font fallbacks."""
    font = "'DejaVu Sans Mono',Consolas,monospace" if mono else "Arial,'DejaVu Sans',sans-serif"
    return (
        f'<text x="{x:g}" y="{y:g}" fill="{color}" font-size="{size}" '
        f'font-family="{font}" font-weight="{weight}" letter-spacing="{spacing:g}" '
        f'text-anchor="{anchor}">{html.escape(value)}</text>'
    )


def line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    color: str = LINE,
    *,
    width: float = 1,
    opacity: float = 1,
) -> str:
    """Return a straight diagram edge."""
    return (
        f'<path d="M{x1:g} {y1:g}L{x2:g} {y2:g}" fill="none" '
        f'stroke="{color}" stroke-width="{width:g}" opacity="{opacity:g}"/>'
    )


def path(points: list[tuple[float, float]], color: str, opacity: float = 1) -> str:
    """Return a deterministic polyline with compact rounded coordinates."""
    coordinates = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return (
        f'<polyline points="{coordinates}" fill="none" stroke="{color}" '
        f'stroke-width="1.2" stroke-linejoin="round" opacity="{opacity:g}"/>'
    )


def polygon(points: list[tuple[float, float]], color: str, opacity: float = 1) -> str:
    """Return an isometric face or filled geometry."""
    coordinates = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polygon points="{coordinates}" fill="{color}" opacity="{opacity:g}"/>'


def dot(x: float, y: float, color: str = TEAL, radius: float = 3) -> str:
    """Return a small diagram node."""
    return f'<circle cx="{x:g}" cy="{y:g}" r="{radius:g}" fill="{color}"/>'


def open_svg(title: str, description: str, width: int, height: int) -> str:
    """Open an accessible self-contained SVG with shared diagram definitions."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">'
        f'<title id="title">{html.escape(title)}</title>'
        f'<desc id="desc">{html.escape(description)}</desc>'
        '<defs><linearGradient id="signal" x1="0" y1="1" x2="1" y2="0">'
        f'<stop stop-color="{TEAL}"/><stop offset=".55" stop-color="{VIOLET}"/>'
        f'<stop offset="1" stop-color="{CORAL}"/></linearGradient>'
        '<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">'
        f'<circle cx="1" cy="1" r=".8" fill="{MUTED}" opacity=".15"/></pattern>'
        "<style>.signal{animation:breathe 7s ease-in-out infinite}"
        "@keyframes breathe{0%,100%{opacity:.68}50%{opacity:1}}"
        "@media(prefers-reduced-motion:reduce){.signal{animation:none}}</style></defs>"
        f'<rect width="{width}" height="{height}" rx="18" fill="{NAVY}"/>'
        f'<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" '
        f'rx="17.5" fill="none" stroke="{LINE}"/>'
    )


def iso(x: float, y: float, z: float, *, scale: float = 1) -> tuple[float, float]:
    """Project a Cartesian point onto a two-to-one isometric plane."""
    return (x - y) * 25 * scale, ((x + y) * 12.5 - z * 27) * scale


def block(x: float, y: float, height: float, color: str, scale: float = 1) -> str:
    """Draw one small voxel with shaded sides and a crisp upper perimeter."""
    top = [
        iso(a, b, height, scale=scale) for a, b in [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]
    ]
    base = [iso(a, b, 0, scale=scale) for a, b in [(x + 1, y), (x + 1, y + 1), (x, y + 1)]]
    return (
        polygon([top[1], top[2], base[1], base[0]], color, 0.16)
        + polygon([top[2], top[3], base[2], base[1]], color, 0.08)
        + polygon(top, color, 0.26)
        + path([*top, top[0]], color, 0.48)
        + line(*top[2], *base[1], color, opacity=0.35)
    )


def landscape() -> str:
    """Build a voxel landscape under a continuous conceptual research surface."""
    parts = ['<g transform="translate(0 142)">']
    for index in range(9):
        parts.append(line(*iso(index, 0, 0), *iso(index, 8, 0), opacity=0.7))
        parts.append(line(*iso(0, index, 0), *iso(8, index, 0), opacity=0.7))
    for x in range(7):
        for y in range(7):
            if (x * 3 + y) % 5 == 0 or (x in [2, 3, 4] and y in [2, 3, 4]):
                height = 0.3 + (math.sin(x * 0.8) * math.cos(y * 0.65) + 1) * 0.65
                color = [TEAL, VIOLET, CORAL][(x + y) % 3]
                parts.append(block(x + 0.06, y + 0.06, height, color))
    parts.append("</g>")

    def surface(u: float, v: float) -> tuple[float, float]:
        z = 1.2 * math.sin(u * 0.65) * math.cos(v * 0.6) + 0.3 * math.sin(v)
        px, py = iso(u, v, z)
        return px, py + 23

    parts.append('<g class="signal">')
    for index in range(25):
        position = 7 * index / 24
        color = TEAL if index < 8 else VIOLET if index < 17 else CORAL
        parts.append(path([surface(position, step * 7 / 36) for step in range(37)], color, 0.65))
    for index in range(17):
        position = 7 * index / 16
        parts.append(path([surface(step * 7 / 36, position) for step in range(37)], PAPER, 0.2))
    parts.append("</g>")
    for u, v, color in [(0, 2, TEAL), (4, 7, CORAL), (7, 0, VIOLET)]:
        x, y = surface(u, v)
        parts.append(line(x, y, x, y + 65, color, opacity=0.35))
        parts.append(dot(x, y, color, 3.5))
        parts.append(dot(x, y + 65, color, 2))
    return "".join(parts)


def make_hero(*, mobile: bool = False) -> str:
    """Render a responsive identity hero with an isometric research landscape."""
    width, height = (600, 690) if mobile else (1200, 480)
    parts = [
        open_svg(
            "Goh Kun Ming — Researching intelligence. Building useful AI.",
            "Applied AI and Analytics, Singapore. A continuous mathematical mesh floats over "
            "an isometric block landscape: a conceptual connection between research, systems "
            "engineering, and creative computing. The geometry is illustrative, not measured data.",
            width,
            height,
        )
    ]
    if mobile:
        parts.extend(
            [
                text(34, 43, "SINGAPORE / APPLIED AI & ANALYTICS", 13, TEAL, mono=True),
                text(34, 91, "Goh Kun Ming", 30, weight=700, spacing=-0.6),
                text(32, 159, "Researching intelligence.", 43, weight=700, spacing=-1.7),
                text(32, 214, "Building useful AI.", 47, TEAL, weight=700, spacing=-1.6),
                text(34, 260, "From rigorous questions to working systems.", 20, MUTED),
                '<rect x="24" y="295" width="552" height="330" fill="url(#dots)"/>',
                f'<g transform="translate(300 301) scale(.95)">{landscape()}</g>',
                line(34, 638, 566, 638),
                text(
                    34, 667, "RESEARCH × ENGINEERING × CURIOSITY", 13, PAPER, mono=True, spacing=0.3
                ),
            ]
        )
    else:
        parts.extend(
            [
                text(
                    52, 48, "SINGAPORE / APPLIED AI & ANALYTICS", 13, TEAL, mono=True, spacing=0.5
                ),
                text(52, 106, "Goh Kun Ming", 32, weight=700, spacing=-0.7),
                text(49, 187, "Researching intelligence.", 49, weight=700, spacing=-1.8),
                text(49, 249, "Building useful AI.", 55, TEAL, weight=700, spacing=-1.7),
                text(52, 307, "From rigorous questions", 23, MUTED),
                text(52, 339, "to working systems.", 23, MUTED),
                line(665, 80, 665, 377),
                '<rect x="694" y="78" width="462" height="315" fill="url(#dots)"/>',
                f'<g transform="translate(926 67) scale(.94)">{landscape()}</g>',
                text(1128, 48, "FIELD NOTES / 01", 12, MUTED, anchor="end", mono=True),
                line(52, 397, 1148, 397),
                text(
                    52, 438, "RESEARCH × ENGINEERING × CURIOSITY", 14, PAPER, mono=True, spacing=0.7
                ),
                text(
                    1148, 438, "A CONTINUOUS WORK IN PROGRESS", 11, MUTED, anchor="end", mono=True
                ),
            ]
        )
    return "".join([*parts, "</svg>"])


def arrow(x: float, y: float, *, vertical: bool = False, color: str = MUTED) -> str:
    """Draw a compact directional arrow between workflow stages."""
    if vertical:
        return line(x, y, x, y + 26, color) + path(
            [(x - 4, y + 21), (x, y + 26), (x + 4, y + 21)], color
        )
    return line(x, y, x + 30, y, color) + path(
        [(x + 25, y - 4), (x + 30, y), (x + 25, y + 4)], color
    )


def make_workflow(*, mobile: bool = False) -> str:
    """Render the conceptual question-to-product workflow and evaluation foundation."""
    width, height = (600, 570) if mobile else (1200, 240)
    stages = [
        ("QUESTION", "Frame the decision", TEAL),
        ("DATA", "Understand the evidence", VIOLET),
        ("MODELS", "Experiment & evaluate", CORAL),
        ("PRODUCT", "Build for people", PAPER),
    ]
    parts = [
        open_svg(
            "How I work: question, data, models, product",
            "Frame the decision; understand the evidence; experiment and evaluate; build for people. "
            "Evaluation and responsible engineering underpin every stage. Conceptual workflow.",
            width,
            height,
        ),
        text(
            34 if mobile else 44,
            34,
            "FROM A GOOD QUESTION TO A USEFUL SYSTEM",
            12,
            MUTED,
            mono=True,
            spacing=0.5,
        ),
    ]
    for index, (title, subtitle, color) in enumerate(stages):
        x, y = (90, 96 + index * 105) if mobile else (44 + index * 286, 104)
        parts.extend(
            [
                text(x, y - 31, f"0{index + 1}", 12, color, mono=True),
                text(x, y, title, 29 if mobile else 27, color, weight=700, spacing=0.2),
                text(x, y + 29, subtitle, 19 if mobile else 18, MUTED),
            ]
        )
        if mobile:
            parts.append(dot(43, y - 12, color, 4))
            if index < 3:
                parts.append(line(43, y - 4, 43, y + 85))
        elif index < 3:
            parts.append(arrow(x + 221, y - 8))
    foundation_y = 500 if mobile else 187
    parts.extend(
        [
            line(
                34 if mobile else 44,
                foundation_y - 21,
                width - 34 if mobile else width - 44,
                foundation_y - 21,
            ),
            dot(42 if mobile else 52, foundation_y + 11, TEAL, 3),
            text(
                58 if mobile else 69,
                foundation_y + 18,
                "Evaluation & responsible engineering",
                22 if mobile else 20,
            ),
            text(width - 44, foundation_y + 18, "AT EVERY STAGE", 11, TEAL, anchor="end", mono=True)
            if not mobile
            else "",
        ]
    )
    return "".join([*parts, "</svg>"])


def project_frame(index: str, title: str, subtitle: str, description: str, color: str) -> list[str]:
    """Open a project strip with an editorial title and a separate diagram field."""
    return [
        open_svg(title, description, 1200, 220),
        text(36, 40, f"SELECTED WORK / {index}", 12, color, mono=True, spacing=1),
        text(34, 105, title, 36, weight=700, spacing=-0.7),
        text(36, 143, subtitle, 18, MUTED),
        text(36, 192, "CONCEPTUAL SCHEMATIC", 10, MUTED, mono=True, spacing=0.9),
        line(570, 28, 570, 192),
        '<rect x="594" y="18" width="578" height="184" fill="url(#dots)"/>',
    ]


def make_quantum() -> str:
    """Draw a circuit-to-generator schematic without invented experimental results."""
    parts = project_frame(
        "01",
        "Hybrid generative models",
        "Classical baselines · circuit-based latent priors",
        "Conceptual circuit gates feed a classical generator, producing a stylised image grid. "
        "This illustration does not report measurements or quantum advantage.",
        VIOLET,
    )
    for index, y in enumerate([65, 109, 153]):
        parts.append(text(605, y + 5, f"q{index}", 12, MUTED, mono=True))
        parts.append(line(635, y, 838, y, VIOLET, opacity=0.65))
        for x, label in [(670, "H"), (760, "R")]:
            parts.extend(
                [
                    f'<rect x="{x}" y="{y - 14}" width="28" height="28" rx="3" fill="{NAVY}" stroke="{VIOLET}"/>',
                    text(x + 14, y + 5, label, 14, VIOLET, anchor="middle", mono=True),
                ]
            )
    parts.extend(
        [line(725, 65, 725, 153, VIOLET), dot(725, 65, VIOLET, 4), dot(725, 153, VIOLET, 4)]
    )
    parts.extend(
        [
            arrow(842, 109, color=VIOLET),
            f'<rect x="887" y="64" width="120" height="90" rx="8" fill="#152030" stroke="{TEAL}" stroke-opacity=".65"/>',
            text(947, 102, "CLASSICAL", 12, TEAL, anchor="middle", mono=True),
            text(947, 126, "GENERATOR", 12, PAPER, anchor="middle", mono=True),
            arrow(1017, 109, color=TEAL),
        ]
    )
    for row in range(4):
        for col in range(4):
            color = [TEAL, VIOLET, CORAL][(row + col) % 3]
            parts.append(
                f'<rect x="{1065 + col * 21}" y="{70 + row * 21}" width="16" height="16" rx="2" fill="{color}" opacity="{0.25 + ((row * 3 + col) % 4) * 0.18:.2f}"/>'
            )
    parts.append(
        text(
            879,
            190,
            "LATENT PRIOR → GENERATOR → IMAGE",
            10,
            MUTED,
            anchor="middle",
            mono=True,
            spacing=0.6,
        )
    )
    return "".join([*parts, "</svg>"])


def leaf(x: float, y: float, angle: float, color: str = TEAL) -> str:
    """Draw a botanical outline and its midrib with a fixed conceptual geometry."""
    return (
        f'<g transform="translate({x:g} {y:g}) rotate({angle:g})">'
        f'<path d="M0 47C-48 14-33-38 0-57C35-35 46 16 0 47Z" fill="{color}" '
        f'fill-opacity=".12" stroke="{color}" stroke-width="1.5"/>'
        f'<path d="M0 56V-47M0 24L-23 1M0 4L24-21M0-17L-16-30" fill="none" '
        f'stroke="{color}" stroke-width="1.1" opacity=".65"/></g>'
    )


def make_vision() -> str:
    """Draw labelled botanical detections without confidence or accuracy claims."""
    parts = project_frame(
        "02",
        "Leaf object detection",
        "Dataset preparation · detection · ONNX export",
        "Conceptual leaves inside object-detection boxes, connected to an inference output. "
        "The boxes are illustrative and contain no fabricated confidence scores.",
        TEAL,
    )
    parts.extend(
        [
            '<g transform="translate(624 27)">',
            leaf(85, 90, -25),
            leaf(191, 89, 31, VIOLET),
            f'<rect x="26" y="20" width="108" height="138" fill="none" stroke="{TEAL}" stroke-width="1.2"/>',
            f'<rect x="137" y="21" width="112" height="137" fill="none" stroke="{VIOLET}" stroke-width="1.2"/>',
            f'<rect x="26" y="9" width="50" height="18" fill="{TEAL}"/>',
            text(31, 22, "leaf", 12, NAVY, mono=True),
            f'<rect x="137" y="10" width="50" height="18" fill="{VIOLET}"/>',
            text(142, 23, "leaf", 12, NAVY, mono=True),
            "</g>",
            arrow(903, 110, color=TEAL),
            f'<rect x="956" y="49" width="184" height="122" rx="7" fill="#101E2B" stroke="{LINE}"/>',
            line(956, 73, 1140, 73),
            dot(969, 61, TEAL, 2),
            dot(979, 61, VIOLET, 2),
            dot(989, 61, CORAL, 2),
            text(974, 101, "DETECT", 13, PAPER, mono=True),
            text(974, 126, "VALIDATE", 13, TEAL, mono=True),
            text(974, 151, "EXPORT", 13, MUTED, mono=True),
        ]
    )
    return "".join([*parts, "</svg>"])


def make_product() -> str:
    """Draw a produce-classification product as a small service architecture."""
    parts = project_frame(
        "03",
        "VeggieAI",
        "Image classification · application engineering",
        "A conceptual produce image passes through an application and model service to "
        "prediction history. This is a simplified illustration, not a deployment topology.",
        CORAL,
    )
    parts.extend(
        [
            f'<rect x="618" y="51" width="104" height="118" rx="8" fill="#16252A" stroke="{LINE}"/>',
            leaf(671, 105, 0, TEAL),
            arrow(734, 110, color=CORAL),
            f'<rect x="782" y="70" width="140" height="80" rx="8" fill="#201E25" stroke="{CORAL}" stroke-opacity=".6"/>',
            text(852, 105, "APP", 17, CORAL, anchor="middle", mono=True),
            text(852, 128, "Flask", 13, PAPER, anchor="middle"),
            line(922, 110, 962, 110, CORAL, opacity=0.7),
            line(962, 110, 962, 56, CORAL, opacity=0.7),
            line(962, 110, 962, 163, CORAL, opacity=0.7),
            line(962, 56, 987, 56, CORAL, opacity=0.7),
            line(962, 163, 987, 163, CORAL, opacity=0.7),
            dot(962, 110, CORAL, 3),
            f'<rect x="987" y="28" width="162" height="57" rx="7" fill="#152030" stroke="{VIOLET}" stroke-opacity=".6"/>',
            text(1068, 52, "MODEL SERVICE", 12, VIOLET, anchor="middle", mono=True),
            text(1068, 72, "TensorFlow", 12, PAPER, anchor="middle"),
            f'<rect x="987" y="135" width="162" height="57" rx="7" fill="#132627" stroke="{TEAL}" stroke-opacity=".6"/>',
            text(1068, 159, "HISTORY", 12, TEAL, anchor="middle", mono=True),
            text(1068, 179, "SQLite", 12, PAPER, anchor="middle"),
            text(852, 182, "AUTHENTICATED WORKFLOWS", 9, MUTED, anchor="middle", mono=True),
        ]
    )
    return "".join([*parts, "</svg>"])


def make_data() -> str:
    """Draw Singapore-inspired housing blocks and an explanatory map legend."""
    parts = project_frame(
        "04",
        "HDB resale analytics",
        "Singapore housing · geospatial analysis · visual stories",
        "An illustrative isometric Singapore housing neighbourhood connects to location, "
        "time, and flat-type facets. Building geometry is conceptual; no values depict prices.",
        TEAL,
    )
    parts.append('<g transform="translate(781 100)">')
    for index in range(6):
        parts.append(line(*iso(index, 0, 0, scale=0.9), *iso(index, 5, 0, scale=0.9), opacity=0.6))
        parts.append(line(*iso(0, index, 0, scale=0.9), *iso(5, index, 0, scale=0.9), opacity=0.6))
    for x, y, height, color in [
        (0, 0, 2.3, VIOLET),
        (2, 0, 2.8, TEAL),
        (0, 2, 1.9, CORAL),
        (2, 2, 2.5, VIOLET),
        (4, 1, 1.8, TEAL),
        (1, 4, 1.4, TEAL),
    ]:
        parts.append(block(x, y, height, color, 0.9))
        for floor in range(1, int(height * 3)):
            a, b = (
                iso(x + 1.02, y + 0.15, floor * 0.3, scale=0.9),
                iso(x + 1.02, y + 0.8, floor * 0.3, scale=0.9),
            )
            parts.append(line(*a, *b, color, opacity=0.6))
    parts.append("</g>")
    for index, (label, color) in enumerate(
        [("LOCATION", TEAL), ("TIME", VIOLET), ("FLAT TYPE", CORAL)]
    ):
        y = 65 + index * 45
        parts.extend([dot(1000, y, color, 4), text(1017, y + 5, label, 13, color, mono=True)])
    parts.append(line(953, 47, 953, 175))
    return "".join([*parts, "</svg>"])


def main() -> None:
    """Write the eight deterministic, accessible recruiter-profile SVG assets."""
    ASSETS.mkdir(parents=True, exist_ok=True)
    generated = {
        "recruiter-hero.svg": make_hero(),
        "recruiter-hero-mobile.svg": make_hero(mobile=True),
        "recruiter-workflow.svg": make_workflow(),
        "recruiter-workflow-mobile.svg": make_workflow(mobile=True),
        "recruiter-quantum.svg": make_quantum(),
        "recruiter-vision.svg": make_vision(),
        "recruiter-product.svg": make_product(),
        "recruiter-data.svg": make_data(),
    }
    for filename, document in generated.items():
        (ASSETS / filename).write_text(document + "\n", encoding="utf-8")
    print(f"Generated {len(generated)} recruiter-profile SVGs in {ASSETS}")


if __name__ == "__main__":
    main()
