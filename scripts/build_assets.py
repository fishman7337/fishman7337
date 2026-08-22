#!/usr/bin/env python3
"""Generate the animated Signal Garden SVG assets used by the profile README."""

from __future__ import annotations

import base64
import html
import textwrap
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
HERO_SOURCE = ASSETS / "signal-garden-hero-v2.png"
PROFILE = yaml.safe_load((ROOT / "content" / "profile.yml").read_text(encoding="utf-8"))
IDENTITY = PROFILE["identity"]
THEME = PROFILE["theme"]


def esc(value: object) -> str:
    """Escape a value for safe inclusion in SVG XML."""
    return html.escape(str(value), quote=True)


def wrap(value: str, width: int = 42) -> list[str]:
    """Wrap text into compact SVG display lines."""
    return textwrap.wrap(str(value), width=width, break_long_words=False)


def ellipsize(value: str, max_chars: int) -> str:
    """Truncate text to a stable display length."""
    value = str(value)
    if len(value) <= max_chars:
        return value
    return value[: max_chars - 1].rstrip() + "…"


def svg_open(height: int, title: str, description: str) -> list[str]:
    """Return accessible opening markup and the shared visual system."""
    return [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" ',
        f'height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{esc(title)}</title>',
        f'<desc id="desc">{esc(description)}</desc>',
        "<defs>",
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">',
        f'<stop offset="0" stop-color="{THEME["bg0"]}"/>',
        f'<stop offset="0.55" stop-color="{THEME["bg1"]}"/>',
        '<stop offset="1" stop-color="#16112C"/>',
        "</linearGradient>",
        '<linearGradient id="signal" x1="0" y1="0" x2="1" y2="0">',
        f'<stop offset="0" stop-color="{THEME["cyan"]}"/>',
        f'<stop offset="0.52" stop-color="{THEME["purple"]}"/>',
        f'<stop offset="1" stop-color="{THEME["coral"]}"/>',
        "</linearGradient>",
        '<radialGradient id="orb" cx="35%" cy="28%" r="72%">',
        '<stop offset="0" stop-color="#F7FAFF" stop-opacity=".96"/>',
        f'<stop offset=".18" stop-color="{THEME["cyan"]}" stop-opacity=".84"/>',
        f'<stop offset=".62" stop-color="{THEME["purple"]}" stop-opacity=".56"/>',
        '<stop offset="1" stop-color="#11152A" stop-opacity=".3"/>',
        "</radialGradient>",
        '<pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse">',
        '<path d="M36 0H0V36" fill="none" stroke="#8DA2C7" stroke-opacity=".08"/>',
        "</pattern>",
        '<filter id="glow" x="-80%" y="-80%" width="260%" height="260%">',
        '<feGaussianBlur stdDeviation="7" result="blur"/>',
        '<feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>',
        "</filter>",
        '<filter id="soft" x="-30%" y="-30%" width="160%" height="160%">',
        '<feDropShadow dx="0" dy="14" stdDeviation="18" flood-color="#02040B" flood-opacity=".58"/>',
        "</filter>",
        "<style><![CDATA[",
        ".title{font:800 52px Inter,Segoe UI,Arial,sans-serif;fill:#F7FAFF;letter-spacing:-1.8px}",
        ".section{font:800 30px Inter,Segoe UI,Arial,sans-serif;fill:#F7FAFF;letter-spacing:-.6px}",
        ".cardTitle{font:750 20px Inter,Segoe UI,Arial,sans-serif;fill:#F7FAFF}",
        ".body{font:500 16px Inter,Segoe UI,Arial,sans-serif;fill:#A8B4D1}",
        ".small{font:550 13px Inter,Segoe UI,Arial,sans-serif;fill:#A8B4D1}",
        ".mono{font:700 13px 'JetBrains Mono',Consolas,monospace;fill:#C8F8FF;letter-spacing:1.2px}",
        ".glass{fill:#12182C;fill-opacity:.78;stroke:#A8B4D1;stroke-opacity:.17}",
        ".glassBright{fill:#17213A;fill-opacity:.86;stroke:#38D9F5;stroke-opacity:.34}",
        ".mesh{fill:none;stroke:url(#signal);stroke-width:1.5;stroke-opacity:.46}",
        ".dash{stroke-dasharray:8 13;animation:dash 14s linear infinite}",
        ".driftA{animation:driftA 7s ease-in-out infinite;transform-box:fill-box;transform-origin:center}",
        ".driftB{animation:driftB 9s ease-in-out infinite;transform-box:fill-box;transform-origin:center}",
        ".pulse{animation:pulse 3.8s ease-in-out infinite;transform-box:fill-box;transform-origin:center}",
        ".spin{animation:spin 24s linear infinite;transform-box:fill-box;transform-origin:center}",
        "@keyframes dash{to{stroke-dashoffset:-420}}",
        "@keyframes driftA{0%,100%{transform:translateY(0)}50%{transform:translateY(-9px)}}",
        "@keyframes driftB{0%,100%{transform:translateY(0)}50%{transform:translateY(7px)}}",
        "@keyframes pulse{0%,100%{opacity:.58;transform:scale(.94)}50%{opacity:1;transform:scale(1.08)}}",
        "@keyframes spin{to{transform:rotate(360deg)}}",
        "@media(prefers-reduced-motion:reduce){*{animation:none!important}}",
        "]]></style>",
        "</defs>",
        f'<rect width="1200" height="{height}" rx="28" fill="url(#bg)"/>',
        f'<rect width="1200" height="{height}" rx="28" fill="url(#grid)"/>',
        f'<rect x="1" y="1" width="1198" height="{height - 2}" rx="27" fill="none" stroke="#99A9C8" stroke-opacity=".16"/>',
    ]


def svg_close(parts: list[str]) -> str:
    """Close and join an SVG document."""
    parts.append("</svg>")
    return "".join(parts)


def text_block(
    lines: list[str], x: int, y: int, line_height: int, css_class: str = "body"
) -> list[str]:
    """Render a list of escaped text lines."""
    return [
        f'<text x="{x}" y="{y + index * line_height}" class="{css_class}">{esc(line)}</text>'
        for index, line in enumerate(lines)
    ]


def chip(x: int, y: int, label: str, width: int, color: str) -> str:
    """Render a small rounded signal chip."""
    return (
        f'<g><rect x="{x}" y="{y}" width="{width}" height="34" rx="17" fill="#0D1325" '
        f'stroke="{color}" stroke-opacity=".46"/><circle cx="{x + 17}" cy="{y + 17}" r="4" '
        f'fill="{color}"/><text x="{x + 30}" y="{y + 22}" class="mono">{esc(label)}</text></g>'
    )


def make_hero() -> str:
    """Fuse the generated 3D artwork, identity, and motion into one hero."""
    image_data = base64.b64encode(HERO_SOURCE.read_bytes()).decode("ascii")
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" ',
        'width="1200" height="450" viewBox="0 0 1200 450" role="img" aria-labelledby="title desc">',
        f'<title id="title">{esc(IDENTITY["name"])} · Signal Garden</title>',
        '<desc id="desc">A luminous glass garden grows from flowing data, beside a concise introduction to Goh Kun Ming and his applied AI work.</desc>',
        "<defs>",
        '<linearGradient id="heroShade" x1="0" y1="0" x2="1" y2="0">',
        '<stop offset="0" stop-color="#020617" stop-opacity=".99"/>',
        '<stop offset=".34" stop-color="#020617" stop-opacity=".92"/>',
        '<stop offset=".58" stop-color="#020617" stop-opacity=".18"/>',
        '<stop offset="1" stop-color="#020617" stop-opacity="0"/>',
        "</linearGradient>",
        '<linearGradient id="heroSignal" x1="0" y1="0" x2="1" y2="0">',
        f'<stop offset="0" stop-color="{THEME["cyan"]}"/>',
        f'<stop offset=".52" stop-color="{THEME["purple"]}"/>',
        f'<stop offset="1" stop-color="{THEME["coral"]}"/>',
        "</linearGradient>",
        '<filter id="heroGlow" x="-100%" y="-100%" width="300%" height="300%">',
        '<feGaussianBlur stdDeviation="6" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>',
        "</filter>",
        '<clipPath id="heroClip"><rect width="1200" height="450" rx="30"/></clipPath>',
        "<style><![CDATA[",
        ".heroName{font:800 58px Inter,Segoe UI,Arial,sans-serif;fill:#F8FAFC;letter-spacing:-2px}",
        ".heroRole{font:700 19px Inter,Segoe UI,Arial,sans-serif;fill:#C8F8FF;letter-spacing:.2px}",
        ".heroBody{font:500 15px Inter,Segoe UI,Arial,sans-serif;fill:#C2CCE1}",
        ".heroMono{font:700 12px JetBrains Mono,Consolas,monospace;fill:#A8B4D1;letter-spacing:1.5px}",
        ".heroChip{font:700 11px JetBrains Mono,Consolas,monospace;fill:#EAFBFF;letter-spacing:.7px}",
        ".heroDash{stroke-dasharray:8 12;animation:heroDash 14s linear infinite}",
        ".heroPulse{animation:heroPulse 3.6s ease-in-out infinite;transform-box:fill-box;transform-origin:center}",
        ".heroFloat{animation:heroFloat 7s ease-in-out infinite;transform-box:fill-box;transform-origin:center}",
        "@keyframes heroDash{to{stroke-dashoffset:-360}}",
        "@keyframes heroPulse{0%,100%{opacity:.42;transform:scale(.86)}50%{opacity:1;transform:scale(1.15)}}",
        "@keyframes heroFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}",
        "@media(prefers-reduced-motion:reduce){*{animation:none!important}}",
        "]]></style>",
        "</defs>",
        '<g clip-path="url(#heroClip)">',
        f'<image width="1200" height="450" preserveAspectRatio="xMidYMid slice" xlink:href="data:image/png;base64,{image_data}"/>',
        '<rect width="760" height="450" fill="url(#heroShade)"/>',
        '<path d="M495 405 C650 354 758 424 894 374 S1082 322 1224 352" fill="none" stroke="url(#heroSignal)" stroke-width="2" stroke-opacity=".44" class="heroDash"/>',
        '<path d="M516 426 C672 382 764 444 918 401 S1086 360 1216 383" fill="none" stroke="#38D9F5" stroke-width="1" stroke-opacity=".22" class="heroDash"/>',
        '<g filter="url(#heroGlow)">',
        f'<circle cx="702" cy="393" r="5" fill="{THEME["cyan"]}" class="heroPulse"/>',
        f'<circle cx="955" cy="364" r="5" fill="{THEME["purple"]}" class="heroPulse"/>',
        f'<circle cx="1122" cy="341" r="5" fill="{THEME["coral"]}" class="heroPulse"/>',
        "</g>",
        '<g class="heroFloat">',
        '<rect x="58" y="42" width="170" height="28" rx="14" fill="#0B1225" fill-opacity=".86" stroke="#38D9F5" stroke-opacity=".42"/>',
        '<circle cx="76" cy="56" r="4" fill="#5EEAD4" filter="url(#heroGlow)" class="heroPulse"/>',
        '<text x="90" y="60" class="heroMono">SIGNAL GARDEN / 01</text>',
        "</g>",
        f'<text x="58" y="143" class="heroName">{esc(IDENTITY["name"])}</text>',
        f'<text x="60" y="181" class="heroRole">{esc(IDENTITY["role"])}</text>',
        '<text x="60" y="220" class="heroBody">Curious questions → reproducible experiments →</text>',
        '<text x="60" y="244" class="heroBody">creative tools and useful data products.</text>',
        f'<text x="60" y="282" class="heroMono">SINGAPORE · OPEN WORK · ARXIV {esc(PROFILE["research"]["arxiv_id"])}</text>',
    ]
    labels = PROFILE["signals"][:4]
    widths = [132, 146, 112, 126]
    colors = [THEME["cyan"], THEME["purple"], THEME["coral"], THEME["green"]]
    x = 60
    for index, (label, width, color) in enumerate(zip(labels, widths, colors, strict=True)):
        if index == 2:
            x = 60
        y = 314 if index < 2 else 360
        parts.extend(
            [
                f'<rect x="{x}" y="{y}" width="{width}" height="32" rx="16" fill="#0A1021" fill-opacity=".88" stroke="{color}" stroke-opacity=".44"/>',
                f'<circle cx="{x + 17}" cy="{y + 16}" r="4" fill="{color}"/>',
                f'<text x="{x + 29}" y="{y + 20}" class="heroChip">{esc(label.upper())}</text>',
            ]
        )
        x += width + 10
    parts.extend(
        [
            "</g>",
            '<rect x="1" y="1" width="1198" height="448" rx="29" fill="none" stroke="#A9B8D4" stroke-opacity=".2"/>',
        ]
    )
    return svg_close(parts)


def make_focus_garden() -> str:
    """Build four animated focus cards from the profile source."""
    parts = svg_open(
        380,
        "How Goh Kun Ming grows ideas",
        "Four focus cards covering exploration, modelling, product building, and sharing open work.",
    )
    parts.extend(
        [
            '<text x="54" y="62" class="section">How I grow an idea</text>',
            '<text x="54" y="91" class="body">A small loop for turning curiosity into something useful.</text>',
            '<path d="M88 304 C246 242 330 352 480 290 S744 226 890 290 S1054 338 1160 260" class="mesh dash"/>',
        ]
    )
    colors = [THEME["cyan"], THEME["purple"], THEME["coral"], THEME["green"]]
    for index, (card_data, color) in enumerate(zip(PROFILE["focus_cards"], colors, strict=True)):
        x = 54 + index * 286
        css = "driftA" if index % 2 == 0 else "driftB"
        parts.extend(
            [
                f'<g class="{css}" filter="url(#soft)">',
                f'<rect x="{x}" y="126" width="250" height="164" rx="24" class="glass"/>',
                f'<circle cx="{x + 34}" cy="160" r="10" fill="{color}" opacity=".9" filter="url(#glow)"/>',
                f'<text x="{x + 56}" y="166" class="mono">{esc(card_data["label"])}</text>',
                f'<text x="{x + 24}" y="207" class="cardTitle">{esc(card_data["title"])}</text>',
            ]
        )
        parts.extend(text_block(wrap(card_data["desc"], 30)[:3], x + 24, 238, 20, "small"))
        parts.append("</g>")
    return svg_close(parts)


def make_project_garden() -> str:
    """Build a glowing project constellation without organization-coded imagery."""
    projects = PROFILE["projects"][:6]
    positions = [(54, 78), (54, 226), (54, 374), (886, 78), (886, 226), (886, 374)]
    anchors = [(314, 128), (314, 276), (314, 424), (886, 128), (886, 276), (886, 424)]
    parts = svg_open(
        540,
        "Selected project Signal Garden",
        "Animated constellation of six public machine-learning, algorithms, and product projects.",
    )
    parts.extend(
        [
            '<text x="54" y="50" class="section">Selected work · a living project garden</text>',
            '<circle cx="600" cy="276" r="108" fill="url(#orb)" opacity=".72" filter="url(#glow)" class="pulse"/>',
            '<g class="spin"><ellipse cx="600" cy="276" rx="174" ry="68" class="mesh"/><ellipse cx="600" cy="276" rx="68" ry="174" class="mesh" transform="rotate(24 600 276)"/></g>',
            f'<text x="600" y="269" text-anchor="middle" class="mono">@{esc(IDENTITY["username"])}</text>',
            '<text x="600" y="297" text-anchor="middle" class="small">research · tools · products</text>',
        ]
    )
    for index, (project, (x, y), (ax, ay)) in enumerate(
        zip(projects, positions, anchors, strict=True)
    ):
        color = [THEME["cyan"], THEME["purple"], THEME["coral"], THEME["green"]][index % 4]
        curve_x = 470 if ax < 600 else 730
        parts.extend(
            [
                f'<path d="M600 276 C{curve_x} 276 {curve_x} {ay} {ax} {ay}" class="mesh dash"/>',
                f'<circle cx="{ax}" cy="{ay}" r="6" fill="{color}" filter="url(#glow)" class="pulse"/>',
                f'<g class="{"driftA" if index % 2 == 0 else "driftB"}" filter="url(#soft)">',
                f'<rect x="{x}" y="{y}" width="260" height="100" rx="21" class="glass"/>',
                f'<rect x="{x + 16}" y="{y + 15}" width="86" height="23" rx="11.5" fill="{color}" fill-opacity=".13" stroke="{color}" stroke-opacity=".42"/>',
                f'<text x="{x + 59}" y="{y + 31}" text-anchor="middle" class="small" fill="{color}">{esc(project["theme"])}</text>',
                f'<text x="{x + 18}" y="{y + 61}" class="cardTitle">{esc(ellipsize(project["name"], 24))}</text>',
                f'<text x="{x + 18}" y="{y + 84}" class="small">{esc(ellipsize(project["stack"], 36))}</text>',
                "</g>",
            ]
        )
    return svg_close(parts)


def make_research_loop() -> str:
    """Build the evidence-first research loop with a moving signal particle."""
    stages = [
        ("01", "Question", "Make it specific"),
        ("02", "Baseline", "Start honestly"),
        ("03", "Experiment", "Keep it reproducible"),
        ("04", "Evaluate", "Measure + limit"),
        ("05", "Share", "Publish the trail"),
    ]
    parts = svg_open(
        300,
        "Evidence-first research loop",
        "Question, baseline, experiment, evaluation, and sharing connected by an animated signal path.",
    )
    parts.extend(
        [
            '<text x="54" y="57" class="section">My research loop</text>',
            '<text x="54" y="86" class="body">Good work should leave a trail that someone else can follow.</text>',
            '<path id="flow" d="M116 190 C260 120 328 248 462 190 S676 132 804 190 S1002 238 1090 190" fill="none" stroke="url(#signal)" stroke-width="4" stroke-linecap="round" opacity=".5"/>',
            f'<circle r="8" fill="{THEME["cyan"]}" filter="url(#glow)"><animateMotion dur="8s" repeatCount="indefinite" path="M116 190 C260 120 328 248 462 190 S676 132 804 190 S1002 238 1090 190"/></circle>',
        ]
    )
    for index, (number, label, note) in enumerate(stages):
        x = 34 + index * 231
        y = 126 if index % 2 == 0 else 180
        color = [THEME["cyan"], THEME["purple"], THEME["coral"], THEME["green"]][index % 4]
        parts.extend(
            [
                f'<g class="{"driftA" if index % 2 == 0 else "driftB"}">',
                f'<rect x="{x}" y="{y}" width="198" height="90" rx="20" class="glassBright"/>',
                f'<text x="{x + 18}" y="{y + 27}" class="mono" fill="{color}">{number}</text>',
                f'<text x="{x + 18}" y="{y + 54}" class="cardTitle">{label}</text>',
                f'<text x="{x + 18}" y="{y + 76}" class="small">{note}</text>',
                "</g>",
            ]
        )
    return svg_close(parts)


def make_signal_footer() -> str:
    """Build the animated closing mesh and profile motto."""
    parts = svg_open(
        190,
        "Signal Garden closing wave",
        "Animated flowing mesh with a curious and careful building motto.",
    )
    parts.extend(
        [
            '<path d="M0 128 C140 40 230 170 370 104 S612 54 748 112 S1002 168 1200 70" class="mesh dash" stroke-width="3"/>',
            '<path d="M0 158 C174 74 274 194 430 126 S692 82 836 134 S1050 184 1200 112" class="mesh dash" opacity=".48"/>',
            '<path d="M0 98 C154 12 290 134 446 74 S698 28 858 86 S1050 124 1200 42" class="mesh dash" opacity=".28"/>',
            f'<circle cx="110" cy="106" r="7" fill="{THEME["cyan"]}" filter="url(#glow)" class="pulse"/>',
            f'<circle cx="1080" cy="86" r="7" fill="{THEME["coral"]}" filter="url(#glow)" class="pulse"/>',
            f'<text x="600" y="80" text-anchor="middle" class="section">{esc(IDENTITY["motto"])}</text>',
            '<text x="600" y="111" text-anchor="middle" class="body">Thanks for wandering through.</text>',
        ]
    )
    return svg_close(parts)


def main() -> None:
    """Generate every deterministic Signal Garden SVG."""
    ASSETS.mkdir(parents=True, exist_ok=True)
    generated = {
        "hero-signal-garden.svg": make_hero(),
        "focus-garden.svg": make_focus_garden(),
        "project-garden.svg": make_project_garden(),
        "research-loop.svg": make_research_loop(),
        "signal-footer.svg": make_signal_footer(),
    }
    for filename, content in generated.items():
        (ASSETS / filename).write_text(content + "\n", encoding="utf-8")
        print(f"wrote {ASSETS / filename}")


if __name__ == "__main__":
    main()
