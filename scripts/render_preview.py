#!/usr/bin/env python3
"""Render a compact visual QA preview of the Curiosity Workshop assets."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw

try:
    import cairosvg
except (ImportError, OSError):
    cairosvg = None

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SCREENSHOTS = ROOT / "screenshots"
WIDTH = 1000
PADDING = 28
GAP = 24
BACKGROUND = "#0D1117"


def fit(image: Image.Image, width: int) -> Image.Image:
    """Resize an image to the requested width without changing its aspect ratio."""
    height = round(image.height * (width / image.width))
    return image.resize((width, height), Image.Resampling.LANCZOS)


def render_svg(path: Path, width: int) -> Image.Image:
    """Render one SVG to a Pillow image for visual inspection."""
    if cairosvg is None:
        raise RuntimeError("CairoSVG is unavailable; use preview/visual-gallery.html")
    png = cairosvg.svg2png(url=str(path), output_width=width)
    return Image.open(BytesIO(png)).convert("RGB")


def main() -> None:
    """Build the vertical README visual preview."""
    if cairosvg is None:
        print("Cairo is unavailable; open preview/visual-gallery.html in a browser instead.")
        return
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    inner_width = WIDTH - PADDING * 2
    images = [
        render_svg(ASSETS / "hero-curiosity-workshop.svg", inner_width),
        render_svg(ASSETS / "workbench-now.svg", inner_width),
        render_svg(ASSETS / "project-cabinet.svg", inner_width),
        render_svg(ASSETS / "making-machine.svg", inner_width),
        render_svg(ASSETS / "current-curiosities.svg", inner_width),
        render_svg(ASSETS / "workshop-footer.svg", inner_width),
    ]
    height = PADDING * 2 + sum(image.height for image in images) + GAP * (len(images) - 1)
    canvas = Image.new("RGB", (WIDTH, height), BACKGROUND)
    draw = ImageDraw.Draw(canvas)
    y = PADDING
    for image in images:
        canvas.paste(image, (PADDING, y))
        y += image.height + GAP
    draw.rounded_rectangle((8, 8, WIDTH - 9, height - 9), radius=22, outline="#30363D", width=2)
    destination = SCREENSHOTS / "curiosity-workshop-preview.png"
    canvas.save(destination, optimize=True)
    print(f"wrote {destination}")


if __name__ == "__main__":
    main()
