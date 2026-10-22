#!/usr/bin/env python3
"""Create public-facing animated cards for six documented portfolio projects.

Workflow illustrations encode project architecture and documented scope. They
are original schematic artwork, not model outputs, predictions, or metrics.
Pillow's bundled font and a fixed palette make the assets portable and compact.
"""

from __future__ import annotations

import argparse
import math
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
PROJECTS = ("quantum", "vision", "product", "data", "housing", "forecast")
DESKTOP_SIZE = (1200, 420)
MOBILE_SIZE = (600, 680)
LOOP_SECONDS = 8
FPS = 12
SCALE = 2
NAVY = "#08111C"
PAPER = "#F4F0E8"
TEAL = "#64E2CB"
CORAL = "#FFA58A"
VIOLET = "#B8ADFF"
MUTED = "#A5B4BF"
LINE = "#2A3C4C"
Point = tuple[float, float]


def mix(a: str, b: str, amount: float) -> str:
    """Blend two hexadecimal colors without introducing transparency."""
    amount = max(0.0, min(1.0, amount))
    channels = [
        round(int(a[i : i + 2], 16) * (1 - amount) + int(b[i : i + 2], 16) * amount)
        for i in (1, 3, 5)
    ]
    return "#" + "".join(f"{channel:02x}" for channel in channels)


@lru_cache(maxsize=32)
def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Use Pillow's bundled font for portable antialiased text."""
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
    """Draw a label in output-pixel coordinates."""
    draw.text(
        tuple(round(value * SCALE) for value in xy),
        value,
        font=font(size),
        fill=color,
        anchor=anchor,
    )


def polyline(draw: ImageDraw.ImageDraw, points: list[Point], color: str, width: float = 1) -> None:
    """Draw an antialiased path using the supersampled canvas."""
    if len(points) > 1:
        draw.line(
            [(round(x * SCALE), round(y * SCALE)) for x, y in points],
            fill=color,
            width=max(1, round(width * SCALE)),
            joint="curve",
        )


def circle(
    draw: ImageDraw.ImageDraw,
    center: Point,
    radius: float,
    color: str,
    *,
    fill: bool = True,
    width: float = 1,
) -> None:
    """Draw a filled or outlined circle."""
    x, y = center
    box = tuple(round(value * SCALE) for value in (x - radius, y - radius, x + radius, y + radius))
    draw.ellipse(
        box,
        fill=color if fill else None,
        outline=None if fill else color,
        width=round(width * SCALE),
    )


def glow(
    draw: ImageDraw.ImageDraw, center: Point, color: str, radius: float = 4, *, intensity: float = 1
) -> None:
    """Draw a compact multiring glow with a crisp luminous centre."""
    for factor, strength in [(3.3, 0.045), (2.6, 0.09), (1.9, 0.18), (1.35, 0.4)]:
        circle(draw, center, radius * factor, mix(NAVY, color, strength * intensity))
    circle(draw, center, radius, mix(NAVY, color, intensity))
    circle(draw, center, radius * 0.4, mix(NAVY, PAPER, intensity))


def rect(
    draw: ImageDraw.ImageDraw,
    box: tuple[float, float, float, float],
    *,
    color: str = LINE,
    fill: str = NAVY,
    radius: float = 10,
    width: float = 1,
) -> None:
    """Draw a rounded card in logical pixels."""
    draw.rounded_rectangle(
        tuple(round(value * SCALE) for value in box),
        radius=round(radius * SCALE),
        fill=fill,
        outline=color,
        width=round(width * SCALE),
    )


def polygon(draw: ImageDraw.ImageDraw, points: list[Point], color: str) -> None:
    """Draw a filled polygon in logical pixels."""
    draw.polygon([(round(x * SCALE), round(y * SCALE)) for x, y in points], fill=color)


def pulse(
    draw: ImageDraw.ImageDraw,
    points: list[Point],
    progress: float,
    color: str,
    *,
    size: float = 4,
) -> None:
    """Move a glowing packet along an arbitrary piecewise-linear connection."""
    lengths = [math.dist(a, b) for a, b in zip(points[:-1], points[1:], strict=True)]
    target = (progress % 1) * sum(lengths)
    for a, b, length in zip(points[:-1], points[1:], lengths, strict=True):
        if target <= length:
            fraction = target / length if length else 0
            glow(
                draw,
                (a[0] + (b[0] - a[0]) * fraction, a[1] + (b[1] - a[1]) * fraction),
                color,
                size,
            )
            return
        target -= length


def route(draw: ImageDraw.ImageDraw, points: list[Point], color: str = LINE) -> None:
    """Draw an architectural connection and compact terminal arrowhead."""
    polyline(draw, points, color, 1.6)
    a, b = points[-2:]
    angle = math.atan2(b[1] - a[1], b[0] - a[0])
    polyline(
        draw,
        [
            (b[0] - 7 * math.cos(angle - 0.5), b[1] - 7 * math.sin(angle - 0.5)),
            b,
            (b[0] - 7 * math.cos(angle + 0.5), b[1] - 7 * math.sin(angle + 0.5)),
        ],
        color,
        1.6,
    )


def foundation(project: str, *, mobile: bool) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    """Create the shared title, frame, and project-specific public footer."""
    metadata = {
        "quantum": (
            "Hybrid generative models",
            "Comparing classical and quantum priors.",
            "Binary MNIST / 3, 5, 7 qubits / FID + KID",
            VIOLET,
        ),
        "vision": (
            "Leaf object detection",
            "From annotated images to an exportable model.",
            "Single-class YOLO / validation / ONNX export",
            TEAL,
        ),
        "product": (
            "VeggieAI",
            "Image classification, connected to an app.",
            "Flask / model serving / prediction history",
            CORAL,
        ),
        "data": (
            "HDB resale analytics",
            "Clean records. Clearer housing decisions.",
            "Price / lease tenure / flat type / location",
            TEAL,
        ),
    }
    metadata.update(
        {
            "housing": (
                "EstateScope AI",
                "Property-price estimates from available inputs.",
                "US property-price prototype / Flask",
                VIOLET,
            ),
            "forecast": (
                "Energy Consumption Forecast",
                "Monthly utilities, modelled through time.",
                "Gas / electricity / water / ARIMA + SARIMAX",
                TEAL,
            ),
        }
    )
    width, height = MOBILE_SIZE if mobile else DESKTOP_SIZE
    image = Image.new("RGB", (width * SCALE, height * SCALE), NAVY)
    draw = ImageDraw.Draw(image)
    rect(draw, (0.5, 0.5, width - 0.5, height - 0.5), radius=18)
    title, subtitle, footer, accent = metadata[project]
    label(draw, (32 if mobile else 44, 26), title, 32 if mobile else 36, PAPER)
    label(draw, (32 if mobile else 45, 73), subtitle, 18 if mobile else 20, MUTED)
    if not mobile:
        label(draw, (1155, 41), "PROJECT WORKFLOW", 12, accent, anchor="rt")
    y = height - 48
    polyline(draw, [(32 if mobile else 44, y), (width - 32 if mobile else width - 44, y)], LINE)
    label(draw, (32 if mobile else 44, y + 17), footer, 14 if mobile else 16, accent)
    return image, draw


def circuit(draw: ImageDraw.ImageDraw, center: Point, *, width: float, height: float) -> None:
    """Draw a representative three-wire circuit with parametrised gates."""
    cx, cy = center
    for i in range(3):
        y = cy + (i - 1) * height / 3
        polyline(draw, [(cx - width / 2, y), (cx + width / 2, y)], mix(NAVY, VIOLET, 0.6), 1.2)
        for j in range(2):
            x = cx - width / 4 + j * width / 2
            rect(draw, (x - 10, y - 10, x + 10, y + 10), color=VIOLET, radius=3)
            label(draw, (x, y - 6), "R", 12, VIOLET, anchor="mt")
    polyline(draw, [(cx, cy - height / 3), (cx, cy + height / 3)], VIOLET, 1)
    circle(draw, (cx, cy - height / 3), 3, VIOLET)
    circle(draw, (cx, cy + height / 3), 6, VIOLET, fill=False)
    polyline(draw, [(cx - 6, cy + height / 3), (cx + 6, cy + height / 3)], VIOLET)


def generator(
    draw: ImageDraw.ImageDraw, center: Point, *, width: float = 170, height: float = 120
) -> None:
    """Draw the shared classical generator as a small connected network."""
    cx, cy = center
    rect(
        draw,
        (cx - width / 2, cy - height / 2, cx + width / 2, cy + height / 2),
        color=mix(NAVY, TEAL, 0.65),
    )
    layers = [
        [
            (cx + (layer - 1) * width * 0.26, cy + (node - (count - 1) / 2) * 18)
            for node in range(count)
        ]
        for layer, count in enumerate((3, 4, 3))
    ]
    for left, right in zip(layers[:-1], layers[1:], strict=True):
        for a in left:
            for b in right:
                polyline(draw, [a, b], mix(NAVY, TEAL, 0.3))
    for layer in layers:
        for point in layer:
            circle(draw, point, 4, TEAL)


def sample_tiles(draw: ImageDraw.ImageDraw, center: Point) -> None:
    """Draw abstract output tiles without presenting invented generated samples."""
    cx, cy = center
    for row in range(3):
        for column in range(3):
            x, y = cx + (column - 1) * 22, cy + (row - 1) * 22
            rect(
                draw,
                (x - 8, y - 8, x + 8, y + 8),
                color=mix(NAVY, PAPER, 0.6),
                radius=2,
                fill=mix(NAVY, PAPER, 0.07),
            )


def quantum_frame(progress: float, *, mobile: bool, static: bool) -> Image.Image:
    """Animate the alternative classical and quantum priors into one generator."""
    image, draw = foundation("quantum", mobile=mobile)
    if mobile:
        classical, quantum = (154, 226), (446, 226)
        gw, gh, gc = 190, 112, (300, 419)
        paths = [
            [(154, 310), (154, 419), (205, 419)],
            [(446, 310), (446, 419), (395, 419)],
        ]
        output = [(300, 475), (300, 500)]
        sample_center = (300, 543)
        label(draw, (154, 139), "CLASSICAL PRIOR", 16, TEAL, anchor="mt")
        label(draw, (446, 139), "QUANTUM PRIOR", 16, VIOLET, anchor="mt")
        label(draw, (446, 282), "3 / 5 / 7 qubits", 14, MUTED, anchor="mt")
        label(draw, (154, 282), "Latent distribution", 14, MUTED, anchor="mt")
        label(draw, (300, 339), "Classical GAN generator", 19, PAPER, anchor="mt")
        label(draw, (300, 589), "Generated images / FID + KID evaluation", 17, MUTED, anchor="mt")
    else:
        classical, quantum = (250, 186), (250, 290)
        gw, gh, gc = 190, 136, (750, 237)
        paths = [
            [(445, 219), (540, 219), (595, 237), (655, 237)],
            [(450, 290), (540, 290), (595, 237), (655, 237)],
        ]
        output = [(845, 237), (990, 237)]
        sample_center = (1050, 237)
        label(draw, (44, 120), "CLASSICAL PRIOR", 16, TEAL)
        label(draw, (44, 243), "QUANTUM PRIOR / 3, 5, 7 QUBITS", 16, VIOLET)
        label(draw, (750, 323), "Classical GAN generator", 18, PAPER, anchor="mt")
        label(draw, (1050, 304), "Generated images", 18, PAPER, anchor="mt")
        label(draw, (1050, 332), "FID + KID evaluation", 15, MUTED, anchor="mt")
    curve_width = 176 if mobile else 390
    cx, cy = classical
    curve = [
        (
            cx - curve_width / 2 + index * curve_width / 80,
            cy + 33 - math.exp(-(((index / 80 - 0.5) / 0.19) ** 2)) * 66,
        )
        for index in range(81)
    ]
    polyline(draw, [(cx - curve_width / 2, cy + 33), (cx + curve_width / 2, cy + 33)], LINE)
    polyline(draw, curve, TEAL, 2)
    circuit(draw, quantum, width=176 if mobile else 390, height=75 if mobile else 60)
    for path, color in zip(paths, (TEAL, VIOLET), strict=True):
        route(draw, path, mix(NAVY, color, 0.55))
        if not static:
            pulse(draw, path, progress * 3, color, size=4.2)
    generator(draw, gc, width=gw, height=gh)
    route(draw, output, mix(NAVY, CORAL, 0.65))
    sample_tiles(draw, sample_center)
    if not static:
        x = cx - curve_width / 2 + (progress * 3 % 1) * curve_width
        amount = ((progress * 3 % 1) - 0.5) / 0.19
        glow(draw, (x, cy + 33 - math.exp(-(amount**2)) * 66), TEAL, 3.5)
        for wire in range(3):
            pulse(
                draw,
                [
                    (
                        quantum[0] - (88 if mobile else 195),
                        quantum[1] + (wire - 1) * (25 if mobile else 20),
                    ),
                    (
                        quantum[0] + (88 if mobile else 195),
                        quantum[1] + (wire - 1) * (25 if mobile else 20),
                    ),
                ],
                progress * 3,
                VIOLET,
                size=3,
            )
        pulse(draw, output, progress * 3 - 0.4, CORAL)
        pulse(
            draw,
            [(gc[0] - 49, gc[1]), (gc[0], gc[1] - 25), (gc[0] + 49, gc[1])],
            progress * 3 - 0.22,
            TEAL,
            size=3.5,
        )
    return image


def leaf(
    draw: ImageDraw.ImageDraw, center: Point, size: float, angle: float, color: str = TEAL
) -> list[Point]:
    """Draw an original botanical silhouette, midrib, and branching veins."""
    cx, cy = center

    def transform(x: float, y: float) -> Point:
        return cx + (x * math.cos(angle) - y * math.sin(angle)) * size, cy + (
            x * math.sin(angle) + y * math.cos(angle)
        ) * size

    outline = []
    for side in (1, -1):
        values = range(33) if side == 1 else range(32, -1, -1)
        for index in values:
            t = index / 32
            outline.append(transform(math.sin(math.pi * t) * 0.38 * side, t * 2 - 1))
    polygon(draw, outline, mix(NAVY, color, 0.15))
    polyline(draw, [*outline, outline[0]], mix(NAVY, color, 0.85), 1.6)
    polyline(draw, [transform(0, -0.93), transform(0, 1.2)], color, 1.2)
    for y in (-0.55, -0.25, 0.05, 0.35, 0.6):
        for side in (-1, 1):
            polyline(
                draw,
                [transform(0, y + 0.14), transform(side * math.cos(y * 1.1) * 0.29, y - 0.15)],
                mix(NAVY, color, 0.55),
                0.8,
            )
    return outline


def detection_box(
    draw: ImageDraw.ImageDraw, bounds: tuple[float, float, float, float], strength: float
) -> None:
    """Draw leaf-class detection corners without invented confidence values."""
    x1, y1, x2, y2 = bounds
    color = mix(NAVY, CORAL, strength)
    for x, y, dx, dy in [(x1, y1, 1, 1), (x2, y1, -1, 1), (x1, y2, 1, -1), (x2, y2, -1, -1)]:
        polyline(draw, [(x, y + dy * 15), (x, y), (x + dx * 15, y)], color, 2)
    label(draw, (x1, y1 - 19), "leaf", 14, color)


def vision_frame(progress: float, *, mobile: bool, static: bool) -> Image.Image:
    """Scan illustrated leaves, reveal detections, then pulse through ONNX export."""
    image, draw = foundation("vision", mobile=mobile)
    frame = (32, 128, 568, 389) if mobile else (44, 128, 558, 340)
    rect(draw, frame, color=mix(NAVY, TEAL, 0.5), radius=12)
    for x in range(int(frame[0] + 24), int(frame[2]), 24):
        for y in range(int(frame[1] + 20), int(frame[3]), 24):
            circle(draw, (x, y), 0.6, mix(NAVY, MUTED, 0.25))
    shapes = (
        [((145, 264), 72, -0.37), ((326, 230), 74, 0.58), ((467, 298), 47, -0.2)]
        if mobile
        else [((145, 250), 62, -0.37), ((324, 215), 61, 0.58), ((466, 270), 44, -0.2)]
    )
    boxes = []
    for index, (center, size, angle) in enumerate(shapes):
        points = leaf(draw, center, size, angle, TEAL if index < 2 else VIOLET)
        boxes.append(
            (
                min(x for x, _ in points) - 9,
                min(y for _, y in points) - 10,
                max(x for x, _ in points) + 9,
                max(y for _, y in points) + 10,
            )
        )
    scan = frame[0] + 12 + (frame[2] - frame[0] - 24) * ((progress) % 1)
    for bounds in boxes:
        strength = 0.9 if static else 0.85 if scan >= (bounds[0] + bounds[2]) / 2 else 0.12
        detection_box(draw, bounds, strength)
    if not static:
        for offset, strength in [(-8, 0.06), (-4, 0.18), (0, 0.9)]:
            polyline(
                draw,
                [(scan + offset, frame[1] + 8), (scan + offset, frame[3] - 8)],
                mix(NAVY, TEAL, strength),
                1.5,
            )
    if mobile:
        yolo, onnx = (154, 500), (446, 500)
        input_path = [(300, 389), (300, 420), (154, 420), (154, 450)]
        route(draw, input_path, LINE)
        label(draw, (154, 570), "Single-class YOLO", 19, PAPER, anchor="mt")
        label(draw, (446, 570), "ONNX export", 19, PAPER, anchor="mt")
        output_path = [(214, 500), (386, 500)]
    else:
        yolo, onnx = (750, 230), (1050, 230)
        input_path = [(558, 230), (690, 230)]
        route(draw, input_path, LINE)
        label(draw, (750, 313), "Single-class YOLO", 20, PAPER, anchor="mt")
        label(draw, (1050, 313), "ONNX export", 20, PAPER, anchor="mt")
        output_path = [(810, 230), (990, 230)]
    for center, color in [(yolo, TEAL), (onnx, VIOLET)]:
        x, y = center
        rect(draw, (x - 60, y - 50, x + 60, y + 50), color=mix(NAVY, color, 0.7), radius=12)
    for row in range(3):
        for column in range(3):
            x, y = yolo[0] + (column - 1) * 23, yolo[1] + (row - 1) * 23
            rect(draw, (x - 8, y - 8, x + 8, y + 8), color=mix(NAVY, TEAL, 0.5), radius=2)
    detection_box(draw, (yolo[0] - 22, yolo[1] - 22, yolo[0] + 22, yolo[1] + 22), 1)
    label(draw, (onnx[0], onnx[1] - 12), "ONNX", 25, VIOLET, anchor="mt")
    route(draw, output_path, mix(NAVY, VIOLET, 0.65))
    if not static:
        pulse(draw, input_path, progress, TEAL)
        pulse(draw, output_path, progress - 0.4, VIOLET)
    return image


def database(
    draw: ImageDraw.ImageDraw, center: Point, *, width: float = 72, height: float = 60
) -> None:
    """Draw a database cylinder for the documented SQLite history store."""
    x, y = center
    rect(
        draw, (x - width / 2, y - height / 2, x + width / 2, y + height / 2), color=CORAL, radius=5
    )
    for offset in (-height / 2, 0, height / 2):
        draw.ellipse(
            tuple(
                round(value * SCALE)
                for value in (x - width / 2, y + offset - 6, x + width / 2, y + offset + 6)
            ),
            outline=CORAL,
            fill=NAVY if offset < 0 else None,
            width=2,
        )


def tomato(draw: ImageDraw.ImageDraw, center: Point, radius: float) -> None:
    """Draw an original tomato icon for the vegetable-classification application."""
    cx, cy = center
    body = [
        (
            cx + math.cos(index * math.pi / 32) * radius,
            cy + math.sin(index * math.pi / 32) * radius * 0.86,
        )
        for index in range(65)
    ]
    polygon(draw, body, mix(NAVY, CORAL, 0.16))
    polyline(draw, body, CORAL, 1.8)
    stem = []
    for index in range(10):
        angle = index * math.pi / 5 - math.pi / 2
        distance = radius * (0.52 if index % 2 == 0 else 0.18)
        stem.append(
            (cx + math.cos(angle) * distance, cy - radius * 0.66 + math.sin(angle) * distance * 0.7)
        )
    polygon(draw, stem, mix(NAVY, TEAL, 0.6))
    polyline(draw, [*stem, stem[0]], TEAL, 1)
    polyline(
        draw,
        [
            (cx - radius * 0.59, cy + radius * 0.1),
            (cx - radius * 0.52, cy - radius * 0.25),
            (cx - radius * 0.36, cy - radius * 0.42),
        ],
        mix(NAVY, PAPER, 0.65),
        1.4,
    )


def browser(draw: ImageDraw.ImageDraw, box: tuple[float, float, float, float]) -> None:
    """Draw a compact image-upload interface as a product architecture cue."""
    x1, y1, x2, y2 = box
    rect(draw, box, color=mix(NAVY, CORAL, 0.65), radius=12)
    polyline(draw, [(x1, y1 + 25), (x2, y1 + 25)], LINE)
    for index, color in enumerate((CORAL, VIOLET, TEAL)):
        circle(draw, (x1 + 15 + index * 13, y1 + 12), 3, color)
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2 + 15
    tomato(draw, (cx, cy - 6), 29)
    label(draw, (cx, y2 - 31), "Upload an image", 16, MUTED, anchor="mt")


def product_frame(progress: float, *, mobile: bool, static: bool) -> Image.Image:
    """Connect the app to alternative serving routes, predictions, and history."""
    image, draw = foundation("product", mobile=mobile)
    if mobile:
        browser_box = (32, 123, 568, 295)
        api, serving, prediction, history = (150, 402), (450, 402), (450, 555), (150, 555)
        paths = [
            ([(300, 295), (300, 328), (150, 328), (150, 357)], CORAL),
            ([(230, 402), (340, 402)], TEAL),
            ([(450, 447), (450, 512)], VIOLET),
            ([(150, 447), (150, 521)], CORAL),
        ]
        label_y = [0, 334, 600, 600]
        serving_width = 220
    else:
        browser_box = (44, 139, 334, 325)
        api, serving, prediction, history = (500, 209), (800, 209), (1080, 209), (800, 327)
        paths = [
            ([(334, 209), (420, 209)], CORAL),
            ([(580, 209), (690, 209)], TEAL),
            ([(910, 209), (1030, 209)], VIOLET),
            ([(500, 254), (500, 327), (764, 327)], CORAL),
        ]
        label_y = [0, 272, 272, 320]
        serving_width = 220
    browser(draw, browser_box)
    for path, color in paths:
        route(draw, path, mix(NAVY, color, 0.55))
    rect(draw, (api[0] - 80, api[1] - 45, api[0] + 80, api[1] + 45), color=CORAL)
    label(draw, (api[0], api[1] - 12), "Flask API", 23, CORAL, anchor="mt")
    rect(
        draw,
        (
            serving[0] - serving_width / 2,
            serving[1] - 45,
            serving[0] + serving_width / 2,
            serving[1] + 45,
        ),
        color=TEAL,
    )
    label(draw, (serving[0], serving[1] - 28), "Local service", 17, TEAL, anchor="mt")
    polyline(draw, [(serving[0] - 91, serving[1]), (serving[0] + 91, serving[1])], LINE)
    label(draw, (serving[0], serving[1] + 10), "TF Serving", 17, VIOLET, anchor="mt")
    for y in (-23, 23):
        circle(draw, (serving[0] - 94, serving[1] + y), 3, TEAL if y < 0 else VIOLET)
    rect(
        draw,
        (prediction[0] - 50, prediction[1] - 43, prediction[0] + 50, prediction[1] + 35),
        color=VIOLET,
    )
    tomato(draw, (prediction[0], prediction[1] - 4), 23)
    database(draw, history, height=52 if mobile else 40)
    for center, title, y in zip(
        (api, serving, prediction),
        ("Flask API", "Serving options", "Prediction"),
        label_y[:3],
        strict=True,
    ):
        if y:
            label(draw, (center[0], y), title, 18, PAPER, anchor="mt")
    label(
        draw,
        (history[0] if mobile else 859, label_y[3]),
        "SQLite history",
        18,
        PAPER,
        anchor="mt" if mobile else "lt",
    )
    if not static:
        for index, (path, color) in enumerate(paths):
            pulse(draw, path, progress * 3 - index * 0.2, color, size=4)
    return image


def building(
    draw: ImageDraw.ImageDraw, base: Point, width: float, height: float, color: str, highlight: int
) -> None:
    """Draw an isometric housing block with architectural window geometry."""
    x, y = base
    depth = width * 0.36
    front = [
        (x - width / 2, y),
        (x + width / 2, y + width * 0.22),
        (x + width / 2, y + width * 0.22 - height),
        (x - width / 2, y - height),
    ]
    side = [
        front[1],
        (x + width / 2 + depth, y + width * 0.22 - depth * 0.55),
        (x + width / 2 + depth, y + width * 0.22 - depth * 0.55 - height),
        front[2],
    ]
    top = [front[3], front[2], side[2], (x - width / 2 + depth, y - depth * 0.55 - height)]
    polygon(draw, front, mix(NAVY, color, 0.13))
    polygon(draw, side, mix(NAVY, color, 0.07))
    polygon(draw, top, mix(NAVY, color, 0.25))
    for face in (front, side, top):
        polyline(draw, [*face, face[0]], mix(NAVY, color, 0.6), 1)
    rows = max(3, int(height / 17))
    for row in range(rows):
        for column in range(3):
            wx = x - width / 2 + 10 + column * (width - 20) / 2
            wy = y - 13 - row * 15 + (wx - (x - width / 2)) * 0.22
            polygon(
                draw,
                [(wx, wy), (wx + 6, wy + 1.3), (wx + 6, wy - 4.7), (wx, wy - 6)],
                mix(NAVY, color, 0.85 if row == highlight % rows else 0.3),
            )


def records(draw: ImageDraw.ImageDraw, center: Point) -> None:
    """Draw a clean data-table stack without fabricated record values."""
    x, y = center
    for index in (2, 1, 0):
        dx, dy = index * 10, -index * 12
        rect(
            draw,
            (x - 88 + dx, y - 60 + dy, x + 88 + dx, y + 60 + dy),
            color=mix(NAVY, TEAL, 0.55),
            radius=7,
        )
    for row in range(5):
        yy = y - 39 + row * 21
        circle(draw, (x - 65, yy), 2, TEAL)
        for column in range(3):
            xx = x - 49 + column * 42
            polyline(draw, [(xx, yy), (xx + 27, yy)], mix(NAVY, MUTED, 0.55), 2)


def dashboard(
    draw: ImageDraw.ImageDraw, box: tuple[float, float, float, float], selected: int
) -> None:
    """Draw a Tableau-style housing view with dimensions rather than fake values."""
    x1, y1, x2, y2 = box
    rect(draw, box, color=mix(NAVY, VIOLET, 0.7), radius=10)
    label(draw, (x1 + 17, y1 + 14), "HOUSING EXPLORER", 13, VIOLET)
    polyline(draw, [(x1 + 15, y1 + 38), (x2 - 15, y1 + 38)], LINE)
    names = ["Price", "Lease", "Flat type", "Location"]
    for index, name in enumerate(names):
        yy = y1 + 55 + index * 26
        xx = x1 + (x2 - x1) * 0.59
        circle(draw, (xx - 11, yy + 6), 3, TEAL if index == selected else LINE)
        label(draw, (xx, yy), name, 16, TEAL if index == selected else MUTED)
    cx, cy = x1 + (x2 - x1) * 0.27, (y1 + y2) / 2 + 15
    for row in range(4):
        for column in range(4):
            if (row, column) in [(0, 0), (0, 3), (3, 0)]:
                continue
            xx, yy = cx + (column - 1.5) * 19, cy + (row - 1.5) * 19
            rect(
                draw,
                (xx - 6, yy - 6, xx + 6, yy + 6),
                color=mix(NAVY, TEAL, 0.7 if (column + row) % 4 == selected else 0.25),
                fill=mix(NAVY, TEAL, 0.13),
                radius=2,
            )


def data_frame(progress: float, *, mobile: bool, static: bool) -> Image.Image:
    """Move cleaned records through housing aggregation into exploratory views."""
    image, draw = foundation("data", mobile=mobile)
    selected = 2 if static else min(3, int(progress * 4))
    if mobile:
        record_center = (130, 228)
        buildings = [
            (360, 314, 62, 103, TEAL),
            (446, 282, 60, 138, VIOLET),
            (505, 327, 53, 77, CORAL),
        ]
        dashboard_box = (65, 425, 535, 606)
        feed_path = [(232, 228), (302, 228)]
        view_path = [(551, 330), (564, 330), (564, 510), (535, 510)]
        label(draw, (132, 320), "202,461", 25, PAPER, anchor="mt")
        label(draw, (132, 351), "cleaned records", 16, MUTED, anchor="mt")
        label(draw, (431, 350), "Aggregation", 18, PAPER, anchor="mt")
        label(draw, (300, 397), "Tableau views", 19, PAPER, anchor="mt")
    else:
        record_center = (152, 231)
        buildings = [
            (465, 301, 75, 130, TEAL),
            (574, 272, 72, 167, VIOLET),
            (661, 310, 65, 98, CORAL),
        ]
        dashboard_box = (866, 139, 1154, 320)
        feed_path = [(260, 231), (411, 231)]
        view_path = [(730, 231), (866, 231)]
        label(draw, (153, 321), "202,461 cleaned records", 18, PAPER, anchor="mt")
        label(draw, (574, 338), "Housing aggregation", 20, PAPER, anchor="mt")
        label(draw, (1010, 337), "Tableau views", 20, PAPER, anchor="mt")
    records(draw, record_center)
    for x, y, width, height, color in buildings:
        building(draw, (x, y), width, height, color, selected + int(progress * 10))
    route(draw, feed_path, mix(NAVY, TEAL, 0.55))
    route(draw, view_path, mix(NAVY, VIOLET, 0.6))
    dashboard(draw, dashboard_box, selected)
    if not static:
        for offset in (0, 0.33, 0.66):
            pulse(draw, feed_path, progress * 3 + offset, TEAL, size=3)
        pulse(draw, view_path, progress * 3 - 0.25, VIOLET)
    return image


def property_icon(
    draw: ImageDraw.ImageDraw, center: Point, size: float, color: str = VIOLET
) -> None:
    """Draw an original house outline for the property-price application."""
    x, y = center
    roof = [
        (x - size * 0.7, y - size * 0.05),
        (x, y - size * 0.65),
        (x + size * 0.7, y - size * 0.05),
    ]
    polyline(draw, roof, color, 1.7)
    polyline(
        draw,
        [
            (x - size * 0.51, y - size * 0.21),
            (x - size * 0.51, y + size * 0.6),
            (x + size * 0.51, y + size * 0.6),
            (x + size * 0.51, y - size * 0.21),
        ],
        color,
        1.7,
    )
    rect(
        draw,
        (x - size * 0.13, y + size * 0.14, x + size * 0.13, y + size * 0.6),
        color=color,
        radius=0,
    )
    for dx in (-0.32, 0.21):
        rect(
            draw,
            (x + size * dx, y - size * 0.05, x + size * (dx + 0.12), y + size * 0.1),
            color=color,
            radius=0,
        )


def modality_icon(draw: ImageDraw.ImageDraw, center: Point, kind: int, color: str) -> None:
    """Draw distinct structured-data, listing-text, and property-image symbols."""
    x, y = center
    rect(draw, (x - 29, y - 25, x + 29, y + 25), color=mix(NAVY, color, 0.65), radius=5)
    if kind == 0:
        for row in range(3):
            yy = y - 14 + row * 14
            circle(draw, (x - 18, yy), 2, color)
            polyline(draw, [(x - 8, yy), (x + 17, yy)], color, 1.5)
    elif kind == 1:
        for row in range(4):
            yy = y - 14 + row * 9
            polyline(draw, [(x - 17, yy), (x + 17 - (row % 3) * 6, yy)], color, 1.4)
    else:
        property_icon(draw, (x, y + 2), 23, color)
        circle(draw, (x + 18, y - 16), 3, color)


def housing_frame(progress: float, *, mobile: bool, static: bool) -> Image.Image:
    """Combine available tabular, optional text, and optional image estimates."""
    image, draw = foundation("housing", mobile=mobile)
    colors = (TEAL, VIOLET, CORAL)
    if mobile:
        centers = [(112, 208), (300, 208), (488, 208)]
        average = (300, 447)
        estimate = (300, 565)
        input_paths = [[(x, 266), (x, 292)] for x, _ in centers]
        average_paths = [
            [(112, 328), (112, 447), (170, 447)],
            [(300, 328), (300, 402)],
            [(488, 328), (488, 447), (430, 447)],
        ]
        output_path = [(300, 492), (300, 530)]
        for index, ((x, _y), color) in enumerate(zip(centers, colors, strict=True)):
            rect(draw, (x - 80, 132, x + 80, 266), color=mix(NAVY, color, 0.6))
            modality_icon(draw, (x, 173), index, color)
            label(
                draw,
                (x, 216),
                ("Structured", "Listing text", "Property image")[index],
                17,
                PAPER,
                anchor="mt",
            )
            label(
                draw, (x, 241), "attributes" if index == 0 else "Optional", 15, MUTED, anchor="mt"
            )
            rect(draw, (x - 42, 294, x + 42, 328), color=mix(NAVY, color, 0.6), radius=17)
            label(draw, (x, 304), "estimate", 15, color, anchor="mt")
    else:
        centers = [(204, 149), (204, 233), (204, 317)]
        average = (770, 233)
        estimate = (1050, 233)
        input_paths = [[(362, y), (456, y)] for _, y in centers]
        average_paths = [
            [(544, 149), (607, 149), (650, 233), (675, 233)],
            [(544, 233), (675, 233)],
            [(544, 317), (607, 317), (650, 233), (675, 233)],
        ]
        output_path = [(865, 233), (975, 233)]
        for index, ((_x, y), color) in enumerate(zip(centers, colors, strict=True)):
            rect(draw, (44, y - 32, 362, y + 32), color=mix(NAVY, color, 0.6))
            modality_icon(draw, (87, y), index, color)
            label(
                draw,
                (131, y - 17),
                ("Structured attributes", "Listing text", "Property image")[index],
                19,
                PAPER,
            )
            if index:
                label(draw, (131, y + 9), "Optional", 13, MUTED)
            rect(draw, (456, y - 17, 544, y + 17), color=mix(NAVY, color, 0.6), radius=17)
            label(draw, (500, y - 7), "estimate", 15, color, anchor="mt")
    for index, (input_path, average_path) in enumerate(
        zip(input_paths, average_paths, strict=True)
    ):
        route(draw, input_path, mix(NAVY, colors[index], 0.6))
        route(draw, average_path, mix(NAVY, colors[index], 0.6))
        if not static:
            pulse(draw, input_path, progress * 2 + index / 3, colors[index], size=3.5)
            pulse(draw, average_path, progress * 2 + index / 3 - 0.2, colors[index], size=3.5)
    ax, ay = average
    if mobile:
        rect(draw, (170, 402, 430, 492), color=mix(NAVY, VIOLET, 0.8))
        label(draw, (ax, ay - 22), "Available-input", 21, PAPER, anchor="mt")
        label(draw, (ax, ay + 8), "average", 23, VIOLET, anchor="mt")
    else:
        rect(draw, (675, 164, 865, 302), color=mix(NAVY, VIOLET, 0.8))
        for index, color in enumerate(colors):
            point = (ax - 34, ay - 42 + index * 17)
            circle(draw, point, 3.5, color)
            polyline(draw, [point, (ax + 25, ay - 25)], mix(NAVY, color, 0.5), 1.2)
        circle(draw, (ax + 25, ay - 25), 6, VIOLET, fill=False)
        label(draw, (ax, ay + 7), "Available-input", 19, PAPER, anchor="mt")
        label(draw, (ax, ay + 34), "average", 21, VIOLET, anchor="mt")
    route(draw, output_path, mix(NAVY, VIOLET, 0.6))
    if mobile:
        rect(draw, (190, 530, 410, 600), color=mix(NAVY, VIOLET, 0.75))
        property_icon(draw, (226, 562), 26)
        label(draw, (267, 556), "Price estimate", 18, PAPER)
    else:
        rect(draw, (975, 164, 1125, 302), color=mix(NAVY, VIOLET, 0.75))
        property_icon(draw, (estimate[0], estimate[1] - 8), 48)
        label(draw, (1050, 321), "Price estimate", 20, PAPER, anchor="mt")
    if not static:
        pulse(draw, output_path, progress * 2 - 0.4, VIOLET)
    return image


def utility_signal(t: float, kind: int) -> float:
    """Return a deterministic illustrative signal without measured data or units."""
    return (
        0.6 * math.sin(t * math.pi * 5 + kind * 0.8)
        + 0.22 * math.cos(t * math.pi * 11 + kind)
        + 0.12 * math.sin(t * math.pi * 19)
    )


def forecast_plot(
    draw: ImageDraw.ImageDraw,
    box: tuple[float, float, float, float],
    progress: float,
    *,
    static: bool,
) -> None:
    """Trace schematic history and future segments without confidence intervals."""
    x1, y1, x2, y2 = box
    rect(draw, box, color=mix(NAVY, TEAL, 0.65))
    boundary = x1 + (x2 - x1) * 0.43
    for y in range(round(y1 + 27), round(y2 - 10), 8):
        polyline(draw, [(boundary, y), (boundary, y + 4)], mix(NAVY, MUTED, 0.6), 0.8)
    label(draw, ((x1 + boundary) / 2, y1 + 9), "History", 12, MUTED, anchor="mt")
    label(draw, ((boundary + x2) / 2, y1 + 9), "Forecast", 12, TEAL, anchor="mt")
    for kind, color in enumerate((CORAL, TEAL, VIOLET)):
        center = y1 + 38 + kind * ((y2 - y1 - 52) / 2)
        amplitude = min(13, (y2 - y1) / 12)
        points = [
            (
                x1 + 12 + (x2 - x1 - 24) * index / 100,
                center - utility_signal(index / 100, kind) * amplitude,
            )
            for index in range(101)
        ]
        split = max(index for index, point in enumerate(points) if point[0] <= boundary)
        polyline(draw, points[: split + 1], mix(NAVY, color, 0.45), 1.2)
        limit = (
            len(points)
            if static
            else split + 2 + round((len(points) - split - 3) * (progress * 2 % 1))
        )
        polyline(draw, points[split:limit], color, 1.7)
        if not static:
            glow(draw, points[limit - 1], color, 2.5)


def validation_card(draw: ImageDraw.ImageDraw, box: tuple[float, float, float, float]) -> None:
    """Show time-order checks and a chronological training/test split."""
    x1, y1, x2, y2 = box
    rect(draw, box, color=mix(NAVY, TEAL, 0.65))
    label(draw, ((x1 + x2) / 2, y1 + 13), "Validate + split", 17, PAPER, anchor="mt")
    width = (x2 - x1 - 35) / 6
    y = (y1 + y2) / 2 + 3
    for index in range(6):
        x = x1 + 17 + width * index
        rect(
            draw,
            (x, y - 7, x + width - 4, y + 7),
            color=TEAL if index < 4 else VIOLET,
            fill=mix(NAVY, TEAL if index < 4 else VIOLET, 0.15),
            radius=2,
        )
    label(draw, (x1 + 17, y2 - 23), "Train", 13, TEAL)
    label(draw, (x2 - 17, y2 - 23), "Test", 13, VIOLET, anchor="rt")


def forecast_frame(progress: float, *, mobile: bool, static: bool) -> Image.Image:
    """Show validated monthly utilities entering independent ARIMA/SARIMAX models."""
    image, draw = foundation("forecast", mobile=mobile)
    colors = (CORAL, TEAL, VIOLET)
    names = ("Gas", "Electricity", "Water")
    if mobile:
        rows = [158, 208, 258]
        input_box = (32, 126, 568, 288)
        wave_start, wave_end = 192, 548
        validation = (32, 339, 242, 443)
        model_boxes = [(333, 316, 562, 356), (333, 375, 562, 415), (333, 434, 562, 474)]
        input_path = [(300, 288), (300, 308), (137, 308), (137, 339)]
        model_paths = [
            [(242, 391), (285, 391), (285, (box[1] + box[3]) / 2), (333, (box[1] + box[3]) / 2)]
            for box in model_boxes
        ]
        plot_box = (60, 522, 540, 610)
        output_paths = [
            [(562, (box[1] + box[3]) / 2), (580, (box[1] + box[3]) / 2), (580, 566), (540, 566)]
            for box in model_boxes
        ]
        label(draw, (300, 491), "Forecast each utility", 20, PAPER, anchor="mt")
    else:
        rows = [156, 230, 304]
        input_box = (44, 123, 352, 338)
        wave_start, wave_end = 147, 337
        validation = (419, 173, 604, 287)
        model_boxes = [(689, 134, 875, 178), (689, 208, 875, 252), (689, 282, 875, 326)]
        input_path = [(352, 230), (419, 230)]
        model_paths = [
            [(604, 230), (640, 230), (640, (box[1] + box[3]) / 2), (689, (box[1] + box[3]) / 2)]
            for box in model_boxes
        ]
        plot_box = (965, 140, 1156, 320)
        output_paths = [
            [(875, (box[1] + box[3]) / 2), (921, (box[1] + box[3]) / 2), (921, 230), (965, 230)]
            for box in model_boxes
        ]
        label(draw, (198, 345), "Monthly observations", 17, PAPER, anchor="mt")
        label(draw, (1060, 341), "Per-utility forecasts", 17, PAPER, anchor="mt")
    rect(draw, input_box, color=mix(NAVY, MUTED, 0.4))
    for kind, (y, name, color) in enumerate(zip(rows, names, colors, strict=True)):
        label(draw, (49 if mobile else 59, y - 7), name, 17 if mobile else 15, color)
        points = [
            (
                wave_start + (wave_end - wave_start) * index / 100,
                y - utility_signal(index / 100, kind) * 13,
            )
            for index in range(101)
        ]
        polyline(draw, points, mix(NAVY, color, 0.8), 1.5)
        if not static:
            glow(draw, points[round(progress * 2 % 1 * 100)], color, 2.8)
    route(draw, input_path, mix(NAVY, TEAL, 0.6))
    for path, color in zip(model_paths, colors, strict=True):
        route(draw, path, mix(NAVY, color, 0.5))
    for path, color in zip(output_paths, colors, strict=True):
        route(draw, path, mix(NAVY, color, 0.45))
    validation_card(draw, validation)
    for kind, (box, color, name) in enumerate(zip(model_boxes, colors, names, strict=True)):
        rect(draw, box, color=mix(NAVY, color, 0.7))
        label(
            draw,
            ((box[0] + box[2]) / 2, box[1] + 13),
            f"{name} / {'SARIMAX' if kind == 1 else 'ARIMA'}",
            16,
            color,
            anchor="mt",
        )
    forecast_plot(draw, plot_box, progress, static=static)
    if not static:
        pulse(draw, input_path, progress * 2, TEAL, size=3.5)
        for kind in range(3):
            pulse(draw, model_paths[kind], progress * 2 - kind * 0.1, colors[kind], size=3)
            pulse(draw, output_paths[kind], progress * 2 - 0.3 - kind * 0.1, colors[kind], size=3)
    return image


def render_frame(
    project: str, progress: float, *, mobile: bool = False, static: bool = False
) -> Image.Image:
    """Render one project card as RGB at the selected layout's native dimensions.

    Args:
        project: One of the documented PROJECTS keys.
        progress: Finite normalised loop position from zero to one.
        mobile: Whether to use the layout designed for a narrow screen.
        static: Whether to compose an explanatory still instead of moving packets.

    Returns:
        The antialiased RGB project illustration.

    Raises:
        ValueError: If the project key or normalised time is invalid.
    """
    if project not in PROJECTS:
        raise ValueError(f"project must be one of {PROJECTS}")
    if not math.isfinite(progress) or not 0 <= progress <= 1:
        raise ValueError("progress must be finite and within [0, 1]")
    renderer = {
        "quantum": quantum_frame,
        "vision": vision_frame,
        "product": product_frame,
        "data": data_frame,
        "housing": housing_frame,
        "forecast": forecast_frame,
    }[project]
    image = renderer(0.35 if static else progress, mobile=mobile, static=static)
    return image.resize(MOBILE_SIZE if mobile else DESKTOP_SIZE, Image.Resampling.LANCZOS)


def build(*, output: Path = ASSETS) -> dict[str, int]:
    """Generate six desktop/mobile GIF pairs with matching PNG fallbacks."""
    output.mkdir(parents=True, exist_ok=True)
    sizes: dict[str, int] = {}
    frame_count = FPS * LOOP_SECONDS
    durations = [
        round((index + 1) * 100 / FPS) * 10 - round(index * 100 / FPS) * 10
        for index in range(frame_count)
    ]
    for project in PROJECTS:
        for mobile in (False, True):
            stem = f"portfolio-{project}" + ("-mobile" if mobile else "")
            still = render_frame(project, 0.35, mobile=mobile, static=True)
            still.save(output / f"{stem}-static.png", optimize=True)
            palette = still.quantize(colors=128, method=Image.Quantize.MEDIANCUT)
            frames = [
                render_frame(project, index / frame_count, mobile=mobile).quantize(
                    palette=palette, dither=Image.Dither.NONE
                )
                for index in range(frame_count)
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
                name = f"{stem}{suffix}"
                sizes[name] = (output / name).stat().st_size
    return sizes


def main() -> None:
    """Build all assets or render one project frame for visual inspection."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ASSETS)
    parser.add_argument("--project", choices=PROJECTS, default="quantum")
    parser.add_argument("--frame", type=float)
    parser.add_argument("--mobile", action="store_true")
    parser.add_argument("--static", action="store_true")
    args = parser.parse_args()
    if args.frame is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        render_frame(args.project, args.frame, mobile=args.mobile, static=args.static).save(
            args.output
        )
    else:
        for name, size in build(output=args.output).items():
            print(f"{name}: {size:,} bytes")


if __name__ == "__main__":
    main()
