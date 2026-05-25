#!/usr/bin/env python3
"""Render static QA screenshots for the editable SVG profile README.

Usage:
  python scripts/render_preview.py

This script avoids browser automation. It rasterizes local SVGs with CairoSVG and builds
preview sheets with Pillow, which makes it easy to spot overlapping text before pushing.
"""
from __future__ import annotations

from pathlib import Path
import json
import zipfile

try:
    import cairosvg
    CAIRO_ERROR = None
except (ImportError, OSError) as exc:
    cairosvg = None
    CAIRO_ERROR = exc

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:
    raise SystemExit("Missing preview dependency. Install it with: pip install pillow") from exc

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SCREENSHOTS = ROOT / "screenshots"
SCREENSHOTS.mkdir(exist_ok=True)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = (
        ["C:/Windows/Fonts/seguibd.ttf", "C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
        if bold
        else ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    )
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT_BIG = load_font(34, bold=True)
FONT_MED = load_font(22, bold=True)
FONT_SMALL = load_font(15)

BG = (13, 17, 23)
PANEL = (22, 27, 34)
FG = (230, 237, 243)
MUTED = (139, 148, 158)
BORDER = (48, 54, 61)
CYAN = (56, 189, 248)
PINK = (244, 114, 182)
GREEN = (52, 211, 153)
AMBER = (251, 191, 36)


def fit(path: Path, width: int) -> Image.Image:
    img = Image.open(path).convert("RGB")
    height = int(img.height * width / img.width)
    return img.resize((width, height), Image.LANCZOS)


def badge(text: str, color: tuple[int, int, int]) -> Image.Image:
    dummy = Image.new("RGB", (10, 10), BG)
    draw = ImageDraw.Draw(dummy)
    bbox = draw.textbbox((0, 0), text, font=FONT_SMALL)
    width = bbox[2] - bbox[0] + 36
    img = Image.new("RGB", (width, 34), BG)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([0, 0, width - 1, 33], radius=17, fill=PANEL, outline=color, width=1)
    draw.ellipse([12, 13, 20, 21], fill=color)
    draw.text((27, 8), text, font=FONT_SMALL, fill=FG)
    return img


def render_svgs() -> list[tuple[str, Path]]:
    rendered: list[tuple[str, Path]] = []
    for svg in sorted(ASSETS.glob("*.svg")):
        out = SCREENSHOTS / f"{svg.stem}.png"
        if cairosvg is not None:
            cairosvg.svg2png(url=str(svg), write_to=str(out), output_width=1200)
        elif not out.exists():
            raise SystemExit(
                "CairoSVG is installed but cannot load native Cairo on this machine. "
                "Create screenshots with Playwright first, then rerun this script. "
                f"Original error: {CAIRO_ERROR}"
            )
        rendered.append((svg.name, out))
    return rendered


def make_top_preview() -> None:
    width = 1280
    inner = 1160
    hero = fit(SCREENSHOTS / "hero-cyberdeck.png", inner)
    mission = fit(SCREENSHOTS / "mission-control.png", inner)
    badges = [
        badge("GitHub · fishman7337", CYAN),
        badge("LinkedIn · Goh Kun Ming", PINK),
        badge("Email · kunmingaden@gmail.com", GREEN),
        badge("arXiv · 2508.09209", AMBER),
    ]
    row = Image.new("RGB", (inner, 54), BG)
    x = (inner - sum(b.width for b in badges) - 12 * (len(badges) - 1)) // 2
    for item in badges:
        row.paste(item, (x, 10))
        x += item.width + 12
    nav = Image.new("RGB", (inner, 44), BG)
    draw = ImageDraw.Draw(nav)
    text = "Mission Control · Research Spotlight · Project Nebula · Technical Stack · GitHub Telemetry · Contact"
    bbox = draw.textbbox((0, 0), text, font=FONT_SMALL)
    draw.text(((inner - (bbox[2] - bbox[0])) // 2, 10), text, font=FONT_SMALL, fill=MUTED)

    height = 40 + hero.height + 16 + row.height + nav.height + 26 + mission.height + 40
    canvas = Image.new("RGB", (width, height), BG)
    y = 40
    canvas.paste(hero, ((width - inner) // 2, y))
    y += hero.height + 16
    canvas.paste(row, ((width - inner) // 2, y))
    y += row.height
    canvas.paste(nav, ((width - inner) // 2, y))
    y += nav.height + 26
    canvas.paste(mission, ((width - inner) // 2, y))
    canvas.save(SCREENSHOTS / "github-style-top-preview.png", quality=95)


def make_contact_sheet(rendered: list[tuple[str, Path]]) -> None:
    thumbs = []
    for name, png in rendered:
        img = fit(png, 560)
        if img.height > 270:
            img = img.resize((int(img.width * 270 / img.height), 270), Image.LANCZOS)
        tile = Image.new("RGB", (610, 350), (5, 8, 22))
        draw = ImageDraw.Draw(tile)
        draw.text((22, 16), name, font=FONT_MED, fill=FG)
        draw.line((22, 48, 588, 48), fill=BORDER)
        tile.paste(img, ((610 - img.width) // 2, 70))
        thumbs.append(tile)
    cols = 2
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 610, rows * 350), (3, 7, 18))
    for i, tile in enumerate(thumbs):
        sheet.paste(tile, ((i % cols) * 610, (i // cols) * 350))
    sheet.save(SCREENSHOTS / "svg-contact-sheet.png", quality=95)


def make_visual_gallery() -> None:
    width = 1280
    inner = 1160
    sections = [
        ("Hero", SCREENSHOTS / "hero-cyberdeck.png"),
        ("Mission Control", SCREENSHOTS / "mission-control.png"),
        ("HQCGAN Lab", SCREENSHOTS / "quantum-lab.png"),
        ("Project Nebula", SCREENSHOTS / "project-nebula.png"),
        ("Technical Stack", SCREENSHOTS / "skill-constellation.png"),
        ("Timeline Roadmap", SCREENSHOTS / "timeline-roadmap.png"),
        ("Terminal Lab", SCREENSHOTS / "terminal-lab.png"),
        ("Footer Wave", SCREENSHOTS / "footer-wave.png"),
    ]
    parts = []
    for title, png in sections:
        img = fit(png, inner)
        header = Image.new("RGB", (inner, 60), BG)
        draw = ImageDraw.Draw(header)
        draw.text((0, 13), title, font=FONT_MED, fill=FG)
        draw.line((0, 50, inner, 50), fill=BORDER)
        parts.extend([header, img])
    height = 40 + sum(part.height for part in parts) + 24 * len(sections) + 60
    canvas = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(canvas)
    draw.text((60, 26), "fishman7337 Profile README Visual QA", font=FONT_BIG, fill=FG)
    y = 86
    for i in range(0, len(parts), 2):
        canvas.paste(parts[i], ((width - inner) // 2, y))
        y += parts[i].height
        canvas.paste(parts[i + 1], ((width - inner) // 2, y))
        y += parts[i + 1].height + 24
    draw.text((60, y), "Static screenshot preview generated from local editable SVGs. Animations render live in GitHub-compatible SVG images.", font=FONT_SMALL, fill=MUTED)
    canvas.save(SCREENSHOTS / "visual-gallery-screenshot.png", quality=95)


def main() -> None:
    rendered = render_svgs()
    make_top_preview()
    make_contact_sheet(rendered)
    make_visual_gallery()
    manifest = {
        "name": "fishman7337-profile-readme-cyberdeck",
        "username": "fishman7337",
        "editable_source": "content/profile.yml",
        "generated_assets": sorted(p.name for p in ASSETS.glob("*.svg")),
        "screenshots": sorted(p.name for p in SCREENSHOTS.glob("*")),
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Rendered screenshots to {SCREENSHOTS}")


if __name__ == "__main__":
    main()
