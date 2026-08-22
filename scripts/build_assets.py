#!/usr/bin/env python3
"""Generate the animated Curiosity Workshop SVG assets."""

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
    """Return shared gradients, filters, and accessible reduced-motion CSS."""
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
  <linearGradient id="copper" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{THEME["amber"]}"/>
    <stop offset=".5" stop-color="{THEME["copper"]}"/>
    <stop offset="1" stop-color="{THEME["coral"]}"/>
  </linearGradient>
  <radialGradient id="globe" cx="35%" cy="28%" r="75%">
    <stop offset="0" stop-color="{THEME["paper"]}"/>
    <stop offset=".18" stop-color="{THEME["cyan"]}" stop-opacity=".95"/>
    <stop offset=".62" stop-color="{THEME["purple"]}" stop-opacity=".58"/>
    <stop offset="1" stop-color="#131523" stop-opacity=".2"/>
  </radialGradient>
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
    .display{{font:800 55px Inter,Segoe UI,Arial,sans-serif;fill:{THEME["text"]};letter-spacing:-2px}}
    .title{{font:800 38px Inter,Segoe UI,Arial,sans-serif;fill:{THEME["text"]};letter-spacing:-1px}}
    .section{{font:780 27px Inter,Segoe UI,Arial,sans-serif;fill:{THEME["text"]};letter-spacing:-.45px}}
    .cardTitle{{font:760 20px Inter,Segoe UI,Arial,sans-serif;fill:{THEME["text"]}}}
    .body{{font:500 16px Inter,Segoe UI,Arial,sans-serif;fill:{THEME["muted"]}}}
    .small{{font:560 13px Inter,Segoe UI,Arial,sans-serif;fill:{THEME["muted"]}}}
    .mono{{font:700 12px 'JetBrains Mono',Consolas,monospace;fill:{THEME["paper"]};letter-spacing:1.5px}}
    .panel{{fill:{THEME["panel"]};fill-opacity:.9;stroke:{THEME["paper"]};stroke-opacity:.13}}
    .wire{{fill:none;stroke:url(#signal);stroke-width:2;stroke-linecap:round}}
    .dash{{stroke-dasharray:8 13;animation:dash 13s linear infinite}}
    .floatA{{animation:floatA 6.5s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
    .floatB{{animation:floatB 8s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
    .pulse{{animation:pulse 3.2s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
    .spin{{animation:spin 24s linear infinite;transform-box:fill-box;transform-origin:center}}
    .scan{{animation:scan 5.5s ease-in-out infinite}}
    @keyframes dash{{to{{stroke-dashoffset:-420}}}}
    @keyframes floatA{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-9px)}}}}
    @keyframes floatB{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(7px)}}}}
    @keyframes pulse{{0%,100%{{opacity:.55;transform:scale(.94)}}50%{{opacity:1;transform:scale(1.08)}}}}
    @keyframes spin{{to{{transform:rotate(360deg)}}}}
    @keyframes scan{{0%,100%{{opacity:.15;transform:translateX(-35px)}}50%{{opacity:.72;transform:translateX(35px)}}}}
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
    """Draw a shared night backdrop and hairline frame."""
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
    css_class: str = "body",
) -> str:
    """Render wrapped text as individually positioned SVG text nodes."""
    return "".join(
        f'<text x="{x}" y="{y + index * line_height}" class="{css_class}">{esc(line)}</text>'
        for index, line in enumerate(lines)
    )


def make_hero() -> str:
    """Fuse the generated 3D workshop, identity, and motion into one hero."""
    svg = [
        svg_open(
            f"{IDENTITY['name']} · Curiosity Workshop",
            "A warm three-dimensional creative-computing workbench with an introduction.",
            1200,
            400,
        ),
        f'<image href="{image_data("curiosity-workshop-hero-v1.png")}" width="1200" height="400" '
        'preserveAspectRatio="xMidYMid slice"/>',
        '<linearGradient id="heroShade" x1="0" y1="0" x2=".75" y2="0">'
        '<stop offset="0" stop-color="#080B12" stop-opacity=".99"/>'
        '<stop offset=".48" stop-color="#080B12" stop-opacity=".87"/>'
        '<stop offset=".78" stop-color="#080B12" stop-opacity=".1"/>'
        '<stop offset="1" stop-color="#080B12" stop-opacity="0"/></linearGradient>',
        '<rect width="1200" height="400" fill="url(#heroShade)"/>',
        '<rect x="53" y="42" width="254" height="28" rx="14" fill="#F3EBDD" fill-opacity=".08" '
        'stroke="#D99362" stroke-opacity=".7"/>',
        '<circle cx="72" cy="56" r="4" fill="#FF9B7A" class="pulse"/>',
        '<text x="86" y="61" class="mono">CURIOSITY WORKSHOP · SINGAPORE</text>',
        f'<text x="52" y="145" class="display">{esc(IDENTITY["name"])}</text>',
        f'<text x="55" y="184" class="section">{esc(IDENTITY["role"])}</text>',
        text_lines(wrap(IDENTITY["tagline"], 46), x=55, y=226, line_height=26),
        '<g transform="translate(54 299)">',
    ]
    for index, label in enumerate(["AI + ML", "VISION", "ALGORITHMS", "PRODUCTS"]):
        x = index * 111
        svg.extend(
            [
                f'<rect x="{x}" y="0" width="98" height="32" rx="16" fill="#171923" '
                'stroke="#F3EBDD" stroke-opacity=".2"/>',
                f'<text x="{x + 49}" y="21" text-anchor="middle" class="mono" '
                f'font-size="10">{esc(label)}</text>',
            ]
        )
    svg.extend(
        [
            "</g>",
            '<path d="M57 359 C202 329 318 384 469 348" class="wire dash" opacity=".68"/>',
            '<circle cx="57" cy="359" r="5" fill="#63D9D1" filter="url(#glow)" class="pulse"/>',
            '<circle cx="469" cy="348" r="5" fill="#FF9B7A" filter="url(#glow)" class="pulse"/>',
            '<rect x="1" y="1" width="1198" height="398" rx="27" fill="none" '
            'stroke="#F3EBDD" stroke-opacity=".16"/>',
            "</svg>",
        ]
    )
    return "".join(svg)


def make_workbench() -> str:
    """Present three concise statements about the work currently on the desk."""
    svg = [
        svg_open(
            "On the workbench",
            "Three cards describe what Kun Ming is learning, building, and optimising for.",
            1200,
            390,
        ),
        frame(1200, 390),
        '<text x="54" y="56" class="mono">ON THE WORKBENCH / NOW</text>',
        '<text x="54" y="105" class="title">Learning is the input. Useful things are the output.</text>',
        '<text x="55" y="136" class="body">A small studio for careful experiments, approachable tools, and visible reasoning.</text>',
    ]
    accents = [THEME["cyan"], THEME["purple"], THEME["coral"]]
    icons = ["M0 20L22 0l22 20-22 20Z", "M0 0h44v44H0z", "M22 0a22 22 0 1 1-.1 0Z"]
    for index, item in enumerate(PROFILE["workbench"]):
        x = 54 + index * 374
        drift = "floatA" if index != 1 else "floatB"
        svg.extend(
            [
                f'<g transform="translate({x} 180)"><g class="{drift}">',
                '<rect width="342" height="150" rx="24" class="panel" filter="url(#soft)"/>',
                f'<path d="{icons[index]}" transform="translate(25 24) scale(.68)" '
                f'fill="{accents[index]}" fill-opacity=".17" stroke="{accents[index]}" stroke-width="2"/>',
                f'<text x="84" y="43" class="mono" fill="{accents[index]}">0{index + 1} / {esc(item["label"].upper())}</text>',
                f'<text x="24" y="86" class="cardTitle">{esc(item["title"])}</text>',
                text_lines(wrap(item["desc"], 42), x=24, y=113, line_height=21, css_class="small"),
                "</g></g>",
            ]
        )
    svg.extend(
        [
            '<path d="M45 354H1155" stroke="url(#signal)" stroke-opacity=".42" class="dash"/>',
            '<circle cx="1072" cy="354" r="6" fill="#F2C76E" class="pulse" filter="url(#glow)"/>',
            "</svg>",
        ]
    )
    return "".join(svg)


def make_cabinet() -> str:
    """Frame the generated six-compartment project cabinet."""
    return "".join(
        [
            svg_open(
                "The project cabinet",
                "A six-compartment three-dimensional cabinet representing six software projects.",
                1200,
                610,
            ),
            f'<image href="{image_data("project-cabinet-v1.png")}" width="1200" height="610" '
            'preserveAspectRatio="xMidYMid slice"/>',
            '<linearGradient id="cabShade" x1="0" y1="0" x2="0" y2=".42">'
            '<stop offset="0" stop-color="#080B12" stop-opacity=".96"/>'
            '<stop offset=".68" stop-color="#080B12" stop-opacity=".2"/>'
            '<stop offset="1" stop-color="#080B12" stop-opacity="0"/></linearGradient>',
            '<rect width="1200" height="170" fill="url(#cabShade)"/>',
            '<text x="54" y="56" class="mono">THE PROJECT CABINET / SIX OPEN DRAWERS</text>',
            '<text x="54" y="105" class="title">Every artifact starts with a question.</text>',
            '<text x="55" y="136" class="body">Use the expandable notes below to look inside each build.</text>',
            '<path d="M44 164H1156" stroke="url(#signal)" stroke-opacity=".55" class="dash"/>',
            '<g fill="#080B12" fill-opacity=".72" stroke="#F3EBDD" stroke-opacity=".35">',
            '<circle cx="380" cy="250" r="16"/><circle cx="820" cy="250" r="16"/>',
            '<circle cx="380" cy="386" r="16"/><circle cx="820" cy="386" r="16"/>',
            '<circle cx="380" cy="520" r="16"/><circle cx="820" cy="520" r="16"/>',
            "</g>",
            '<g class="mono" text-anchor="middle" fill="#F3EBDD">',
            '<text x="380" y="255">01</text><text x="820" y="255">02</text>',
            '<text x="380" y="391">03</text><text x="820" y="391">04</text>',
            '<text x="380" y="525">05</text><text x="820" y="525">06</text>',
            "</g>",
            '<rect x="1" y="1" width="1198" height="608" rx="27" fill="none" '
            'stroke="#F3EBDD" stroke-opacity=".17"/>',
            "</svg>",
        ]
    )


def make_machine() -> str:
    """Animate a question through the six stages of Kun Ming's making process."""
    steps = PROFILE["process"]
    svg = [
        svg_open(
            "How an idea leaves the workshop",
            "An animated assembly line moves from question through data, baseline, experiment, product, and sharing.",
            1200,
            430,
        ),
        frame(1200, 430),
        '<text x="54" y="56" class="mono">THE MAKING MACHINE / 06 STATIONS</text>',
        '<text x="54" y="106" class="title">A question is only the beginning.</text>',
        '<text x="55" y="137" class="body">The interesting work is turning it into evidence, an artifact, and a path someone else can follow.</text>',
        '<path id="route" d="M92 280 C226 193 340 350 474 262 S704 183 838 270 S1008 334 1110 245" '
        'fill="none" stroke="#F3EBDD" stroke-opacity=".16" stroke-width="34" stroke-linecap="round"/>',
        '<path d="M92 280 C226 193 340 350 474 262 S704 183 838 270 S1008 334 1110 245" '
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
                f'<circle cx="{x}" cy="{y}" r="32" fill="#171923" stroke="{color}" '
                'stroke-opacity=".72" filter="url(#soft)"/>',
                f'<circle cx="{x}" cy="{y}" r="10" fill="{color}" fill-opacity=".86" class="pulse"/>',
                f'<text x="{x}" y="{y + 62}" text-anchor="middle" class="mono">{index + 1:02d}</text>',
                f'<text x="{x}" y="{y + 84}" text-anchor="middle" class="small">{esc(label)}</text>',
                "</g>",
            ]
        )
    svg.extend(
        [
            '<circle r="9" fill="#FFF9EF" filter="url(#glow)">'
            '<animateMotion dur="8s" repeatCount="indefinite" rotate="auto">'
            '<mpath href="#route"/></animateMotion></circle>',
            '<text x="54" y="399" class="mono">COMPLEXITY HAS TO EARN ITS PLACE</text>',
            "</svg>",
        ]
    )
    return "".join(svg)


def make_curiosities() -> str:
    """Draw three animated sculptural curiosities."""
    svg = [
        svg_open(
            "Current curiosities",
            "Three animated objects represent generative systems, computer vision, and human-friendly machine learning.",
            1200,
            390,
        ),
        frame(1200, 390),
        '<text x="54" y="56" class="mono">CURRENT CURIOSITIES / SUBJECT TO CHANGE</text>',
        '<text x="54" y="104" class="title">Three corners I keep wandering back to.</text>',
    ]
    items = PROFILE["curiosities"]
    for index, item in enumerate(items):
        x = 54 + index * 374
        center = x + 171
        svg.append(f'<g transform="translate({x} 137)">')
        svg.append('<rect width="342" height="202" rx="24" class="panel" filter="url(#soft)"/>')
        if index == 0:
            svg.extend(
                [
                    '<circle cx="171" cy="58" r="34" fill="url(#globe)" class="pulse"/>',
                    '<ellipse cx="171" cy="58" rx="54" ry="18" fill="none" stroke="#D99362" class="spin"/>',
                    '<ellipse cx="171" cy="58" rx="18" ry="54" fill="none" stroke="#B89DFF" class="spin"/>',
                ]
            )
        elif index == 1:
            svg.extend(
                [
                    '<path d="M135 77C140 27 195 18 211 38C213 80 180 96 143 82Z" '
                    'fill="#8FBE72" fill-opacity=".72" stroke="#F3EBDD" stroke-opacity=".5" class="floatA"/>',
                    '<path d="M139 88L201 37M160 69l-18-16m39-3l9 20" fill="none" stroke="#F3EBDD" stroke-opacity=".62"/>',
                    '<path d="M116 27h28M116 27v28M226 27h-28M226 27v28M116 90h28M116 90V62M226 90h-28M226 90V62" '
                    'fill="none" stroke="#63D9D1" stroke-width="2" class="scan"/>',
                ]
            )
        else:
            svg.extend(
                [
                    '<path d="M110 72C135 19 169 103 197 47S231 84 246 43" class="wire dash"/>',
                    '<circle cx="110" cy="72" r="6" fill="#63D9D1" class="pulse"/>',
                    '<circle cx="197" cy="47" r="6" fill="#B89DFF" class="pulse"/>',
                    '<circle cx="246" cy="43" r="6" fill="#FF9B7A" class="pulse"/>',
                ]
            )
        dot = [THEME["cyan"], THEME["green"], THEME["coral"]][index]
        svg.extend(
            [
                f'<text x="22" y="133" class="cardTitle">{esc(item["title"])}</text>',
                text_lines(wrap(item["desc"], 40), x=22, y=158, line_height=19, css_class="small"),
                "</g>",
                f'<circle cx="{center}" cy="356" r="3" fill="{dot}"/>',
            ]
        )
    svg.append("</svg>")
    return "".join(svg)


def make_footer() -> str:
    """Close the profile with a restrained workshop night-light."""
    return "".join(
        [
            svg_open(
                "Workshop closing note",
                "A warm animated light path with a motto about curiosity, clarity, and usefulness.",
                1200,
                190,
            ),
            frame(1200, 190),
            '<path d="M0 138C168 38 294 178 452 108S724 48 874 116s222 50 326-30" '
            'class="wire dash" stroke-width="3" opacity=".72"/>',
            '<path d="M0 168C170 86 322 197 500 136s300-34 448 14 188 20 252-8" '
            'class="wire dash" opacity=".34"/>',
            '<circle cx="119" cy="108" r="7" fill="#63D9D1" class="pulse" filter="url(#glow)"/>',
            '<circle cx="1080" cy="102" r="7" fill="#FF9B7A" class="pulse" filter="url(#glow)"/>',
            f'<text x="600" y="80" text-anchor="middle" class="section">{esc(IDENTITY["motto"])}</text>',
            '<text x="600" y="112" text-anchor="middle" class="body">Thanks for looking around the workshop.</text>',
            "</svg>",
        ]
    )


def main() -> None:
    """Generate every deterministic Curiosity Workshop SVG."""
    ASSETS.mkdir(parents=True, exist_ok=True)
    generated = {
        "hero-curiosity-workshop.svg": make_hero(),
        "workbench-now.svg": make_workbench(),
        "project-cabinet.svg": make_cabinet(),
        "making-machine.svg": make_machine(),
        "current-curiosities.svg": make_curiosities(),
        "workshop-footer.svg": make_footer(),
    }
    for filename, document in generated.items():
        (ASSETS / filename).write_text(document, encoding="utf-8")
    print(f"Generated {len(generated)} Curiosity Workshop SVGs in {ASSETS}")


if __name__ == "__main__":
    main()
