#!/usr/bin/env python3
"""Generate the responsive visual assets for the GitHub profile."""

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
    """Escape a value for safe SVG text insertion."""
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
    """Return the shared visual language and reduced-motion CSS."""
    return f"""
<defs>
  <linearGradient id="night" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{THEME["bg0"]}"/>
    <stop offset=".58" stop-color="{THEME["bg1"]}"/>
    <stop offset="1" stop-color="#211A25"/>
  </linearGradient>
  <linearGradient id="signal" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{THEME["cyan"]}"/>
    <stop offset=".5" stop-color="{THEME["purple"]}"/>
    <stop offset="1" stop-color="{THEME["coral"]}"/>
  </linearGradient>
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
    <path d="M32 0H0V32" fill="none" stroke="#F3EBDD" stroke-opacity=".045"/>
  </pattern>
  <filter id="soft" x="-30%" y="-30%" width="160%" height="170%">
    <feDropShadow dx="0" dy="16" stdDeviation="18" flood-color="#02040A" flood-opacity=".58"/>
  </filter>
  <filter id="glow" x="-100%" y="-100%" width="300%" height="300%">
    <feGaussianBlur stdDeviation="6" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <style><![CDATA[
    .display{{font:800 58px Inter,Segoe UI,Arial,sans-serif;fill:{THEME["text"]};letter-spacing:-2px}}
    .mobileDisplay{{font:800 64px Inter,Segoe UI,Arial,sans-serif;fill:{THEME["text"]};letter-spacing:-2px}}
    .title{{font:800 40px Inter,Segoe UI,Arial,sans-serif;fill:{THEME["text"]};letter-spacing:-1px}}
    .section{{font:780 28px Inter,Segoe UI,Arial,sans-serif;fill:{THEME["text"]};letter-spacing:-.45px}}
    .body{{font:520 18px Inter,Segoe UI,Arial,sans-serif;fill:{THEME["muted"]}}}
    .mobileBody{{font:520 25px Inter,Segoe UI,Arial,sans-serif;fill:{THEME["muted"]}}}
    .small{{font:570 15px Inter,Segoe UI,Arial,sans-serif;fill:{THEME["muted"]}}}
    .mono{{font:720 13px 'JetBrains Mono',Consolas,monospace;fill:{THEME["paper"]};letter-spacing:1.5px}}
    .wire{{fill:none;stroke:url(#signal);stroke-width:2;stroke-linecap:round}}
    .dash{{stroke-dasharray:8 13;animation:dash 13s linear infinite}}
    .floatA{{animation:floatA 6.5s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
    .floatB{{animation:floatB 8s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
    .pulse{{animation:pulse 3.2s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
    @keyframes dash{{to{{stroke-dashoffset:-420}}}}
    @keyframes floatA{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-8px)}}}}
    @keyframes floatB{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(7px)}}}}
    @keyframes pulse{{0%,100%{{opacity:.55;transform:scale(.94)}}50%{{opacity:1;transform:scale(1.08)}}}}
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


def frame(width: int, height: int, radius: int = 28) -> str:
    """Draw the shared night backdrop and hairline frame."""
    return (
        f'<rect width="{width}" height="{height}" rx="{radius}" fill="url(#night)"/>'
        f'<rect width="{width}" height="{height}" rx="{radius}" fill="url(#grid)"/>'
        f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="{radius - 1}" '
        'fill="none" stroke="#F3EBDD" stroke-opacity=".14"/>'
    )


def text_lines(
    lines: list[str],
    *,
    x: int,
    y: int,
    line_height: int,
    css_class: str,
) -> str:
    """Render wrapped text as individually positioned SVG text nodes."""
    return "".join(
        f'<text x="{x}" y="{y + index * line_height}" class="{css_class}">{esc(line)}</text>'
        for index, line in enumerate(lines)
    )


def make_hero() -> str:
    """Build the concise desktop identity hero."""
    svg = [
        svg_open(
            f"{IDENTITY['name']} · Ideas to useful tools",
            "A tactile three-dimensional creative-computing workbench with a concise introduction.",
            1200,
            420,
        ),
        f'<image href="{image_data("curiosity-workshop-hero-v1.png")}" width="1200" height="420" '
        'preserveAspectRatio="xMidYMid slice"/>',
        '<linearGradient id="heroShade" x1="0" y1="0" x2=".78" y2="0">'
        '<stop offset="0" stop-color="#080B12" stop-opacity=".99"/>'
        '<stop offset=".5" stop-color="#080B12" stop-opacity=".9"/>'
        '<stop offset=".82" stop-color="#080B12" stop-opacity=".08"/>'
        '<stop offset="1" stop-color="#080B12" stop-opacity="0"/></linearGradient>',
        '<rect width="1200" height="420" fill="url(#heroShade)"/>',
        '<rect x="54" y="46" width="246" height="30" rx="15" fill="#F3EBDD" fill-opacity=".08" '
        'stroke="#D99362" stroke-opacity=".72"/>',
        '<circle cx="74" cy="61" r="4" fill="#FF9B7A" class="pulse"/>',
        '<text x="89" y="66" class="mono">IDEAS → EVIDENCE → TOOLS</text>',
        f'<text x="54" y="156" class="display">{esc(IDENTITY["name"])}</text>',
        f'<text x="57" y="199" class="section">{esc(IDENTITY["role"])}</text>',
        text_lines(wrap(IDENTITY["tagline"], 40), x=57, y=249, line_height=29, css_class="body"),
        '<g transform="translate(56 324)">',
    ]
    for index, label in enumerate(["GENERATIVE", "VISION", "ALGORITHMS", "PRODUCT"]):
        x = index * 122
        svg.extend(
            [
                f'<rect x="{x}" width="110" height="34" rx="17" fill="#171923" '
                'stroke="#F3EBDD" stroke-opacity=".2"/>',
                f'<text x="{x + 55}" y="22" text-anchor="middle" class="mono" '
                f'font-size="10">{esc(label)}</text>',
            ]
        )
    svg.extend(
        [
            "</g>",
            '<path d="M58 385C202 351 330 411 492 370" class="wire dash" opacity=".64"/>',
            '<circle cx="58" cy="385" r="5" fill="#63D9D1" filter="url(#glow)" class="pulse"/>',
            '<circle cx="492" cy="370" r="5" fill="#FF9B7A" filter="url(#glow)" class="pulse"/>',
            '<rect x="1" y="1" width="1198" height="418" rx="27" fill="none" '
            'stroke="#F3EBDD" stroke-opacity=".16"/>',
            "</svg>",
        ]
    )
    return "".join(svg)


def make_mobile_hero() -> str:
    """Build a portrait composition with readable typography for narrow screens."""
    return "".join(
        [
            svg_open(
                f"{IDENTITY['name']} · Applied AI and Analytics",
                "A mobile-first introduction above a cropped three-dimensional creative-computing workbench.",
                760,
                760,
            ),
            frame(760, 760, 34),
            '<rect x="46" y="44" width="314" height="38" rx="19" fill="#F3EBDD" fill-opacity=".08" '
            'stroke="#D99362" stroke-opacity=".72"/>',
            '<circle cx="70" cy="63" r="5" fill="#FF9B7A" class="pulse"/>',
            '<text x="91" y="69" class="mono" font-size="16">IDEAS → EVIDENCE → TOOLS</text>',
            f'<text x="46" y="170" class="mobileDisplay">{esc(IDENTITY["name"])}</text>',
            f'<text x="49" y="217" class="section" font-size="32">{esc(IDENTITY["role"])}</text>',
            text_lines(
                wrap(IDENTITY["tagline"], 33),
                x=49,
                y=270,
                line_height=34,
                css_class="mobileBody",
            ),
            '<clipPath id="mobileScene"><rect x="24" y="350" width="712" height="374" rx="28"/></clipPath>',
            '<g clip-path="url(#mobileScene)">',
            f'<image href="{image_data("curiosity-workshop-hero-v1.png")}" x="24" y="350" '
            'width="712" height="374" preserveAspectRatio="xMaxYMid slice"/>',
            '<linearGradient id="sceneFade" x1="0" y1="0" x2="0" y2=".4">'
            '<stop offset="0" stop-color="#080B12" stop-opacity=".72"/>'
            '<stop offset="1" stop-color="#080B12" stop-opacity="0"/></linearGradient>',
            '<rect x="24" y="350" width="712" height="160" fill="url(#sceneFade)"/>',
            "</g>",
            '<rect x="24" y="350" width="712" height="374" rx="28" fill="none" '
            'stroke="#F3EBDD" stroke-opacity=".16"/>',
            "</svg>",
        ]
    )


def make_cabinet() -> str:
    """Present the six project exhibits without competing overlay copy."""
    return "".join(
        [
            svg_open(
                "Six selected project exhibits",
                "A six-compartment three-dimensional cabinet representing six software projects.",
                1200,
                600,
            ),
            f'<image href="{image_data("project-cabinet-v1.png")}" width="1200" height="600" '
            'preserveAspectRatio="xMidYMid slice"/>',
            '<path d="M56 56H300" stroke="url(#signal)" stroke-width="3" class="dash" opacity=".72"/>',
            '<text x="56" y="87" class="mono">SIX BUILDS / SIX QUESTIONS</text>',
            '<rect x="1" y="1" width="1198" height="598" rx="27" fill="none" '
            'stroke="#F3EBDD" stroke-opacity=".17"/>',
            "</svg>",
        ]
    )


def make_machine() -> str:
    """Animate one idea through six honest stages of making."""
    steps = PROFILE["process"]
    svg = [
        svg_open(
            "From question to useful",
            "An animated path moves through question, data, baseline, experiment, product, and sharing.",
            1200,
            430,
        ),
        frame(1200, 430),
        '<text x="54" y="57" class="mono">FROM QUESTION TO USEFUL / 06 STAGES</text>',
        '<text x="54" y="110" class="title">The model is only the middle.</text>',
        '<text x="55" y="145" class="body">Good work also explains where it came from and how someone else can try it.</text>',
        '<path id="route" d="M92 280C226 193 340 350 474 262S704 183 838 270S1008 334 1110 245" '
        'fill="none" stroke="#F3EBDD" stroke-opacity=".16" stroke-width="34" stroke-linecap="round"/>',
        '<path d="M92 280C226 193 340 350 474 262S704 183 838 270S1008 334 1110 245" '
        'class="wire dash" stroke-width="3"/>',
    ]
    positions = [(92, 280), (290, 252), (474, 262), (672, 229), (838, 270), (1110, 245)]
    colors = [
        THEME["cyan"],
        THEME["blue"],
        THEME["purple"],
        THEME["coral"],
        THEME["amber"],
        THEME["green"],
    ]
    for index, ((x, y), label, color) in enumerate(zip(positions, steps, colors, strict=True)):
        drift = "floatA" if index % 2 == 0 else "floatB"
        svg.extend(
            [
                f'<g class="{drift}">',
                f'<circle cx="{x}" cy="{y}" r="33" fill="#171923" stroke="{color}" '
                'stroke-opacity=".75" filter="url(#soft)"/>',
                f'<circle cx="{x}" cy="{y}" r="10" fill="{color}" class="pulse"/>',
                f'<text x="{x}" y="{y + 61}" text-anchor="middle" class="mono">{index + 1:02d}</text>',
                f'<text x="{x}" y="{y + 85}" text-anchor="middle" class="small">{esc(label)}</text>',
                "</g>",
            ]
        )
    svg.extend(
        [
            '<circle r="9" fill="#FFF9EF" filter="url(#glow)">'
            '<animateMotion dur="8s" repeatCount="indefinite" rotate="auto">'
            '<mpath href="#route"/></animateMotion></circle>',
            '<text x="54" y="402" class="mono">QUESTION · EVIDENCE · ARTIFACT · HANDOFF</text>',
            "</svg>",
        ]
    )
    return "".join(svg)


def make_footer() -> str:
    """Close the desktop profile with one restrained line."""
    return "".join(
        [
            svg_open(
                "Curious by default. Clear by design.",
                "An animated line closes the profile.",
                1200,
                170,
            ),
            frame(1200, 170),
            '<path d="M0 130C168 30 294 170 452 100S724 40 874 108s222 50 326-30" '
            'class="wire dash" stroke-width="3" opacity=".7"/>',
            '<circle cx="119" cy="100" r="7" fill="#63D9D1" class="pulse" filter="url(#glow)"/>',
            '<circle cx="1080" cy="94" r="7" fill="#FF9B7A" class="pulse" filter="url(#glow)"/>',
            f'<text x="600" y="77" text-anchor="middle" class="section">{esc(IDENTITY["motto"])}</text>',
            '<text x="600" y="109" text-anchor="middle" class="body">Thanks for looking around.</text>',
            "</svg>",
        ]
    )


def make_mobile_footer() -> str:
    """Close the narrow profile with readable type and subtle motion."""
    return "".join(
        [
            svg_open(
                "Curious by default. Clear by design.",
                "A mobile closing note with an animated line.",
                760,
                250,
            ),
            frame(760, 250, 30),
            '<path d="M0 190C120 100 224 226 352 165S566 118 760 182" '
            'class="wire dash" stroke-width="3" opacity=".7"/>',
            '<circle cx="88" cy="158" r="8" fill="#63D9D1" class="pulse" filter="url(#glow)"/>',
            '<circle cx="674" cy="166" r="8" fill="#FF9B7A" class="pulse" filter="url(#glow)"/>',
            f'<text x="380" y="83" text-anchor="middle" class="title">{esc(IDENTITY["motto"])}</text>',
            '<text x="380" y="124" text-anchor="middle" class="mobileBody">Thanks for looking around.</text>',
            "</svg>",
        ]
    )


def main() -> None:
    """Generate every deterministic responsive profile SVG."""
    ASSETS.mkdir(parents=True, exist_ok=True)
    generated = {
        "hero-curiosity-workshop.svg": make_hero(),
        "hero-curiosity-workshop-mobile.svg": make_mobile_hero(),
        "project-cabinet.svg": make_cabinet(),
        "making-machine.svg": make_machine(),
        "workshop-footer.svg": make_footer(),
        "workshop-footer-mobile.svg": make_mobile_footer(),
    }
    for filename, document in generated.items():
        (ASSETS / filename).write_text(document, encoding="utf-8")
    print(f"Generated {len(generated)} responsive profile SVGs in {ASSETS}")


if __name__ == "__main__":
    main()
