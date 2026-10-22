#!/usr/bin/env python3
"""Generate public-facing animation cards for five additional portfolio projects.

The scenes illustrate documented methods and architecture. They do not display
student records, generated model results, measured usage, or performance claims.
"""

from __future__ import annotations

import argparse
import importlib.util
import math
from functools import lru_cache
from pathlib import Path
from types import ModuleType

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
PROJECTS = ("student", "haiku", "restoration", "fitness", "pendulum")
DESKTOP_SIZE = (1200, 420)
MOBILE_SIZE = (600, 680)
FPS = 12
LOOP_SECONDS = 8
SCALE = 2
Point = tuple[float, float]


@lru_cache(maxsize=2)
def load_sibling(name: str) -> ModuleType:
    """Load a renderer beside this file without relying on the caller's path.

    Args:
        name: Filename stem of the shared drawing or additional-scene module.

    Returns:
        The loaded sibling module, cached for subsequent frames.

    Raises:
        ImportError: If the sibling module cannot be loaded.
    """
    path = Path(__file__).with_name(f"{name}.py")
    spec = importlib.util.spec_from_file_location(f"portfolio_{name}", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load project renderer: {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


DRAW = load_sibling("build_portfolio_animations")
NAVY, PAPER, TEAL = DRAW.NAVY, DRAW.PAPER, DRAW.TEAL
CORAL, VIOLET, MUTED, LINE = DRAW.CORAL, DRAW.VIOLET, DRAW.MUTED, DRAW.LINE
label, polyline, circle, rect = DRAW.label, DRAW.polyline, DRAW.circle, DRAW.rect
mix, polygon, glow, route, pulse = DRAW.mix, DRAW.polygon, DRAW.glow, DRAW.route, DRAW.pulse


def foundation(project: str, *, mobile: bool) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    """Create a frame and title treatment matching the other project cards."""
    metadata = {
        "student": (
            "Student Performance Intelligence",
            "Latest-semester signals, transparent risk tiers.",
            "Dash / GPA + attendance rules / cohort exploration",
            TEAL,
        ),
        "haiku": (
            "HaikuForge AI",
            "Syllable-aware poetry, with a voice.",
            "Thesaurus / Markov chains / WAV narration",
            VIOLET,
        ),
    }
    metadata["pendulum"] = (
        "Pendulum Learning Lab",
        "Exploring deep Q-learning for pendulum control.",
        "Illustrated interaction loop / replay + target updates",
        CORAL,
    )
    width, height = MOBILE_SIZE if mobile else DESKTOP_SIZE
    image = Image.new("RGB", (width * SCALE, height * SCALE), NAVY)
    draw = ImageDraw.Draw(image)
    rect(draw, (0.5, 0.5, width - 0.5, height - 0.5), radius=18)
    title, subtitle, footer, accent = metadata[project]
    label(draw, (32 if mobile else 44, 26), title, 30 if mobile else 36)
    label(draw, (32 if mobile else 45, 73), subtitle, 18 if mobile else 20, MUTED)
    if not mobile:
        label(draw, (1155, 41), "PROJECT WORKFLOW", 12, accent, anchor="rt")
    y = height - 48
    polyline(draw, [(32 if mobile else 44, y), (width - 32 if mobile else width - 44, y)], LINE)
    label(draw, (32 if mobile else 44, y + 17), footer, 14 if mobile else 16, accent)
    return image, draw


def student_source(draw: ImageDraw.ImageDraw, center: Point, kind: int, *, mobile: bool) -> None:
    """Draw contextual profile, results, survey, and course data without records."""
    x, y = center
    width, height = (116, 94) if mobile else (117, 78)
    rect(
        draw,
        (x - width / 2, y - height / 2, x + width / 2, y + height / 2),
        color=mix(NAVY, TEAL if kind % 2 == 0 else VIOLET, 0.5),
    )
    if kind == 0:
        circle(draw, (x, y - 16), 7, TEAL, fill=False, width=1.5)
        polyline(
            draw,
            [(x - 14, y + 3), (x - 11, y - 3), (x, y - 7), (x + 11, y - 3), (x + 14, y + 3)],
            TEAL,
            1.5,
        )
    elif kind == 1:
        for index in range(3):
            yy = y - 23 + index * 11
            circle(draw, (x - 20, yy + 2), 2, VIOLET)
            polyline(draw, [(x - 10, yy + 2), (x + 19, yy + 2)], VIOLET, 1.4)
    elif kind == 2:
        for index in range(2):
            yy = y - 20 + index * 15
            rect(draw, (x - 23, yy - 3, x - 15, yy + 5), color=TEAL, radius=1)
            polyline(draw, [(x - 9, yy + 1), (x + 21, yy + 1)], TEAL, 1.3)
    else:
        polyline(draw, [(x, y - 26), (x, y + 2)], VIOLET, 1.4)
        for side in (-1, 1):
            points = [(x, y - 21), (x + side * 24, y - 25), (x + side * 24, y - 1), (x, y + 3)]
            polyline(draw, points, VIOLET, 1.4)
    label(
        draw,
        (x, y + 17 if mobile else y + 15),
        ("Profile", "Results", "Surveys", "Courses")[kind],
        16,
        PAPER,
        anchor="mt",
    )


def student_frame(progress: float, *, mobile: bool, static: bool) -> Image.Image:
    """Animate documented GPA/attendance rules into exploratory risk tiers."""
    image, draw = foundation("student", mobile=mobile)
    colors = (TEAL, VIOLET, CORAL)
    names = ("Low", "Medium", "High")
    conditions = ("Neither below", "One below", "Both below")
    if mobile:
        source_centers = [(90, 178), (230, 178), (370, 178), (510, 178)]
        rules = (110, 288, 490, 404)
        source_paths = [[(x, 225), (x, 259), (300, 259), (300, 288)] for x, _ in source_centers]
        tier_boxes = [(50, 457, 190, 527), (230, 457, 370, 527), (410, 457, 550, 527)]
        tier_paths = [
            [(300, 404), (300, 430), ((box[0] + box[2]) / 2, 430), ((box[0] + box[2]) / 2, 457)]
            for box in tier_boxes
        ]
        view_box = (32, 565, 568, 611)
        output_paths = [
            [((box[0] + box[2]) / 2, 527), ((box[0] + box[2]) / 2, 546), (300, 546), (300, 565)]
            for box in tier_boxes
        ]
    else:
        source_centers = [(110, 177), (257, 177), (110, 286), (257, 286)]
        rules = (423, 155, 689, 309)
        source_paths = [
            [(169, 177), (183, 177), (183, 231), (423, 231)],
            [(316, 177), (363, 177), (363, 231), (423, 231)],
            [(169, 286), (183, 286), (183, 231), (423, 231)],
            [(316, 286), (363, 286), (363, 231), (423, 231)],
        ]
        tier_boxes = [(782, 131, 901, 194), (782, 208, 901, 271), (782, 285, 901, 348)]
        tier_paths = [
            [(689, 231), (734, 231), (734, (box[1] + box[3]) / 2), (782, (box[1] + box[3]) / 2)]
            for box in tier_boxes
        ]
        view_box = (1000, 150, 1155, 320)
        output_paths = [
            [(901, (box[1] + box[3]) / 2), (945, (box[1] + box[3]) / 2), (945, 235), (1000, 235)]
            for box in tier_boxes
        ]
    for index, center in enumerate(source_centers):
        student_source(draw, center, index, mobile=mobile)
    for path in source_paths:
        route(draw, path, mix(NAVY, TEAL, 0.4))
    for path, color in zip(tier_paths, colors, strict=True):
        route(draw, path, mix(NAVY, color, 0.55))
    for path, color in zip(output_paths, colors, strict=True):
        route(draw, path, mix(NAVY, color, 0.45))
    x1, y1, x2, y2 = rules
    rect(draw, rules, color=mix(NAVY, TEAL, 0.75))
    label(draw, ((x1 + x2) / 2, y1 + 16), "Latest semester", 21, PAPER, anchor="mt")
    if mobile:
        label(draw, (x1 + 28, y1 + 53), "GPA", 18, TEAL)
        label(draw, (x1 + 28, y1 + 82), "Attendance", 18, VIOLET)
        label(draw, (x2 - 25, y1 + 57), "vs threshold", 16, MUTED, anchor="rt")
        label(draw, (x2 - 25, y1 + 86), "vs threshold", 16, MUTED, anchor="rt")
    else:
        label(draw, (x1 + 20, y1 + 58), "GPA", 18, TEAL)
        label(draw, (x1 + 20, y1 + 94), "Attendance", 18, VIOLET)
        label(draw, (x2 - 18, y1 + 61), "vs threshold", 14, MUTED, anchor="rt")
        label(draw, (x2 - 18, y1 + 98), "vs threshold", 14, MUTED, anchor="rt")
        label(draw, ((x1 + x2) / 2, 330), "Configured rules", 16, MUTED, anchor="mt")
    for box, name, condition, color in zip(tier_boxes, names, conditions, colors, strict=True):
        rect(draw, box, color=mix(NAVY, color, 0.8))
        x, y = (box[0] + box[2]) / 2, box[1]
        label(draw, (x, y + 13), name, 20, color, anchor="mt")
        label(draw, (x, y + 42), condition, 13, MUTED, anchor="mt")
    rect(draw, view_box, color=mix(NAVY, VIOLET, 0.65))
    selected = 1 if static else min(2, int(progress * 3))
    for index, text in enumerate(("Cohorts", "Trends", "Surveys")):
        if mobile:
            x, y = 118 + index * 182, 580
            label(draw, (x, y), text, 17, TEAL if selected == index else MUTED, anchor="mt")
        else:
            x, y = 1021, 191 + index * 44
            circle(draw, (x, y + 6), 3, TEAL if selected == index else LINE)
            label(draw, (x + 14, y), text, 17, TEAL if selected == index else MUTED)
    if not mobile:
        label(draw, (1077, 336), "Dash views", 18, PAPER, anchor="mt")
    if not static:
        for index, path in enumerate(source_paths):
            pulse(draw, path, progress * 2 + index / len(source_paths), TEAL, size=3)
        for index in range(3):
            pulse(draw, tier_paths[index], progress * 2 - index * 0.15, colors[index], size=3.5)
            pulse(
                draw, output_paths[index], progress * 2 - index * 0.15 - 0.35, colors[index], size=3
            )
    return image


def word(
    draw: ImageDraw.ImageDraw, center: Point, value: str, color: str, *, width: float = 108
) -> None:
    """Draw one word-state node in the illustrative Markov transition diagram."""
    x, y = center
    rect(
        draw, (x - width / 2, y - 20, x + width / 2, y + 20), color=mix(NAVY, color, 0.8), radius=20
    )
    label(draw, (x, y - 8), value, 18, color, anchor="mt")


def syllable_lines(
    draw: ImageDraw.ImageDraw,
    box: tuple[float, float, float, float],
    progress: float,
    *,
    mobile: bool,
    static: bool,
) -> None:
    """Fill a visible 5/7/5 syllable target without claiming guaranteed output."""
    x1, y1, x2, y2 = box
    rect(draw, box, color=mix(NAVY, VIOLET, 0.7))
    label(draw, ((x1 + x2) / 2, y1 + 17), "5 / 7 / 5 syllable target", 20, PAPER, anchor="mt")
    filled = 17 if static else min(17, int(progress * 21))
    count = 0
    for row, (target, color) in enumerate(zip((5, 7, 5), (TEAL, VIOLET, CORAL), strict=True)):
        y = y1 + 65 + row * (45 if mobile else 42)
        label(draw, (x1 + 30, y - 9), str(target), 20, color)
        spacing = 37 if mobile else 35
        start = x1 + 99
        for index in range(target):
            point = (start + index * spacing, y)
            lit = count < filled
            circle(draw, point, 8.5, mix(NAVY, color, 0.28 if lit else 0.06))
            circle(
                draw, point, 8.5, color if lit else mix(NAVY, color, 0.35), fill=False, width=1.2
            )
            if not static and count == max(0, filled - 1):
                glow(draw, point, color, 3)
            count += 1


def narration(
    draw: ImageDraw.ImageDraw,
    box: tuple[float, float, float, float],
    progress: float,
    *,
    static: bool,
) -> None:
    """Draw an illustrative moving audio waveform for word-level WAV narration."""
    x1, y1, x2, y2 = box
    rect(draw, box, color=mix(NAVY, CORAL, 0.5))
    cy = (y1 + y2) / 2
    polygon(draw, [(x1 + 17, cy - 7), (x1 + 17, cy + 7), (x1 + 29, cy)], CORAL)
    label(draw, (x1 + 43, cy - 6), "WAV", 13, CORAL)
    start, end = x1 + 91, x2 - 13
    cursor = start + (end - start) * (progress * 2 % 1)
    for index in range(60):
        x = start + index * (end - start) / 59
        amplitude = (
            (0.2 + 0.8 * abs(math.sin(index * 0.63) * math.sin(index * 0.17 + 0.4)))
            * (y2 - y1)
            * 0.32
        )
        emphasis = static or abs(x - cursor) < 27
        polyline(
            draw,
            [(x, cy - amplitude), (x, cy + amplitude)],
            CORAL if emphasis else mix(NAVY, CORAL, 0.3),
            1.4,
        )


def haiku_frame(progress: float, *, mobile: bool, static: bool) -> Image.Image:
    """Animate thesaurus words through Markov transitions and syllable/audio views."""
    image, draw = foundation("haiku", mobile=mobile)
    if mobile:
        source, transformed = (126, 190), (126, 267)
        nodes = [(367, 190), (505, 190), (436, 275)]
        target_box = (32, 349, 568, 533)
        audio_box = (32, 565, 568, 610)
        source_path = [(180, 267), (277, 267), (277, 190), (313, 190)]
        target_path = [(436, 295), (436, 326), (300, 326), (300, 349)]
        label(draw, (126, 132), "Thesaurus", 18, TEAL, anchor="mt")
        label(draw, (436, 132), "Markov transitions", 18, VIOLET, anchor="mt")
        label(draw, (300, 541), "Word-level narration", 15, MUTED, anchor="mt")
    else:
        source, transformed = (144, 184), (144, 284)
        nodes = [(410, 185), (579, 185), (495, 285)]
        target_box = (715, 130, 1155, 320)
        audio_box = (715, 332, 1155, 361)
        source_path = [(198, 284), (300, 284), (300, 185), (356, 185)]
        target_path = [(549, 285), (645, 285), (645, 226), (715, 226)]
        label(draw, (144, 128), "Thesaurus", 19, TEAL, anchor="mt")
        label(draw, (495, 128), "Markov transitions", 19, VIOLET, anchor="mt")
        label(draw, (495, 337), "Word-level WAV narration", 16, MUTED, anchor="mt")
    transform_path = [(source[0], source[1] + 20), (transformed[0], transformed[1] - 20)]
    routes = [
        [(nodes[0][0] + 54, nodes[0][1]), (nodes[1][0] - 54, nodes[1][1])],
        [(nodes[1][0], nodes[1][1] + 20), (nodes[2][0] + 27, nodes[2][1] - 20)],
        [(nodes[2][0] - 27, nodes[2][1] - 20), (nodes[0][0], nodes[0][1] + 20)],
    ]
    route(draw, transform_path, mix(NAVY, TEAL, 0.6))
    route(draw, source_path, mix(NAVY, TEAL, 0.6))
    route(draw, target_path, mix(NAVY, VIOLET, 0.6))
    for path in routes:
        route(draw, path, mix(NAVY, VIOLET, 0.6))
    word(draw, source, "rain", TEAL)
    word(draw, transformed, "drizzle", TEAL)
    for center, text in zip(nodes, ("drizzle", "falls", "softly"), strict=True):
        word(draw, center, text, VIOLET)
    syllable_lines(draw, target_box, progress, mobile=mobile, static=static)
    narration(draw, audio_box, progress, static=static)
    if not static:
        pulse(draw, transform_path, progress * 2, TEAL, size=3.3)
        pulse(draw, source_path, progress * 2 - 0.3, TEAL, size=3.5)
        for index, path in enumerate(routes):
            pulse(draw, path, progress * 2 - index / 3, VIOLET, size=3)
        pulse(draw, target_path, progress * 2 - 0.6, VIOLET, size=3.5)
    return image


def pendulum_environment(
    draw: ImageDraw.ImageDraw,
    box: tuple[float, float, float, float],
    progress: float,
    *,
    static: bool,
) -> None:
    """Draw periodic illustrative motion without simulating a learned policy."""
    x1, y1, x2, y2 = box
    rect(draw, box, color=mix(NAVY, CORAL, 0.6))
    label(draw, ((x1 + x2) / 2, y1 + 13), "Pendulum-v1", 18, PAPER, anchor="mt")
    cx, cy, length = (x1 + x2) / 2, y1 + 64, 90
    arc = [
        (
            cx + math.sin(-1.15 + index * 2.3 / 70) * length,
            cy + math.cos(-1.15 + index * 2.3 / 70) * length,
        )
        for index in range(71)
    ]
    polyline(draw, arc, mix(NAVY, CORAL, 0.22), 1)
    polyline(draw, [(cx - 29, cy - 15), (cx + 29, cy - 15)], MUTED, 2)
    polyline(draw, [(cx, cy - 15), (cx, cy)], MUTED, 1.5)
    for offset in (-0.045, -0.03, -0.015, 0):
        if static and offset:
            continue
        phase = progress + offset
        angle = 1.02 * math.sin(2 * math.pi * phase) + 0.12 * math.sin(4 * math.pi * phase)
        bob = (cx + math.sin(angle) * length, cy + math.cos(angle) * length)
        polyline(
            draw,
            [(cx, cy), bob],
            PAPER if offset == 0 else mix(NAVY, CORAL, 0.1),
            3 if offset == 0 else 1.5,
        )
        if offset == 0:
            glow(draw, bob, CORAL, 8)
    circle(draw, (cx, cy), 6, TEAL)
    circle(draw, (cx, cy), 2, PAPER)
    polyline(draw, [(x1 + 25, y2 - 17), (x2 - 25, y2 - 17)], LINE, 1)


def torque_icon(draw: ImageDraw.ImageDraw, center: Point, progress: float, *, static: bool) -> None:
    """Show two torque directions without implying a particular action-bin count."""
    x, y = center
    for index, color in enumerate((CORAL, VIOLET)):
        points = [
            (
                x
                + math.cos((-2.8 + step * 2.4 / 20) if index == 0 else (2.8 - step * 2.4 / 20))
                * 23,
                y
                + math.sin((-2.8 + step * 2.4 / 20) if index == 0 else (2.8 - step * 2.4 / 20))
                * 17,
            )
            for step in range(21)
        ]
        active = static or (math.cos(progress * 2 * math.pi) > 0) == (index == 0)
        route(draw, points, color if active else mix(NAVY, color, 0.3))
    circle(draw, center, 4, TEAL)


def replay_buffer(draw: ImageDraw.ImageDraw, box: tuple[float, float, float, float]) -> None:
    """Draw a small replay-memory queue without episode counts or reward values."""
    x1, y1, x2, y2 = box
    rect(draw, box, color=mix(NAVY, TEAL, 0.7))
    label(draw, ((x1 + x2) / 2, y1 + 12), "Experience replay", 17, TEAL, anchor="mt")
    for index in range(5):
        x = (x1 + x2) / 2 + (index - 2) * 21
        rect(draw, (x - 7, y2 - 17, x + 7, y2 - 8), color=mix(NAVY, TEAL, 0.7), radius=2)


def pendulum_frame(progress: float, *, mobile: bool, static: bool) -> Image.Image:
    """Illustrate DQN interaction, experience replay, and target-network updates."""
    image, draw = foundation("pendulum", mobile=mobile)
    if mobile:
        environment = (32, 122, 296, 327)
        state = (340, 137, 568, 222)
        network = (454, 320)
        memory = (32, 374, 256, 434)
        target = (32, 548, 256, 605)
        action = (340, 466, 568, 546)
        paths = [
            ([(296, 190), (340, 190)], TEAL),
            ([(454, 222), (454, 263)], TEAL),
            ([(454, 378), (454, 466)], VIOLET),
            ([(568, 506), (584, 506), (584, 620), (18, 620), (18, 225), (32, 225)], CORAL),
            ([(164, 327), (164, 374)], TEAL),
            ([(256, 404), (315, 404), (315, 320), (340, 320)], TEAL),
            ([(400, 378), (400, 443), (283, 443), (283, 576), (256, 576)], VIOLET),
        ]
        network_width = 228
    else:
        environment = (44, 130, 324, 333)
        state = (410, 145, 595, 225)
        network = (795, 202)
        memory = (410, 270, 600, 325)
        target = (695, 285, 895, 325)
        action = (1000, 145, 1155, 245)
        paths = [
            ([(324, 185), (410, 185)], TEAL),
            ([(595, 185), (690, 185)], TEAL),
            ([(900, 185), (1000, 185)], VIOLET),
            ([(1077, 245), (1077, 352), (184, 352), (184, 333)], CORAL),
            ([(502, 225), (502, 270)], TEAL),
            ([(600, 297), (650, 297), (650, 220), (690, 220)], TEAL),
            ([(795, 260), (795, 285)], VIOLET),
        ]
        network_width = 210
    for path, color in paths:
        route(draw, path, mix(NAVY, color, 0.5))
    pendulum_environment(draw, environment, progress, static=static)
    rect(draw, state, color=mix(NAVY, TEAL, 0.7))
    label(draw, ((state[0] + state[2]) / 2, state[1] + 14), "State", 22, TEAL, anchor="mt")
    label(
        draw,
        ((state[0] + state[2]) / 2, state[1] + 48),
        "Orientation + velocity",
        15 if mobile else 14,
        MUTED,
        anchor="mt",
    )
    DRAW.generator(draw, network, width=network_width, height=115)
    label(
        draw,
        (network[0], 353 if mobile else 120),
        "DQN variants",
        18 if mobile else 20,
        VIOLET,
        anchor="mt",
    )
    replay_buffer(draw, memory)
    rect(draw, target, color=mix(NAVY, VIOLET, 0.7))
    label(
        draw,
        ((target[0] + target[2]) / 2, target[1] + (20 if mobile else 12)),
        "Target network",
        18 if mobile else 17,
        VIOLET,
        anchor="mt",
    )
    rect(draw, action, color=mix(NAVY, CORAL, 0.7))
    torque_icon(draw, ((action[0] + action[2]) / 2, action[1] + 29), progress, static=static)
    label(
        draw,
        ((action[0] + action[2]) / 2, action[3] - 28),
        "Discrete torque",
        18,
        CORAL,
        anchor="mt",
    )
    if not static:
        for index, (path, color) in enumerate(paths):
            pulse(draw, path, progress * (1 if index == 3 else 2) - index * 0.13, color, size=3.2)
        pulse(
            draw,
            [
                (network[0] - 54, network[1]),
                (network[0], network[1] - 27),
                (network[0] + 54, network[1]),
            ],
            progress * 2 - 0.2,
            TEAL,
            size=3,
        )
    return image


def render_frame(
    project: str, progress: float, *, mobile: bool = False, static: bool = False
) -> Image.Image:
    """Render one RGB project card with strict project/time validation.

    Args:
        project: A key from PROJECTS.
        progress: Finite loop position between zero and one, inclusive.
        mobile: Whether to use the layout for narrow screens.
        static: Whether to render a complete explanatory still.

    Returns:
        The project illustration at its native output dimensions.

    Raises:
        ValueError: If the key or time is invalid.
    """
    if project not in PROJECTS:
        raise ValueError(f"project must be one of {PROJECTS}")
    if not math.isfinite(progress) or not 0 <= progress <= 1:
        raise ValueError("progress must be finite and within [0, 1]")
    if project in ("student", "haiku", "pendulum"):
        renderer = {"student": student_frame, "haiku": haiku_frame, "pendulum": pendulum_frame}[
            project
        ]
    else:
        module = load_sibling("additional_project_scenes")
        renderer = module.restoration_frame if project == "restoration" else module.fitness_frame
    image = renderer(0.35 if static else progress, mobile=mobile, static=static)
    return image.resize(MOBILE_SIZE if mobile else DESKTOP_SIZE, Image.Resampling.LANCZOS)


def build(*, output: Path = ASSETS) -> dict[str, int]:
    """Generate five desktop/mobile GIF pairs and reduced-motion PNG fallbacks."""
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
    """Build the five projects or render one selected frame for visual review."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ASSETS)
    parser.add_argument("--project", choices=PROJECTS, default="student")
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
