"""Protect optional project motion and matching accessible fallbacks."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = (
    "quantum",
    "housing",
    "product",
    "data",
    "forecast",
    "student",
    "haiku",
    "restoration",
    "fitness",
    "pendulum",
)
STEMS = tuple(f"portfolio-{project}" for project in PROJECTS) + (
    "profile-hero",
    "process-applied",
    "process-research",
)


@pytest.mark.parametrize("stem", STEMS)
@pytest.mark.parametrize("suffix", ["", "-mobile"])
def test_animation_has_motion_and_matching_still(stem: str, suffix: str) -> None:
    """Check actual animation frames, safe pacing and a usable static composition."""
    with Image.open(ROOT / "assets" / f"{stem}{suffix}.gif") as gif:
        assert gif.is_animated
        assert gif.n_frames >= 40
        assert gif.info["loop"] == 0
        first = gif.convert("RGB")
        changed = False
        elapsed = 0
        for index in range(gif.n_frames):
            gif.seek(index)
            assert gif.info["duration"] >= 50
            elapsed += gif.info["duration"]
            changed |= ImageChops.difference(first, gif.convert("RGB")).getbbox() is not None
        assert changed
        assert 6_000 <= elapsed <= 12_000
        with Image.open(ROOT / "assets" / f"{stem}{suffix}-static.png") as still:
            assert still.size == gif.size
            assert not getattr(still, "is_animated", False)
        assert gif.width <= 600 if suffix else gif.width > 600


@pytest.mark.parametrize("project", PROJECTS)
def test_project_motion_is_optional_and_inside_its_portfolio_link(project: str) -> None:
    """Reduced-motion and unsupported clients must receive the static project view."""
    readme = (ROOT / "README.md").read_text()
    pictures = re.findall(
        r"<a\s+href=\"([^\"]+)\">\s*(<picture>.*?</picture>)\s*</a>", readme, re.S
    )
    matched = [(url, picture) for url, picture in pictures if f"portfolio-{project}.gif" in picture]
    assert len(matched) == 1
    url, picture = matched[0]
    assert url.startswith("https://github.com/fishman7337/")
    sources = re.findall(r"<source\b[^>]+>", picture)
    gif_sources = [source for source in sources if ".gif" in source]
    assert len(gif_sources) == 2
    assert all("prefers-reduced-motion: no-preference" in source for source in gif_sources)
    assert "max-width: 600px" in gif_sources[0]
    assert f"portfolio-{project}-mobile-static.png" in sources[-1]
    assert f'<img src="./assets/portfolio-{project}-static.png"' in picture


def test_every_readme_visual_supports_optional_desktop_and_mobile_motion() -> None:
    """No public visual should lose its motion option or accessible still fallback."""
    readme = (ROOT / "README.md").read_text()
    pictures = re.findall(r"<picture>.*?</picture>", readme, re.S)
    assert len(pictures) == len(STEMS)
    assert len(re.findall(r"<img\b", readme)) == len(pictures)
    for picture in pictures:
        gif_sources = [tag for tag in re.findall(r"<source\b[^>]+>", picture) if ".gif" in tag]
        assert len(gif_sources) == 2
        assert "-mobile.gif" in gif_sources[0]
        assert all("prefers-reduced-motion: no-preference" in tag for tag in gif_sources)
        assert re.search(r'<img src="[^"]+-static.png"', picture)
