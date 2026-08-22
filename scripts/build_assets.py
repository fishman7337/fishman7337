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
RESEARCH_SOURCE = ASSETS / "research-seed-lab-v1.png"
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
        ".display{font:800 42px Inter,Segoe UI,Arial,sans-serif;fill:#F7FAFF;letter-spacing:-1.4px}",
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


def make_manifesto() -> str:
    """Build the asymmetric editorial introduction panel."""
    parts = svg_open(
        430,
        "Goh Kun Ming's working manifesto",
        "An editorial introduction about turning questions into evidence, experiments, and useful software.",
    )
    parts.extend(
        [
            '<rect x="48" y="46" width="675" height="338" rx="30" class="glassBright" filter="url(#soft)"/>',
            '<text x="82" y="92" class="mono">THE MESSY MIDDLE</text>',
            '<text x="80" y="153" class="display">I like the moment</text>',
            '<text x="80" y="202" class="display">when a question</text>',
            '<text x="80" y="251" class="display">becomes a tool.</text>',
            '<text x="82" y="302" class="body">Data first. Baseline nearby. Claims kept honest.</text>',
            '<text x="82" y="330" class="body">Then make the useful part approachable.</text>',
            '<path d="M82 357 H638" stroke="url(#signal)" stroke-width="3" stroke-linecap="round" class="dash"/>',
        ]
    )
    notes = [
        ("NOW", "Applied AI &amp; Analytics", "Learning in Singapore", THEME["cyan"]),
        ("CURIOUS ABOUT", "Generative AI · Vision", "Quantum ML · Data products", THEME["purple"]),
        ("DEFAULT MODE", "Build → test → explain", "Share the evidence trail", THEME["coral"]),
    ]
    for index, (label, title, note, color) in enumerate(notes):
        y = 46 + index * 116
        parts.extend(
            [
                f'<g class="{"driftA" if index % 2 == 0 else "driftB"}">',
                f'<rect x="755" y="{y}" width="397" height="96" rx="24" class="glass"/>',
                f'<rect x="755" y="{y}" width="6" height="96" rx="3" fill="{color}" opacity=".86"/>',
                f'<circle cx="790" cy="{y + 28}" r="7" fill="{color}" filter="url(#glow)"/>',
                f'<text x="811" y="{y + 33}" class="mono">{label}</text>',
                f'<text x="788" y="{y + 62}" class="cardTitle">{title}</text>',
                f'<text x="788" y="{y + 83}" class="small">{note}</text>',
                "</g>",
            ]
        )
    return svg_close(parts)


def project_art(index: int, color: str) -> list[str]:
    """Return a distinct animated visual metaphor for one project specimen."""
    if index == 0:
        return [
            '<circle cx="936" cy="190" r="92" fill="url(#orb)" opacity=".82" filter="url(#glow)" class="pulse"/>',
            '<g class="spin"><ellipse cx="936" cy="190" rx="148" ry="54" class="mesh"/><ellipse cx="936" cy="190" rx="54" ry="148" class="mesh" transform="rotate(28 936 190)"/></g>',
            '<path d="M850 190 Q936 118 1022 190 T1194 190" class="mesh dash"/>',
        ]
    if index == 1:
        return [
            f'<path d="M908 314 C782 222 814 92 1088 70 C1094 242 1028 330 908 314Z" fill="{color}" fill-opacity=".13" stroke="{color}" stroke-width="3"/>',
            '<path d="M846 300 C928 242 1000 170 1082 82 M926 230 L868 178 M968 188 L1022 138" class="mesh dash"/>',
            '<rect x="825" y="112" width="116" height="96" rx="12" fill="none" stroke="#F7FAFF" stroke-opacity=".52" class="driftA"/>',
            '<rect x="970" y="198" width="124" height="92" rx="12" fill="none" stroke="#F7FAFF" stroke-opacity=".34" class="driftB"/>',
        ]
    if index == 2:
        return [
            f'<circle cx="927" cy="170" r="106" fill="{color}" fill-opacity=".13"/>',
            '<circle cx="965" cy="136" r="104" fill="#080C1D"/>',
            '<path d="M808 270 Q926 196 1100 242" class="mesh dash"/>',
            '<g class="driftA" stroke="#F7FAFF" stroke-linecap="round"><path d="M830 304h72"/><path d="M928 304h104"/><path d="M1056 304h72"/></g>',
            f'<circle cx="818" cy="88" r="8" fill="{color}" class="pulse" filter="url(#glow)"/>',
        ]
    if index == 3:
        return [
            '<g class="driftB"><rect x="824" y="68" width="254" height="276" rx="16" class="glassBright"/><path d="M858 112h168M858 146h142M858 180h176M858 214h116" stroke="#A8B4D1" stroke-width="9" stroke-linecap="round" opacity=".42"/></g>',
            '<path d="M950 228v44M950 272l-64 44M950 272l64 44M886 316l-42 30M886 316l34 34M1014 316l-34 34M1014 316l46 30" class="mesh dash"/>',
            f'<circle cx="950" cy="228" r="9" fill="{color}" class="pulse"/>',
        ]
    if index == 4:
        return [
            '<path d="M786 298 C838 210 912 286 952 190 S1050 98 1138 136" fill="none" stroke="url(#signal)" stroke-width="9" stroke-linecap="round" class="dash"/>',
            '<path d="M798 98h126l40 54h154v180H798Z" fill="#111A30" stroke="#A8B4D1" stroke-opacity=".24"/>',
            f'<circle cx="798" cy="298" r="17" fill="{color}" filter="url(#glow)" class="pulse"/><circle cx="1138" cy="136" r="17" fill="{color}" filter="url(#glow)" class="pulse"/>',
        ]
    return [
        '<circle cx="954" cy="196" r="128" fill="none" stroke="#A8B4D1" stroke-opacity=".2" stroke-width="28"/>',
        f'<path d="M954 68 A128 128 0 1 1 836 246" fill="none" stroke="{color}" stroke-width="28" stroke-linecap="round" filter="url(#glow)" class="pulse"/>',
        '<path d="M778 254h72l28-66 52 122 38-84 32 28h134" fill="none" stroke="url(#signal)" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" class="dash"/>',
    ]


def make_project_specimen(project: dict[str, str], index: int) -> str:
    """Build one readable, clickable project-card illustration."""
    color = [THEME["cyan"], THEME["purple"], THEME["coral"], THEME["green"]][index % 4]
    parts = svg_open(
        420,
        f"{project['name']} project specimen",
        f"Animated visual card for {project['name']}, a {project['theme']} project.",
    )
    parts.extend(
        [
            f'<text x="54" y="58" class="mono">SPECIMEN / {index + 1:02d}</text>',
            f'<rect x="54" y="82" width="148" height="30" rx="15" fill="{color}" fill-opacity=".13" stroke="{color}" stroke-opacity=".48"/>',
            f'<text x="128" y="102" text-anchor="middle" class="small" fill="{color}">{esc(project["theme"])}</text>',
            f'<text x="52" y="285" class="display">{esc(project["name"])}</text>',
            f'<text x="54" y="326" class="body">{esc(ellipsize(project["desc"], 68))}</text>',
            f'<text x="54" y="368" class="mono">{esc(ellipsize(project["stack"].upper(), 58))}</text>',
            '<path d="M54 392 H1146" stroke="url(#signal)" stroke-width="3" stroke-linecap="round" class="dash"/>',
        ]
    )
    parts.extend(project_art(index, color))
    return svg_close(parts)


def make_research_observatory() -> str:
    """Build the research centerpiece around the conceptual generated artwork."""
    image_data = base64.b64encode(RESEARCH_SOURCE.read_bytes()).decode("ascii")
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1200" height="600" viewBox="0 0 1200 600" role="img" aria-labelledby="title desc">',
        '<title id="title">Quantum-enhanced generative models research note</title>',
        '<desc id="desc">Conceptual glass seed laboratory beside a concise, evidence-bounded summary of Goh Kun Ming’s HQCGAN research.</desc>',
        '<defs><linearGradient id="shade" x1="0" y1="0" x2="1" y2="0"><stop offset=".35" stop-color="#020617" stop-opacity="0"/><stop offset=".58" stop-color="#020617" stop-opacity=".8"/><stop offset="1" stop-color="#020617" stop-opacity=".99"/></linearGradient>',
        '<linearGradient id="line" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#38D9F5"/><stop offset=".55" stop-color="#A78BFA"/><stop offset="1" stop-color="#FB8B7B"/></linearGradient>',
        '<filter id="rg" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
        '<clipPath id="rc"><rect width="1200" height="600" rx="30"/></clipPath>',
        "<style><![CDATA[.rt{font:800 45px Inter,Segoe UI,Arial,sans-serif;fill:#F8FAFC;letter-spacing:-1.4px}.rb{font:500 16px Inter,Segoe UI,Arial,sans-serif;fill:#C2CCE1}.rm{font:700 12px JetBrains Mono,Consolas,monospace;fill:#C8F8FF;letter-spacing:1.35px}.dash{stroke-dasharray:8 12;animation:d 13s linear infinite}.pulse{animation:p 3.6s ease-in-out infinite;transform-box:fill-box;transform-origin:center}@keyframes d{to{stroke-dashoffset:-360}}@keyframes p{0%,100%{opacity:.45;transform:scale(.9)}50%{opacity:1;transform:scale(1.12)}}@media(prefers-reduced-motion:reduce){*{animation:none!important}}]]></style></defs>",
        '<g clip-path="url(#rc)">',
        f'<image width="1200" height="600" preserveAspectRatio="xMidYMid slice" xlink:href="data:image/png;base64,{image_data}"/>',
        '<rect width="1200" height="600" fill="url(#shade)"/>',
        '<path d="M72 510 C250 438 360 548 542 478 S812 426 1138 470" fill="none" stroke="url(#line)" stroke-width="3" stroke-opacity=".48" class="dash"/>',
        '<circle cx="198" cy="474" r="7" fill="#38D9F5" filter="url(#rg)" class="pulse"/><circle cx="514" cy="488" r="7" fill="#A78BFA" filter="url(#rg)" class="pulse"/>',
        '<text x="698" y="78" class="rm">RESEARCH NOTE / ARXIV 2508.09209</text>',
        '<text x="696" y="145" class="rt">Quantum-enhanced</text><text x="696" y="198" class="rt">generative models</text>',
        '<text x="698" y="246" class="rb">A reproducible comparison—not a victory lap.</text>',
        '<text x="698" y="273" class="rb">The classical baseline led overall.</text>',
    ]
    metrics = [
        ("CLASSICAL BASELINE", "comparison anchor", THEME["cyan"]),
        ("3 · 5 · 7 QUBITS", "hybrid variants", THEME["purple"]),
        ("BINARY MNIST", "digits 0 and 1", THEME["coral"]),
        ("FID + KID", "image quality", THEME["green"]),
    ]
    for index, (label, note, color) in enumerate(metrics):
        x = 698 + (index % 2) * 224
        y = 310 + (index // 2) * 84
        parts.extend(
            [
                f'<rect x="{x}" y="{y}" width="206" height="66" rx="16" fill="#0A1021" fill-opacity=".86" stroke="{color}" stroke-opacity=".42"/>',
                f'<text x="{x + 15}" y="{y + 26}" class="rm" fill="{color}">{label}</text>',
                f'<text x="{x + 15}" y="{y + 49}" class="rb">{note}</text>',
            ]
        )
    parts.extend(
        [
            '<text x="698" y="511" class="rb">Tests · configs · paper source · documented limitations</text>',
            '<text x="698" y="552" class="rm">CONCEPTUAL VISUAL · RESULTS LIVE IN THE PAPER</text>',
            '</g><rect x="1" y="1" width="1198" height="598" rx="29" fill="none" stroke="#A9B8D4" stroke-opacity=".2"/>',
        ]
    )
    return svg_close(parts)


def make_craft_map() -> str:
    """Build a compact map of the tools used across the making process."""
    stages = [
        ("01", "Ask", "Data · notebooks · baselines", THEME["cyan"]),
        ("02", "Model", "PyTorch · TensorFlow · Qiskit", THEME["purple"]),
        ("03", "Shape", "Python · FastAPI · React · Plotly", THEME["coral"]),
        ("04", "Ship", "pytest · Actions · Docker · Playwright", THEME["green"]),
    ]
    parts = svg_open(
        470,
        "Craft map from question to shipped artifact",
        "Four connected stages and representative tools used to ask, model, shape, and ship projects.",
    )
    parts.extend(
        [
            '<text x="54" y="62" class="section">The craft map</text>',
            '<text x="54" y="93" class="body">Tools are supporting characters. The through-line is the way the work gets made.</text>',
            '<path d="M118 258 C252 144 366 352 506 238 S744 142 874 248 S1044 340 1120 218" class="mesh dash" stroke-width="4"/>',
        ]
    )
    for index, (number, title, tools_text, color) in enumerate(stages):
        x = 54 + index * 286
        y = 146 if index % 2 == 0 else 226
        parts.extend(
            [
                f'<g class="{"driftA" if index % 2 == 0 else "driftB"}">',
                f'<rect x="{x}" y="{y}" width="250" height="150" rx="24" class="glassBright" filter="url(#soft)"/>',
                f'<circle cx="{x + 30}" cy="{y + 31}" r="10" fill="{color}" filter="url(#glow)" class="pulse"/>',
                f'<text x="{x + 52}" y="{y + 36}" class="mono">{number}</text>',
                f'<text x="{x + 24}" y="{y + 81}" class="section">{title}</text>',
            ]
        )
        parts.extend(text_block(wrap(tools_text, 28), x + 24, y + 112, 21, "small"))
        parts.append("</g>")
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
        "studio-manifesto.svg": make_manifesto(),
        "research-observatory.svg": make_research_observatory(),
        "craft-map.svg": make_craft_map(),
        "signal-footer.svg": make_signal_footer(),
    }
    for index, project in enumerate(PROFILE["projects"][:6]):
        generated[f"project-{index + 1:02d}-{project['repo']}.svg"] = make_project_specimen(
            project, index
        )
    for filename, content in generated.items():
        (ASSETS / filename).write_text(content + "\n", encoding="utf-8")
        print(f"wrote {ASSETS / filename}")


if __name__ == "__main__":
    main()
