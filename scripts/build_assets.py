#!/usr/bin/env python3
"""Generate the responsive Spatial Portfolio SVG assets."""

from __future__ import annotations

import base64
import html
import textwrap
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SOURCE_ASSETS = ROOT / "assets"
PROFILE = yaml.safe_load((ROOT / "content" / "profile.yml").read_text(encoding="utf-8"))
IDENTITY = PROFILE["identity"]
THEME = PROFILE["theme"]


def esc(value: object) -> str:
    """Escape a value for safe SVG insertion."""
    return html.escape(str(value), quote=True)


def wrap(value: str, width: int) -> list[str]:
    """Wrap a short sentence without splitting words."""
    return textwrap.wrap(value, width=width, break_long_words=False, break_on_hyphens=False)


def ellipsize(value: str, limit: int) -> str:
    """Bound text to a deterministic character count."""
    return value if len(value) <= limit else f"{value[: limit - 1].rstrip()}…"


def image_data(filename: str) -> str:
    """Return a checked-in PNG as a self-contained data URI."""
    payload = base64.b64encode((SOURCE_ASSETS / filename).read_bytes()).decode("ascii")
    return f"data:image/png;base64,{payload}"


def defs() -> str:
    """Return the shared spatial-portfolio gradients, filters, and motion."""
    return f"""
<defs>
  <linearGradient id="signal" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{THEME["cyan"]}"/>
    <stop offset=".52" stop-color="{THEME["purple"]}"/>
    <stop offset="1" stop-color="{THEME["coral"]}"/>
  </linearGradient>
  <linearGradient id="copper" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#F0B07F"/>
    <stop offset=".5" stop-color="#D37A4C"/>
    <stop offset="1" stop-color="#7A3F30"/>
  </linearGradient>
  <radialGradient id="vignette">
    <stop offset="55%" stop-color="#050814" stop-opacity="0"/>
    <stop offset="100%" stop-color="#02040A" stop-opacity=".72"/>
  </radialGradient>
  <pattern id="microGrid" width="36" height="36" patternUnits="userSpaceOnUse">
    <path d="M36 0H0V36" fill="none" stroke="#EAF4FF" stroke-opacity=".035"/>
  </pattern>
  <filter id="glow" x="-150%" y="-150%" width="400%" height="400%">
    <feGaussianBlur stdDeviation="6" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="soft" x="-30%" y="-30%" width="160%" height="160%">
    <feDropShadow dx="0" dy="14" stdDeviation="18" flood-color="#00030A" flood-opacity=".72"/>
  </filter>
  <style><![CDATA[
    .display{{font:800 61px Inter,Segoe UI,Arial,sans-serif;fill:#FFF9EF;letter-spacing:-2.2px}}
    .mobileDisplay{{font:800 67px Inter,Segoe UI,Arial,sans-serif;fill:#FFF9EF;letter-spacing:-2px}}
    .role{{font:720 27px Inter,Segoe UI,Arial,sans-serif;fill:#E8E4F3;letter-spacing:-.35px}}
    .body{{font:520 20px Inter,Segoe UI,Arial,sans-serif;fill:#C9C6D4}}
    .mobileBody{{font:520 28px Inter,Segoe UI,Arial,sans-serif;fill:#C9C6D4}}
    .mono{{font:700 13px 'JetBrains Mono',Consolas,monospace;fill:#F3EBDD;letter-spacing:1.8px}}
    .wire{{fill:none;stroke:url(#signal);stroke-linecap:round;stroke-linejoin:round}}
    .dash{{stroke-dasharray:9 15;animation:dash 16s linear infinite}}
    .draw{{stroke-dasharray:420;animation:draw 8s ease-in-out infinite}}
    .orbit{{animation:orbit 17s linear infinite;transform-box:fill-box;transform-origin:center}}
    .orbitReverse{{animation:orbitReverse 24s linear infinite;transform-box:fill-box;transform-origin:center}}
    .float{{animation:float 7s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
    .pulse{{animation:pulse 3.4s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
    .scan{{animation:scan 7.5s ease-in-out infinite}}
    @keyframes dash{{to{{stroke-dashoffset:-480}}}}
    @keyframes draw{{0%,100%{{stroke-dashoffset:420;opacity:.15}}50%{{stroke-dashoffset:0;opacity:.82}}}}
    @keyframes orbit{{to{{transform:rotate(360deg)}}}}
    @keyframes orbitReverse{{to{{transform:rotate(-360deg)}}}}
    @keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-10px)}}}}
    @keyframes pulse{{0%,100%{{opacity:.45;transform:scale(.86)}}50%{{opacity:1;transform:scale(1.12)}}}}
    @keyframes scan{{0%,100%{{transform:translateX(-26%);opacity:0}}45%,55%{{opacity:.32}}50%{{transform:translateX(126%)}}}}
    @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
  ]]></style>
</defs>"""


def svg_open(title: str, description: str, width: int, height: int) -> str:
    """Open one accessible SVG document."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">'
        f'<title id="title">{esc(title)}</title><desc id="desc">{esc(description)}</desc>{defs()}'
    )


def image_layer(filename: str, width: int, height: int, anchor: str = "xMidYMid") -> str:
    """Embed a generated scene with a consistent crop."""
    return (
        f'<image href="{image_data(filename)}" width="{width}" height="{height}" '
        f'preserveAspectRatio="{anchor} slice"/>'
    )


def frame(width: int, height: int, radius: int = 28) -> str:
    """Draw the shared gallery frame, vignette, and corner marks."""
    return "".join(
        [
            f'<rect width="{width}" height="{height}" fill="url(#microGrid)"/>',
            f'<rect width="{width}" height="{height}" fill="url(#vignette)"/>',
            f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="{radius}" '
            'fill="none" stroke="#E9F3FF" stroke-opacity=".16"/>',
            '<path d="M30 76V30H76M1124 30h46v46" fill="none" stroke="#F3EBDD" '
            'stroke-opacity=".36" stroke-width="2"/>',
            f'<path d="M30 {height - 76}v46h46M{width - 76} {height - 30}h46v-46" '
            'fill="none" stroke="#F3EBDD" stroke-opacity=".22" stroke-width="2"/>',
        ]
    )


def text_lines(lines: list[str], *, x: int, y: int, line_height: int, css_class: str) -> str:
    """Render wrapped text as individually positioned SVG text nodes."""
    return "".join(
        f'<text x="{x}" y="{y + index * line_height}" class="{css_class}">{esc(line)}</text>'
        for index, line in enumerate(lines)
    )


def make_hero() -> str:
    """Build the desktop spatial-portfolio identity hero."""
    return "".join(
        [
            svg_open(
                f"{IDENTITY['name']} · Spatial Portfolio",
                "A cinematic glass-and-mesh installation representing applied AI, analytics, and product craft.",
                1200,
                470,
            ),
            image_layer("spatial-portfolio-hero-v1.png", 1200, 470, "xMidYMid"),
            '<linearGradient id="heroShade" x1="0" y1="0" x2=".72" y2="0">'
            '<stop offset="0" stop-color="#03050C" stop-opacity=".99"/>'
            '<stop offset=".54" stop-color="#050814" stop-opacity=".9"/>'
            '<stop offset=".84" stop-color="#050814" stop-opacity=".08"/>'
            '<stop offset="1" stop-color="#050814" stop-opacity="0"/></linearGradient>',
            '<rect width="1200" height="470" fill="url(#heroShade)"/>',
            '<g transform="translate(56 48)">',
            '<circle cx="7" cy="7" r="6" fill="#63D9D1" class="pulse" filter="url(#glow)"/>',
            '<text x="27" y="12" class="mono">SPATIAL PORTFOLIO / SINGAPORE</text>',
            f'<text x="0" y="112" class="display">{esc(IDENTITY["name"])}</text>',
            f'<text x="2" y="156" class="role">{esc(IDENTITY["role"])}</text>',
            text_lines(wrap(IDENTITY["tagline"], 36), x=2, y=213, line_height=30, css_class="body"),
            '<path d="M2 300C118 246 232 344 382 282" class="wire dash" stroke-width="2" opacity=".85"/>',
            '<circle cx="2" cy="300" r="5" fill="#63D9D1" class="pulse" filter="url(#glow)"/>',
            '<circle cx="382" cy="282" r="5" fill="#FF9B7A" class="pulse" filter="url(#glow)"/>',
            '<text x="2" y="352" class="mono">MODELS · DATA · PRODUCTS · DELIVERY</text>',
            "</g>",
            '<g class="orbit" opacity=".72"><ellipse cx="872" cy="222" rx="258" ry="104" '
            'fill="none" stroke="url(#signal)" stroke-width="1.5" stroke-dasharray="5 14"/></g>',
            frame(1200, 470),
            "</svg>",
        ]
    )


def make_mobile_hero() -> str:
    """Build a portrait hero with typography sized for narrow GitHub layouts."""
    return "".join(
        [
            svg_open(
                f"{IDENTITY['name']} · Spatial Portfolio",
                "A mobile introduction above a cinematic glass-and-mesh AI installation.",
                760,
                820,
            ),
            '<rect width="760" height="820" rx="34" fill="#050814"/>',
            '<g transform="translate(46 48)">',
            '<circle cx="8" cy="8" r="7" fill="#63D9D1" class="pulse" filter="url(#glow)"/>',
            '<text x="32" y="14" class="mono" font-size="17">SPATIAL PORTFOLIO / SINGAPORE</text>',
            f'<text x="0" y="119" class="mobileDisplay">{esc(IDENTITY["name"])}</text>',
            f'<text x="2" y="169" class="role" font-size="31">{esc(IDENTITY["role"])}</text>',
            text_lines(
                wrap(IDENTITY["tagline"], 31),
                x=2,
                y=224,
                line_height=37,
                css_class="mobileBody",
            ),
            "</g>",
            '<clipPath id="mobileCrop"><rect x="24" y="358" width="712" height="426" rx="28"/></clipPath>',
            '<g clip-path="url(#mobileCrop)">',
            f'<image href="{image_data("spatial-portfolio-hero-v1.png")}" x="24" y="358" '
            'width="712" height="426" preserveAspectRatio="xMaxYMid slice"/>',
            '<linearGradient id="mobileFade" x1="0" y1="0" x2="0" y2=".4">'
            '<stop offset="0" stop-color="#050814" stop-opacity=".72"/>'
            '<stop offset="1" stop-color="#050814" stop-opacity="0"/></linearGradient>',
            '<rect x="24" y="358" width="712" height="150" fill="url(#mobileFade)"/>',
            '<path d="M80 706C220 590 330 774 510 638S680 588 754 644" class="wire dash" '
            'stroke-width="3" opacity=".75"/>',
            "</g>",
            '<rect x="24" y="358" width="712" height="426" rx="28" fill="none" '
            'stroke="#E9F3FF" stroke-opacity=".17"/>',
            '<rect x="1" y="1" width="758" height="818" rx="33" fill="none" '
            'stroke="#E9F3FF" stroke-opacity=".15"/>',
            "</svg>",
        ]
    )


WORLD_PATHS = {
    "generative": [
        "M52 426C218 282 330 484 514 340S816 246 1150 372",
        "M102 118C330 34 486 184 632 118S894 92 1094 154",
    ],
    "language": [
        "M50 358C236 182 364 452 564 290S872 188 1140 302",
        "M164 90C312 176 436 84 602 148S876 220 1048 108",
    ],
    "movement": [
        "M42 442C214 322 278 438 458 326S766 220 1162 330",
        "M110 150C252 62 404 186 580 130S924 68 1084 180",
    ],
    "tools": [
        "M52 420C254 238 356 478 574 310S882 214 1144 340",
        "M104 124C278 38 414 206 606 116S884 72 1100 170",
    ],
}


def make_world(filename: str, title: str, description: str, variant: str) -> str:
    """Wrap one generated project world in an animated spatial viewport."""
    height = 560 if variant != "tools" else 590
    paths = WORLD_PATHS[variant]
    return "".join(
        [
            svg_open(title, description, 1200, height),
            image_layer(filename, 1200, height),
            '<linearGradient id="scanLight" x1="0" y1="0" x2="1" y2="0">'
            '<stop offset="0" stop-color="#63D9D1" stop-opacity="0"/>'
            '<stop offset=".5" stop-color="#B89DFF" stop-opacity=".72"/>'
            '<stop offset="1" stop-color="#FF9B7A" stop-opacity="0"/></linearGradient>',
            '<rect x="-260" y="0" width="250" height="100%" fill="url(#scanLight)" '
            'class="scan" opacity=".18"/>',
            f'<path d="{paths[0]}" class="wire draw" stroke-width="2.4" opacity=".76"/>',
            f'<path d="{paths[1]}" class="wire dash" stroke-width="1.5" opacity=".52"/>',
            '<g class="orbitReverse" opacity=".62"><ellipse cx="600" cy="285" rx="462" ry="178" '
            'fill="none" stroke="url(#signal)" stroke-width="1.2" stroke-dasharray="3 18"/></g>',
            '<g class="float">',
            '<circle cx="118" cy="124" r="6" fill="#63D9D1" class="pulse" filter="url(#glow)"/>',
            '<circle cx="1066" cy="182" r="6" fill="#FF9B7A" class="pulse" filter="url(#glow)"/>',
            '<circle cx="684" cy="458" r="5" fill="#B89DFF" class="pulse" filter="url(#glow)"/>',
            "</g>",
            frame(1200, height),
            "</svg>",
        ]
    )


def make_footer(width: int, height: int, mobile: bool = False) -> str:
    """Build the closing animated portal without embedding small copy."""
    center_x = width // 2
    center_y = height // 2
    rx = 250 if not mobile else 180
    ry = 56 if not mobile else 70
    outer_ry = ry - 20 if not mobile else ry - 26
    return "".join(
        [
            svg_open(
                "An open orbit",
                "A luminous animated mesh orbit closes the spatial portfolio.",
                width,
                height,
            ),
            f'<rect width="{width}" height="{height}" rx="28" fill="#050814"/>',
            f'<rect width="{width}" height="{height}" fill="url(#microGrid)" opacity=".72"/>',
            f'<g class="orbit"><ellipse cx="{center_x}" cy="{center_y}" rx="{rx}" ry="{ry}" '
            'fill="none" stroke="url(#signal)" stroke-width="3" stroke-dasharray="8 14"/></g>',
            f'<g class="orbitReverse"><ellipse cx="{center_x}" cy="{center_y}" rx="{rx + 72}" '
            f'ry="{outer_ry}" fill="none" stroke="url(#copper)" '
            'stroke-opacity=".55" stroke-width="1.5" stroke-dasharray="2 11"/></g>',
            f'<path d="M0 {center_y + 36}C{center_x // 2} {center_y - 86} '
            f'{center_x + center_x // 2} {center_y + 112} {width} {center_y - 34}" '
            'class="wire dash" stroke-width="2" opacity=".55"/>',
            f'<circle cx="{center_x}" cy="{center_y}" r="10" fill="#FFF9EF" class="pulse" '
            'filter="url(#glow)"/>',
            f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="27" '
            'fill="none" stroke="#E9F3FF" stroke-opacity=".15"/>',
            "</svg>",
        ]
    )


def main() -> None:
    """Generate every deterministic responsive profile SVG."""
    ASSETS.mkdir(parents=True, exist_ok=True)
    generated = {
        "spatial-hero.svg": make_hero(),
        "spatial-hero-mobile.svg": make_mobile_hero(),
        "world-generative-vision.svg": make_world(
            "world-generative-vision-v1.png",
            "Generative vision",
            "A glass generative seed flows through a woven mesh into a geometric leaf detection rig.",
            "generative",
        ),
        "world-language-memory.svg": make_world(
            "world-language-memory-v1.png",
            "Language and memory",
            "Paper poetry curls into an archival restoration structure through a luminous graph.",
            "language",
        ),
        "world-movement-products.svg": make_world(
            "world-movement-products-v1.png",
            "Movement and products",
            "A luminous route crosses ceramic terrain and becomes a glass product progress ring.",
            "movement",
        ),
        "tool-constellation.svg": make_world(
            "tool-constellation-v1.png",
            "Tool constellation",
            "Models, data, product craft, and delivery form one connected spatial system.",
            "tools",
        ),
        "spatial-footer.svg": make_footer(1200, 210),
        "spatial-footer-mobile.svg": make_footer(760, 250, mobile=True),
    }
    for filename, document in generated.items():
        (ASSETS / filename).write_text(document, encoding="utf-8")
    print(f"Generated {len(generated)} responsive Spatial Portfolio SVGs in {ASSETS}")


if __name__ == "__main__":
    main()
