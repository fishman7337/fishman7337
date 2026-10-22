#!/usr/bin/env python3
"""Render evidence-grounded Newspaper Restoration and FitnessQuest scenes.

These schematic workflows show repository architecture. Example text and visual
progress markers are illustrations, not measured outcomes or real user data.
The master animation builder adds frame timing, encoding, and static fallbacks.
"""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path

from PIL import Image, ImageDraw

_HELPERS_PATH = Path(__file__).with_name("build_portfolio_animations.py")
_SPEC = importlib.util.spec_from_file_location("portfolio_scene_drawing", _HELPERS_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise ImportError(f"Cannot load drawing helpers: {_HELPERS_PATH}")
g = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(g)
SCALE = g.SCALE
DESKTOP_SIZE = (1200, 420)
MOBILE_SIZE = (600, 680)


def foundation(project: str, *, mobile: bool) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    """Create a titled portfolio canvas at the shared supersampling scale."""
    metadata = {
        "restoration": (
            "Newspaper restoration",
            "Recover damaged words with classical search.",
            "Tries / wildcard matching / edit distance / graph views",
            g.VIOLET,
        ),
        "fitness": (
            "FitnessQuest",
            "Authenticated challenges and game progression.",
            "Express / JWT / MySQL / profiles and challenges",
            g.CORAL,
        ),
    }
    width, height = MOBILE_SIZE if mobile else DESKTOP_SIZE
    title, subtitle, footer, accent = metadata[project]
    image = Image.new("RGB", (width * SCALE, height * SCALE), g.NAVY)
    draw = ImageDraw.Draw(image)
    g.rect(draw, (0.5, 0.5, width - 0.5, height - 0.5), radius=18)
    g.label(draw, (32 if mobile else 44, 26), title, 32 if mobile else 36, g.PAPER)
    g.label(draw, (32 if mobile else 45, 73), subtitle, 18 if mobile else 20, g.MUTED)
    if not mobile:
        g.label(draw, (1155, 41), "PROJECT WORKFLOW", 12, accent, anchor="rt")
    y = height - 48
    g.polyline(draw, [(32 if mobile else 44, y), (width - 32 if mobile else width - 44, y)], g.LINE)
    g.label(draw, (32 if mobile else 44, y + 17), footer, 13 if mobile else 16, accent)
    return image, draw


def damaged_text(draw: ImageDraw.ImageDraw, center: tuple[float, float]) -> None:
    """Draw a terminal-style damaged-word example with explicit wildcard input."""
    x, y = center
    g.rect(draw, (x - 118, y - 77, x + 118, y + 77), color=g.mix(g.NAVY, g.CORAL, 0.65))
    for index, color in enumerate((g.CORAL, g.VIOLET, g.TEAL)):
        g.circle(draw, (x - 98 + index * 13, y - 57), 3, color)
    g.label(draw, (x + 99, y - 63), "INPUT", 12, g.MUTED, anchor="rt")
    g.polyline(draw, [(x - 105, y - 38), (x + 105, y - 38)], g.LINE)
    g.label(draw, (x, y - 12), "news*aper", 30, g.PAPER, anchor="mt")
    g.label(draw, (x, y + 41), "damaged word", 17, g.CORAL, anchor="mt")


def trie(
    draw: ImageDraw.ImageDraw,
    center: tuple[float, float],
    progress: float,
    *,
    static: bool,
) -> None:
    """Illustrate shared prefixes and a branch during wildcard traversal."""
    x, y = center
    nodes = {
        "n": (x, y - 67),
        "e": (x, y - 27),
        "w": (x, y + 13),
        "s": (x - 41, y + 54),
        "t": (x + 41, y + 54),
        "p": (x - 41, y + 95),
    }
    edges = [("n", "e"), ("e", "w"), ("w", "s"), ("w", "t"), ("s", "p")]
    for start, end in edges:
        g.polyline(draw, [nodes[start], nodes[end]], g.mix(g.NAVY, g.VIOLET, 0.5), 1.4)
    active = 4 if static else min(4, int(progress * 5))
    route = ("n", "e", "w", "s", "p")
    for name, point in nodes.items():
        selected = name in route[: active + 1]
        g.circle(draw, point, 13, g.mix(g.NAVY, g.VIOLET, 0.23 if selected else 0.07))
        g.circle(draw, point, 13, g.VIOLET if selected else g.LINE, fill=False)
        g.label(
            draw, (point[0], point[1] - 8), name, 18, g.PAPER if selected else g.MUTED, anchor="mt"
        )
    if not static:
        points = [nodes[name] for name in route]
        g.pulse(draw, points, progress, g.VIOLET, size=3)


def candidates(
    draw: ImageDraw.ImageDraw,
    center: tuple[float, float],
    progress: float,
    *,
    static: bool,
) -> None:
    """Show a text candidate and edit operations without invented model scores."""
    x, y = center
    g.rect(draw, (x - 113, y - 73, x + 113, y + 73), color=g.mix(g.NAVY, g.TEAL, 0.6))
    g.label(draw, (x, y - 52), "Candidate matches", 18, g.TEAL, anchor="mt")
    g.polyline(draw, [(x - 95, y - 20), (x + 95, y - 20)], g.LINE)
    g.label(draw, (x, y - 3), "newspaper", 27, g.PAPER, anchor="mt")
    labels = ("insert", "delete", "replace")
    selected = 2 if static else min(2, int(progress * 3))
    for index, text in enumerate(labels):
        g.label(
            draw,
            (x + (index - 1) * 67, y + 43),
            text,
            14,
            g.TEAL if index == selected else g.MUTED,
            anchor="mt",
        )


def restored_text(draw: ImageDraw.ImageDraw, center: tuple[float, float]) -> None:
    """Draw candidate restored text as a document rather than a fabricated scan."""
    x, y = center
    g.rect(draw, (x - 84, y - 79, x + 84, y + 79), color=g.mix(g.NAVY, g.CORAL, 0.6), radius=6)
    g.label(draw, (x, y - 58), "RESTORED TEXT", 13, g.CORAL, anchor="mt")
    g.polyline(draw, [(x - 65, y - 30), (x + 65, y - 30)], g.LINE)
    for i, width in enumerate((103, 117, 82, 108)):
        yy = y - 8 + i * 19
        g.polyline(draw, [(x - 58, yy), (x - 58 + width, yy)], g.mix(g.NAVY, g.PAPER, 0.6), 2)
    g.polyline(draw, [(x + 39, y + 54), (x + 48, y + 61), (x + 65, y + 44)], g.TEAL, 2)


def restoration_frame(
    progress: float, *, mobile: bool = False, static: bool = False
) -> Image.Image:
    """Animate damaged input through trie search and edit-distance candidates.

    Returns a supersampled RGB scene for the master animation builder.
    """
    image, draw = foundation("restoration", mobile=mobile)
    if mobile:
        input_center, trie_center = (160, 228), (441, 202)
        candidate_center, result_center = (170, 501), (447, 502)
        paths = [
            ([(278, 228), (338, 228), (338, 175), (421, 175)], g.VIOLET),
            ([(400, 310), (375, 310), (375, 379), (170, 379), (170, 428)], g.TEAL),
            ([(283, 501), (361, 501)], g.CORAL),
        ]
        g.label(draw, (160, 324), "Wildcard input", 18, g.CORAL, anchor="mt")
        g.label(draw, (441, 324), "Prefix trie", 18, g.VIOLET, anchor="mt")
        g.label(draw, (170, 597), "Edit-distance search", 17, g.TEAL, anchor="mt")
        g.label(draw, (447, 597), "Candidate output", 17, g.CORAL, anchor="mt")
    else:
        input_center, trie_center = (162, 224), (453, 204)
        candidate_center, result_center = (756, 224), (1068, 224)
        paths = [
            ([(280, 224), (368, 224)], g.VIOLET),
            ([(516, 224), (641, 224)], g.TEAL),
            ([(869, 224), (982, 224)], g.CORAL),
        ]
        for x, title, color in (
            (162, "Wildcard input", g.CORAL),
            (453, "Prefix trie", g.VIOLET),
            (756, "Edit-distance search", g.TEAL),
            (1068, "Candidate output", g.CORAL),
        ):
            g.label(draw, (x, 331), title, 18, color, anchor="mt")
    for points, color in paths:
        g.route(draw, points, g.mix(g.NAVY, color, 0.5))
    damaged_text(draw, input_center)
    trie(draw, trie_center, progress, static=static)
    candidates(draw, candidate_center, progress, static=static)
    restored_text(draw, result_center)
    if not static:
        for index, (points, color) in enumerate(paths):
            g.pulse(draw, points, progress * 2 - index * 0.2, color)
    return image


def fitness_browser(
    draw: ImageDraw.ImageDraw,
    box: tuple[float, float, float, float],
    progress: float,
    *,
    static: bool,
) -> None:
    """Draw a public-facing browser interface with no invented user statistics."""
    x1, y1, x2, y2 = box
    g.rect(draw, box, color=g.mix(g.NAVY, g.CORAL, 0.65))
    for index in range(3):
        g.circle(draw, (x1 + 16 + index * 12, y1 + 15), 3, (g.CORAL, g.VIOLET, g.TEAL)[index])
    g.label(draw, (x1 + 65, y1 + 9), "FITNESSQUEST", 14, g.CORAL)
    g.polyline(draw, [(x1, y1 + 32), (x2, y1 + 32)], g.LINE)
    labels = ("Profile", "Challenges", "Game progress")
    active = 1 if static else min(2, int(progress * 3))
    for index, title in enumerate(labels):
        yy = y1 + 52 + index * 36
        color = g.TEAL if index == active else g.MUTED
        g.rect(draw, (x1 + 17, yy - 3, x2 - 17, yy + 24), color=g.mix(g.NAVY, color, 0.4), radius=5)
        g.circle(draw, (x1 + 33, yy + 10), 3, color)
        g.label(draw, (x1 + 47, yy + 1), title, 17, color)


def challenge_rules(draw: ImageDraw.ImageDraw, center: tuple[float, float]) -> None:
    """Draw challenge logic as checked tasks without invented activity counts."""
    x, y = center
    g.rect(draw, (x - 95, y - 45, x + 95, y + 45), color=g.TEAL)
    g.label(draw, (x, y - 26), "Challenges", 23, g.TEAL, anchor="mt")
    for i in range(3):
        xx = x + (i - 1) * 45
        g.rect(draw, (xx - 9, y + 9, xx + 9, y + 27), color=g.mix(g.NAVY, g.TEAL, 0.5), radius=3)
        g.polyline(draw, [(xx - 5, y + 18), (xx - 1, y + 22), (xx + 6, y + 14)], g.TEAL, 1.7)


def game_progress(
    draw: ImageDraw.ImageDraw,
    center: tuple[float, float],
    progress: float,
    *,
    static: bool,
) -> None:
    """Draw a game-path motif that represents progression without a numeric claim."""
    x, y = center
    radius = 41
    for index in range(40):
        angle = index * math.tau / 40
        point = (x + math.cos(angle) * radius, y + math.sin(angle) * radius)
        g.circle(draw, point, 1.4, g.mix(g.NAVY, g.VIOLET, 0.4))
    diamonds = [(x - 25, y + 15), (x, y - 16), (x + 25, y + 15)]
    g.polyline(draw, diamonds, g.mix(g.NAVY, g.VIOLET, 0.7), 2)
    active = 2 if static else min(2, int(progress * 3))
    for index, (xx, yy) in enumerate(diamonds):
        color = g.VIOLET if index <= active else g.LINE
        g.polygon(draw, [(xx, yy - 7), (xx + 7, yy), (xx, yy + 7), (xx - 7, yy)], color)
    if not static:
        angle = progress * math.tau - math.pi / 2
        g.glow(draw, (x + math.cos(angle) * radius, y + math.sin(angle) * radius), g.VIOLET, 3)


def fitness_frame(progress: float, *, mobile: bool = False, static: bool = False) -> Image.Image:
    """Animate browser requests through owned challenge actions and persisted state.

    Returns a supersampled RGB scene for the master animation builder.
    """
    image, draw = foundation("fitness", mobile=mobile)
    if mobile:
        browser_box = (54, 128, 546, 299)
        api, challenges, game, database = (150, 400), (450, 400), (450, 555), (150, 555)
        paths = [
            ([(300, 299), (300, 327), (150, 327), (150, 353)], g.CORAL),
            ([(230, 400), (353, 400)], g.TEAL),
            ([(450, 445), (450, 512)], g.VIOLET),
            ([(150, 447), (150, 527)], g.CORAL),
        ]
        g.label(draw, (150, 594), "MySQL state", 18, g.CORAL, anchor="mt")
        g.label(draw, (450, 609), "Game progression", 18, g.VIOLET, anchor="mt")
    else:
        browser_box = (44, 139, 334, 325)
        api, challenges, game, database = (500, 209), (800, 209), (1080, 209), (800, 327)
        paths = [
            ([(334, 209), (418, 209)], g.CORAL),
            ([(580, 209), (703, 209)], g.TEAL),
            ([(895, 209), (1036, 209)], g.VIOLET),
            ([(580, 232), (615, 232), (615, 327), (762, 327)], g.CORAL),
        ]
        g.label(draw, (500, 275), "JWT + ownership", 18, g.CORAL, anchor="mt")
        g.label(draw, (1080, 275), "Game progression", 18, g.VIOLET, anchor="mt")
        g.label(draw, (856, 322), "MySQL state", 18, g.CORAL)
    for points, color in paths:
        g.route(draw, points, g.mix(g.NAVY, color, 0.55))
    fitness_browser(draw, browser_box, progress, static=static)
    g.rect(draw, (api[0] - 80, api[1] - 45, api[0] + 80, api[1] + 45), color=g.CORAL)
    g.label(draw, (api[0], api[1] - 23), "Express API", 22, g.CORAL, anchor="mt")
    g.label(
        draw,
        (api[0], api[1] + 14),
        "JWT + ownership" if mobile else "Authorised actions",
        15,
        g.MUTED,
        anchor="mt",
    )
    challenge_rules(draw, challenges)
    game_progress(draw, game, progress, static=static)
    g.database(draw, database, height=52 if mobile else 40)
    if not static:
        for index, (points, color) in enumerate(paths):
            g.pulse(draw, points, progress * 3 - index * 0.2, color, size=4)
    return image
