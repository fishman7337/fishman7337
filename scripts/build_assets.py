#!/usr/bin/env python3
'''Generate animated SVG assets for the fishman7337 GitHub profile README.

Primary edit path:
  1. Edit content/profile.yml
  2. Run: python scripts/build_assets.py

Direct SVG edit path:
  - Open assets/*.svg in VS Code, Figma, Illustrator, or Inkscape.
  - Text remains as real <text> elements, not outlined paths.
  - Major text groups and layers have stable ids like edit-hero-name or edit-project-hqcgan.
'''
from __future__ import annotations

from pathlib import Path
import html
import math
import textwrap
import yaml

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
DATA = yaml.safe_load((ROOT / 'content' / 'profile.yml').read_text(encoding='utf-8'))
T = DATA['theme']
I = DATA['identity']

ASSETS.mkdir(exist_ok=True)


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def wrap(text: str, width: int = 42) -> list[str]:
    return textwrap.wrap(str(text), width=width, break_long_words=False, replace_whitespace=False)


def ellipsize(text: str, max_chars: int) -> str:
    text = str(text)
    return text if len(text) <= max_chars else text[: max_chars - 1].rstrip() + '…'


def svg_header(width: int, height: int, title: str, desc: str = '') -> str:
    tpl = '''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{esc(title)}</title>
<desc id="desc">{esc(desc or title)}</desc>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{T['bg0']}"/>
    <stop offset="48%" stop-color="{T['bg1']}"/>
    <stop offset="100%" stop-color="#111827"/>
  </linearGradient>
  <linearGradient id="panelGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{T['panel']}" stop-opacity="0.98"/>
    <stop offset="100%" stop-color="{T['panel2']}" stop-opacity="0.92"/>
  </linearGradient>
  <linearGradient id="neon" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{T['cyan']}"/>
    <stop offset="45%" stop-color="{T['purple']}"/>
    <stop offset="100%" stop-color="{T['pink']}"/>
  </linearGradient>
  <linearGradient id="greenGrad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{T['green']}"/>
    <stop offset="100%" stop-color="{T['cyan']}"/>
  </linearGradient>
  <linearGradient id="amberGrad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{T['amber']}"/>
    <stop offset="100%" stop-color="{T['pink']}"/>
  </linearGradient>
  <linearGradient id="glassGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#17233C" stop-opacity="0.92"/>
    <stop offset="100%" stop-color="#06131B" stop-opacity="0.86"/>
  </linearGradient>
  <linearGradient id="scanGrad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{T['cyan']}" stop-opacity="0"/>
    <stop offset="52%" stop-color="{T['cyan']}" stop-opacity="0.24"/>
    <stop offset="100%" stop-color="{T['cyan']}" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="orbGlow" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="{T['cyan']}" stop-opacity="0.85"/>
    <stop offset="65%" stop-color="{T['purple']}" stop-opacity="0.16"/>
    <stop offset="100%" stop-color="{T['purple']}" stop-opacity="0"/>
  </radialGradient>
  <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="6" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="cardShadow" x="-30%" y="-30%" width="160%" height="160%">
    <feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#020617" flood-opacity="0.50"/>
  </filter>
  <pattern id="grid" width="44" height="44" patternUnits="userSpaceOnUse">
    <path d="M 44 0 L 0 0 0 44" fill="none" stroke="{T['cyan']}" stroke-opacity="0.065" stroke-width="1"/>
  </pattern>
  <pattern id="microGrid" width="12" height="12" patternUnits="userSpaceOnUse">
    <path d="M 12 0 L 0 0 0 12" fill="none" stroke="{T['green']}" stroke-opacity="0.045" stroke-width="1"/>
  </pattern>
  <style><![CDATA[
    .bg { fill: url(#bg); }
    .grid { fill: url(#grid); opacity: .95; }
    .microGrid { fill: url(#microGrid); opacity: .70; }
    .title { font-family: Inter, ui-sans-serif, system-ui, Segoe UI, Arial, sans-serif; font-weight: 900; letter-spacing: 0; fill: {T['text']}; }
    .subtitle { font-family: Inter, ui-sans-serif, system-ui, Segoe UI, Arial, sans-serif; font-weight: 700; fill: {T['cyan']}; }
    .body { font-family: Inter, ui-sans-serif, system-ui, Segoe UI, Arial, sans-serif; fill: {T['muted']}; }
    .mono { font-family: JetBrains Mono, SFMono-Regular, Consolas, Monaco, monospace; fill: {T['text']}; }
    .label { font-family: JetBrains Mono, SFMono-Regular, Consolas, Monaco, monospace; font-weight: 800; fill: {T['cyan']}; }
    .muted { fill: {T['muted']}; }
    .tiny { font-size: 18px; }
    .small { font-size: 22px; }
    .medium { font-size: 28px; }
    .large { font-size: 46px; }
    .huge { font-size: 72px; }
    .chip { fill: rgba(15, 23, 42, .78); stroke: {T['cyan']}; stroke-opacity: .35; }
    .panel { fill: url(#panelGrad); stroke: {T['cyan']}; stroke-opacity: .22; filter: url(#cardShadow); }
    .glass { fill: url(#glassGrad); stroke: {T['cyan']}; stroke-opacity: .24; filter: url(#cardShadow); }
    .hairline { stroke: {T['cyan']}; stroke-opacity: .28; stroke-width: 1.3; fill: none; }
    .faintLine { stroke: {T['muted']}; stroke-opacity: .18; stroke-width: 1; fill: none; }
    .neonStroke { stroke: url(#neon); stroke-width: 3; fill: none; filter: url(#softGlow); }
    .glowText { fill: url(#neon); filter: url(#softGlow); }
    .pulse { animation: pulse 2.8s ease-in-out infinite; transform-origin: center; transform-box: fill-box; }
    .floatA { animation: floatA 8s ease-in-out infinite; transform-box: fill-box; }
    .floatB { animation: floatB 10s ease-in-out infinite; transform-box: fill-box; }
    .spinSlow { animation: spin 24s linear infinite; transform-origin: center; transform-box: fill-box; }
    .spinReverse { animation: spinReverse 32s linear infinite; transform-origin: center; transform-box: fill-box; }
    .dash { fill: none; stroke-dasharray: 16 18; animation: dash 12s linear infinite; }
    .scan { animation: scan 6s ease-in-out infinite; }
    .blink { animation: blink 1.2s steps(2, end) infinite; }
    .bar { transform-origin: left center; transform-box: fill-box; animation: barLoad 3.2s ease-out both; }
    .twinkle { animation: twinkle 3s ease-in-out infinite; }
    .wave { animation: wave 7s ease-in-out infinite alternate; }
    .fadeSlide { animation: fadeSlide 5s ease-in-out infinite; }
    @keyframes pulse { 0%,100% { opacity:.55; transform:scale(1); } 50% { opacity:1; transform:scale(1.055); } }
    @keyframes floatA { 0%,100% { transform:translateY(0px); } 50% { transform:translateY(-14px); } }
    @keyframes floatB { 0%,100% { transform:translateY(0px); } 50% { transform:translateY(12px); } }
    @keyframes spin { from { transform:rotate(0deg); } to { transform:rotate(360deg); } }
    @keyframes spinReverse { from { transform:rotate(360deg); } to { transform:rotate(0deg); } }
    @keyframes dash { to { stroke-dashoffset:-280; } }
    @keyframes scan { 0%,100% { transform:translateY(-120px); opacity:0; } 25%,70% { opacity:.50; } 50% { transform:translateY(740px); opacity:.20; } }
    @keyframes blink { 0%,45% { opacity: 1; } 46%,100% { opacity: 0; } }
    @keyframes barLoad { from { transform:scaleX(.08); } to { transform:scaleX(1); } }
    @keyframes twinkle { 0%,100% { opacity:.25; } 50% { opacity:1; } }
    @keyframes wave { from { transform: translateX(-20px); } to { transform: translateX(20px); } }
    @keyframes fadeSlide { 0%,100% { opacity:.28; transform:translateX(-12px); } 50% { opacity:.75; transform:translateX(12px); } }
    @media (prefers-reduced-motion: reduce) { * { animation: none !important; } }
  ]]></style>
</defs>
'''
    replacements = {
        '{width}': str(width),
        '{height}': str(height),
        '{esc(title)}': esc(title),
        '{esc(desc or title)}': esc(desc or title),
        "{T['bg0']}": T['bg0'],
        "{T['bg1']}": T['bg1'],
        "{T['panel']}": T['panel'],
        "{T['panel2']}": T['panel2'],
        "{T['cyan']}": T['cyan'],
        "{T['purple']}": T['purple'],
        "{T['pink']}": T['pink'],
        "{T['green']}": T['green'],
        "{T['amber']}": T['amber'],
        "{T['blue']}": T['blue'],
        "{T['text']}": T['text'],
        "{T['muted']}": T['muted'],
    }
    for k, v in replacements.items():
        tpl = tpl.replace(k, str(v))
    return tpl


def svg_footer() -> str:
    return '</svg>\n'


def bg(width: int, height: int) -> str:
    # Lightweight deterministic starfield and trace layer: GitHub-safe, no external assets.
    stars = []
    traces = []
    for i in range(1, 56):
        x = (i * 137) % width
        y = (i * 83) % height
        r = 1 + (i % 3) * 0.65
        color = [T['cyan'], T['purple'], T['green'], T['pink']][i % 4]
        stars.append(f'<circle class="twinkle" cx="{x}" cy="{y}" r="{r:.1f}" fill="{color}" opacity="0.45" style="animation-delay:{(i%9)*.25:.2f}s"/>')
    for i in range(14):
        x = 72 + (i * 113) % max(200, width - 160)
        y = 104 + (i * 71) % max(180, height - 180)
        w = 42 + (i % 4) * 26
        h = 18 + (i % 3) * 12
        color = [T['cyan'], T['green'], T['purple'], T['amber']][i % 4]
        traces.append(
            f'<path d="M{x} {y} h{w} v{h} h{w//2}" fill="none" stroke="{color}" '
            f'stroke-opacity="0.13" stroke-width="1.2"/>'
        )
    return f'''<rect width="{width}" height="{height}" fill="{T['bg0']}"/>
<rect class="bg" width="{width}" height="{height}" rx="28"/>
<rect class="grid" width="{width}" height="{height}" rx="28"/>
<rect class="microGrid" width="{width}" height="{height}" rx="28"/>
<path d="M0 0 H{width} V126 C{int(width*.75)} 96 {int(width*.60)} 136 {int(width*.38)} 104 C{int(width*.20)} 78 {int(width*.12)} 112 0 78 Z" fill="url(#neon)" opacity="0.055"/>
<path d="M0 {height-120} C{int(width*.22)} {height-58} {int(width*.42)} {height-160} {int(width*.68)} {height-92} C{int(width*.82)} {height-56} {int(width*.92)} {height-118} {width} {height-82} V{height} H0 Z" fill="url(#greenGrad)" opacity="0.05"/>
<g opacity="0.42">{''.join(stars)}</g>
<g id="ambient-circuit-traces">{''.join(traces)}</g>
<path d="M28 92 V28 H92 M{width-92} 28 H{width-28} V92 M28 {height-92} V{height-28} H92 M{width-92} {height-28} H{width-28} V{height-92}" fill="none" stroke="url(#neon)" stroke-width="4" stroke-linecap="round" opacity="0.62"/>
<rect class="scan" x="0" y="0" width="{width}" height="136" fill="url(#scanGrad)" opacity="0.42"/>
'''


def pill(x, y, label, width=None, fill='rgba(15,23,42,.72)', stroke=None, cls='mono', fs=18):
    width = width or max(120, len(label) * fs * 0.66 + 34)
    stroke = stroke or T['cyan']
    return f'''<g>
<rect x="{x}" y="{y}" width="{width:.0f}" height="38" rx="19" fill="{fill}" stroke="{stroke}" stroke-opacity="0.36"/>
<text x="{x+width/2:.0f}" y="{y+25}" text-anchor="middle" class="{cls}" font-size="{fs}" font-weight="700">{esc(label)}</text>
</g>'''


def card(x, y, w, h, rx=26, opacity=1):
    return f'<rect class="panel" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" opacity="{opacity}"/>'


def section_head(section: str, title: str, subtitle: str, code: str = '') -> str:
    code_svg = ''
    if code:
        code_svg = f'''<rect x="70" y="44" width="{max(150, len(code) * 13 + 36)}" height="32" rx="16" fill="rgba(2,6,23,.70)" stroke="{T['green']}" stroke-opacity="0.34"/>
<text id="edit-{section}-code" x="90" y="66" class="label" font-size="14" fill="{T['green']}">{esc(code)}</text>'''
    return f'''<g id="edit-{section}-header">
{code_svg}
<text id="edit-{section}-title" x="70" y="108" class="title large">{esc(title)}</text>
<text id="edit-{section}-subtitle" x="72" y="143" class="body small">{esc(subtitle)}</text>
<path d="M72 158 H510" class="hairline"/>
</g>'''


def ring_gauge(cx: float, cy: float, r: float, score: int, color: str) -> str:
    circumference = 2 * math.pi * r
    fill_len = circumference * max(0, min(score, 100)) / 100
    return f'''<circle cx="{cx}" cy="{cy}" r="{r}" fill="rgba(2,6,23,.68)" stroke="{T['muted']}" stroke-opacity="0.18" stroke-width="6"/>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="6" stroke-linecap="round" stroke-dasharray="{fill_len:.1f} {circumference:.1f}" transform="rotate(-90 {cx} {cy})"/>'''


def mini_meter(x: float, y: float, values: list[int], color: str, width: int = 118) -> str:
    bars = []
    step = width / max(1, len(values))
    for idx, val in enumerate(values):
        h = 10 + val % 32
        bars.append(f'<rect class="bar" x="{x + idx*step:.1f}" y="{y + 42 - h}" width="{max(3, step-5):.1f}" height="{h}" rx="2" fill="{color}" opacity="{0.36 + (idx % 3) * 0.13:.2f}" style="animation-delay:{idx*.04:.2f}s"/>')
    return ''.join(bars)


def metric_card(x: float, y: float, value: str, label: str, color: str, w: int = 150) -> str:
    return f'''<g>
<rect x="{x}" y="{y}" width="{w}" height="50" rx="15" fill="rgba(16,26,53,.72)" stroke="{color}" stroke-opacity="0.32"/>
<text x="{x+18}" y="{y+22}" class="title" font-size="22">{esc(value)}</text>
<text x="{x+18}" y="{y+40}" class="mono" font-size="11" fill="{T["muted"]}">{esc(label)}</text>
</g>'''


def make_hero() -> str:
    width, height = 1600, 640
    chips = DATA['signals']
    metrics = DATA['metrics']
    s = [svg_header(width, height, f"{I['name']} cyberdeck profile banner", 'Animated GitHub profile hero banner'), bg(width, height)]
    s.append('<g id="layer-background-orbits" opacity="0.78">')
    s.append(f'<circle class="spinSlow" cx="1230" cy="316" r="194" fill="none" stroke="{T["purple"]}" stroke-opacity="0.28" stroke-width="2" stroke-dasharray="12 18"/>')
    s.append(f'<circle class="spinReverse" cx="1230" cy="316" r="248" fill="none" stroke="{T["cyan"]}" stroke-opacity="0.18" stroke-width="2" stroke-dasharray="6 22"/>')
    s.append(f'<circle cx="1230" cy="316" r="310" fill="url(#orbGlow)" opacity="0.20"/>')
    s.append('</g>')

    s.append('<g id="edit-hero-main-copy">')
    s.append(f'<path d="M52 74 V520" stroke="url(#neon)" stroke-width="5" stroke-linecap="round" opacity="0.74"/>')
    s.append(pill(72, 66, f"{I['username']} // PROFILE README OS", width=430, fs=18))
    s.append(f'<text id="edit-hero-name" x="72" y="160" class="title huge">{esc(I["name"])}</text>')
    s.append(f'<text id="edit-hero-username" x="76" y="205" class="mono medium" fill="{T["cyan"]}">@{esc(I["username"])}</text>')
    for idx, line in enumerate(wrap(I['tagline'], 56)[:2]):
        s.append(f'<text id="edit-hero-tagline-{idx+1}" x="72" y="{262+idx*34}" class="body small">{esc(line)}</text>')
    s.append(f'<text id="edit-hero-role" x="72" y="350" class="subtitle medium">{esc(I["role"])}</text>')
    s.append(f'<text id="edit-hero-edu" x="72" y="388" class="body small">{esc(I["education"])}</text>')

    x, y = 72, 430
    for i, ch in enumerate(chips):
        w = max(132, len(ch) * 13 + 42)
        if x + w > 760:
            x, y = 72, y + 52
        s.append(pill(x, y, ch, width=w, fs=17, stroke=[T['cyan'], T['purple'], T['green'], T['pink']][i % 4]))
        x += w + 14
    s.append(f'<text id="edit-hero-motto" x="76" y="535" class="mono" font-size="17" fill="{T["muted"]}">{esc(I["motto"])}</text>')
    s.append('</g>')

    # metric cards
    s.append('<g id="edit-hero-metrics">')
    metric_items = [(metrics['public_repositories'], 'PUBLIC REPOS'), (metrics['arxiv_preprints'], 'ARXIV PREPRINT'), (metrics['base'], 'BASE'), (metrics['focus'], 'FOCUS')]
    for i, (val, label) in enumerate(metric_items):
        mx = 72 + i * 178
        s.append(metric_card(mx, 558, val, label, [T["cyan"],T["purple"],T["green"],T["amber"]][i], w=152))
    s.append('</g>')

    # Right cockpit
    s.append('<g id="edit-hero-cockpit" class="floatA">')
    s.append(card(930, 82, 590, 468, 34))
    s.append(f'<rect x="960" y="116" width="530" height="58" rx="20" fill="rgba(6,11,24,.78)" stroke="{T["cyan"]}" stroke-opacity="0.20"/>')
    s.append(f'<text id="edit-hero-cockpit-title" x="988" y="151" class="mono" font-size="21" font-weight="900" fill="{T["cyan"]}">LIVE RESEARCH STACK</text>')
    s.append(f'<circle cx="1462" cy="144" r="8" fill="{T["green"]}"/>')
    s.append(f'<text x="1410" y="151" class="mono" font-size="15" fill="{T["green"]}">ONLINE</text>')

    # central orb and nodes
    s.append(f'<circle cx="1228" cy="318" r="112" fill="rgba(56,189,248,.10)" stroke="url(#neon)" stroke-width="3"/>')
    s.append('<g id="edit-hero-core-node" class="pulse">')
    s.append(f'<circle cx="1228" cy="318" r="74" fill="rgba(167,139,250,.10)" stroke="{T["purple"]}" stroke-opacity="0.46"/>')
    s.append(f'<text id="edit-hero-core" x="1228" y="304" text-anchor="middle" class="title" font-size="32">AI SYSTEMS</text>')
    s.append(f'<text x="1228" y="338" text-anchor="middle" class="mono" font-size="18" fill="{T["muted"]}">R&amp;D | CV | QML | MLOps</text>')
    s.append('</g>')
    nodes = [('QML', 1082, 222, T['purple']), ('CV', 1390, 230, T['cyan']), ('MLOps', 1390, 414, T['green']), ('Trust', 1084, 414, T['amber'])]
    for idx, (label, nx, ny, color) in enumerate(nodes):
        s.append(f'<path class="dash" d="M1228 318 L{nx} {ny}" stroke="{color}" stroke-opacity="0.36" stroke-width="2"/>')
        s.append(f'<g id="edit-hero-node-group-{idx+1}" class="pulse" style="animation-delay:{idx*.35:.2f}s">')
        s.append(f'<circle cx="{nx}" cy="{ny}" r="38" fill="rgba(15,23,42,.88)" stroke="{color}" stroke-width="2"/>')
        s.append(f'<text id="edit-hero-node-{idx+1}" x="{nx}" y="{ny+7}" text-anchor="middle" class="mono" font-size="17" font-weight="800">{esc(label)}</text>')
        s.append('</g>')
    # terminal strip
    s.append(f'<rect x="975" y="466" width="500" height="62" rx="18" fill="rgba(2,6,23,.82)" stroke="{T["green"]}" stroke-opacity="0.22"/>')
    s.append(f'<text id="edit-hero-terminal-1" x="1000" y="493" class="mono" font-size="16" fill="{T["green"]}">$ build --truth-grounded --readme-ready</text>')
    s.append(f'<text id="edit-hero-terminal-2" x="1000" y="516" class="mono" font-size="14" fill="{T["muted"]}">status: reproducible portfolio system ready</text>')
    s.append(f'<g id="edit-hero-signal-meters" opacity="0.92">')
    signal_rows = [('eval', 988, 206, T['cyan'], [8, 19, 31, 22, 35, 26, 40]), ('docs', 1368, 206, T['green'], [18, 11, 28, 33, 25, 38, 29]), ('ops', 988, 384, T['amber'], [25, 34, 21, 39, 28, 31, 42]), ('risk', 1368, 384, T['pink'], [16, 24, 12, 35, 18, 29, 22])]
    for label, mx, my, color, vals in signal_rows:
        s.append(f'<text x="{mx}" y="{my-12}" class="label" font-size="13" fill="{color}">{label.upper()}</text>')
        s.append(mini_meter(mx, my, vals, color, width=68))
    s.append('</g>')
    s.append('</g>')

    # bottom animated data bars
    s.append('<g id="hero-waveform" opacity="0.70">')
    for i in range(58):
        x = 830 + i * 11
        h = 18 + (i * 37 % 58)
        color = [T['cyan'], T['purple'], T['green']][i % 3]
        s.append(f'<rect class="bar" x="{x}" y="{604-h}" width="6" height="{h}" rx="3" fill="{color}" opacity="0.45" style="animation-delay:{i*.015:.2f}s"/>')
    s.append('</g>')
    s.append(svg_footer())
    return '\n'.join(s)


def make_mission() -> str:
    width, height = 1600, 660
    cards = DATA['mission_cards']
    s = [svg_header(width, height, 'Mission control HUD', 'Animated mission control board'), bg(width, height)]
    s.append(section_head('mission', 'Mission Control', 'Research questions, baselines, systems delivery, and responsible release practices in one operating loop.', 'OPS LOOP'))
    # center pipeline line
    s.append('<g id="edit-mission-pipeline">')
    y = 470
    steps = ['Question', 'Baseline', 'Experiment', 'Evaluate', 'Harden', 'Ship']
    start, gap = 140, 260
    s.append(f'<path class="dash" d="M{start} {y} H{start + gap*(len(steps)-1)}" stroke="url(#neon)" stroke-width="4"/>')
    for i, step in enumerate(steps):
        x = start + i * gap
        s.append(f'<g id="edit-mission-step-group-{i+1}" class="pulse" style="animation-delay:{i*.18:.2f}s">')
        s.append(f'<circle cx="{x}" cy="{y}" r="22" fill="rgba(15,23,42,.96)" stroke="{[T["cyan"],T["purple"],T["green"],T["amber"],T["pink"],T["blue"]][i]}" stroke-width="3"/>')
        s.append(f'<text id="edit-mission-step-{i+1}" x="{x}" y="{y+58}" text-anchor="middle" class="mono" font-size="15" fill="{T["muted"]}">{esc(step)}</text>')
        s.append('</g>')
    s.append('</g>')

    # cards
    for i, c in enumerate(cards):
        x = 70 + i * 382
        y = 170
        color = [T['cyan'], T['purple'], T['green'], T['amber']][i]
        s.append(f'<g id="edit-mission-card-{i+1}" class="float{ "A" if i%2==0 else "B" }" style="animation-delay:{i*.2:.2f}s">')
        s.append(f'<rect x="{x}" y="{y}" width="340" height="230" rx="28" fill="url(#panelGrad)" stroke="{color}" stroke-opacity="0.34" filter="url(#cardShadow)"/>')
        s.append(ring_gauge(x+55, y+58, 31, int(c['score']), color))
        s.append(f'<text x="{x+55}" y="{y+66}" text-anchor="middle" class="mono" font-size="17" font-weight="900" fill="{color}">{esc(c["label"])}</text>')
        s.append(f'<text x="{x+104}" y="{y+52}" class="title" font-size="30">{esc(c["title"])}</text>')
        s.append(f'<text x="{x+104}" y="{y+84}" class="mono" font-size="13" fill="{T["muted"]}">EVIDENCE-LED TRACK</text>')
        # progress bar
        s.append(f'<rect x="{x+34}" y="{y+112}" width="272" height="14" rx="7" fill="rgba(2,6,23,.72)"/>')
        s.append(f'<rect class="bar" x="{x+34}" y="{y+112}" width="{272*int(c["score"])/100:.1f}" height="14" rx="7" fill="{color}" opacity="0.72"/>')
        yy = y + 158
        for j, line in enumerate(wrap(c['desc'], 36)[:3]):
            s.append(f'<text x="{x+34}" y="{yy+j*24}" class="body" font-size="18">{esc(line)}</text>')
        s.append('</g>')
    s.append(svg_footer())
    return '\n'.join(s)


def make_quantum_lab() -> str:
    width, height = 1600, 570
    r = DATA['research']
    s = [svg_header(width, height, 'HQCGAN quantum lab pipeline', 'Animated diagram explaining the HQCGAN research pipeline'), bg(width, height)]
    s.append(section_head('quantum', r['title'], f'{r["subtitle"]} | arXiv:{r["arxiv_id"]}', 'RESEARCH TRACE'))

    # pipeline boxes
    boxes = [
        ('Classical Baseline', 'GAN noise prior', 88, 214, 238, T['cyan']),
        ('Quantum Circuit', '3 / 5 / 7 qubits', 390, 214, 238, T['purple']),
        ('Latent Prior', 'Noisy sampling', 692, 214, 238, T['pink']),
        ('Generator', 'Digit synthesis', 994, 214, 238, T['green']),
        ('Evaluation', 'FID / KID', 1296, 214, 238, T['amber']),
    ]
    for i, (title, sub, x, y, w, color) in enumerate(boxes):
        s.append(f'<g id="edit-quantum-stage-{i+1}">')
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="140" rx="26" fill="url(#panelGrad)" stroke="{color}" stroke-opacity="0.42" filter="url(#cardShadow)"/>')
        s.append(f'<text x="{x+22}" y="{y+44}" class="title" font-size="22">{esc(title)}</text>')
        s.append(f'<text x="{x+22}" y="{y+78}" class="mono" font-size="18" fill="{color}">{esc(sub)}</text>')
        s.append(f'<text x="{x+22}" y="{y+112}" class="body" font-size="16">stage.{i+1:02d} / reproducible</text>')
        s.append('</g>')
        if i < len(boxes)-1:
            ax = x + w + 20
            s.append(f'<path class="dash" d="M{ax} {y+70} H{x+302-20}" stroke="url(#neon)" stroke-width="4"/>')
            s.append(f'<polygon points="{x+302-26},{y+62} {x+302-8},{y+70} {x+302-26},{y+78}" fill="{T["cyan"]}" opacity="0.8"/>')

    # quantum circuit detail panel
    s.append('<g id="edit-quantum-circuit-detail">')
    s.append(f'<rect x="92" y="386" width="660" height="126" rx="24" fill="rgba(2,6,23,.68)" stroke="{T["purple"]}" stroke-opacity="0.28"/>')
    for q in range(5):
        yy = 418 + q*18
        s.append(f'<line x1="132" y1="{yy}" x2="704" y2="{yy}" stroke="{T["muted"]}" stroke-opacity="0.32"/>')
        s.append(f'<text x="106" y="{yy+5}" class="mono" font-size="12" fill="{T["muted"]}">q{q}</text>')
        for g in range(5):
            gx = 188 + g*96 + (q%2)*20
            color = [T['cyan'], T['purple'], T['pink'], T['green'], T['amber']][(g+q)%5]
            s.append(f'<g class="pulse" style="animation-delay:{(g+q)*.08:.2f}s">')
            s.append(f'<rect x="{gx}" y="{yy-10}" width="38" height="20" rx="7" fill="rgba(15,23,42,.96)" stroke="{color}" stroke-width="1.5"/>')
            s.append(f'<text x="{gx+19}" y="{yy+5}" text-anchor="middle" class="mono" font-size="10" fill="{color}">R{(g+q)%3+1}</text>')
            s.append('</g>')
    s.append('</g>')

    # notes panel
    s.append('<g id="edit-quantum-notes">')
    s.append(f'<rect x="806" y="386" width="700" height="126" rx="24" fill="rgba(2,6,23,.68)" stroke="{T["green"]}" stroke-opacity="0.28"/>')
    s.append(f'<text x="836" y="424" class="subtitle" font-size="23">Research readout</text>')
    for i, line in enumerate(wrap(r['result_note'], 72)[:2]):
        s.append(f'<text id="edit-quantum-result-{i+1}" x="836" y="{456+i*25}" class="body" font-size="18">{esc(line)}</text>')
    badges = [('150 epochs', T['cyan']), ('Binary MNIST 0/1', T['purple']), ('FID + KID', T['amber']), ('Noise-aware', T['green'])]
    bx = 836
    for label, color in badges:
        w = max(112, len(label) * 10 + 34)
        s.append(f'<rect x="{bx}" y="490" width="{w}" height="28" rx="14" fill="rgba(15,23,42,.72)" stroke="{color}" stroke-opacity="0.30"/>')
        s.append(f'<text x="{bx+17}" y="509" class="mono" font-size="13" fill="{color}">{esc(label)}</text>')
        bx += w + 12
    s.append('</g>')
    s.append(svg_footer())
    return '\n'.join(s)


def make_project_nebula() -> str:
    width, height = 1600, 720
    projects = DATA['projects'][:10]
    s = [svg_header(width, height, 'Project nebula map', 'Animated project constellation showing public GitHub builds'), bg(width, height)]
    s.append(section_head('nebula', 'Project Nebula', 'A public build map across research, geospatial AI, MLOps, analytics, security, NLP, RL, and dashboards.', 'PUBLIC GRAPH'))
    # central core
    cx, cy = 800, 380
    s.append(f'<circle cx="{cx}" cy="{cy}" r="110" fill="url(#orbGlow)" opacity="0.35"/>')
    # positions chosen for zero label overlap
    coords = [(255,230),(555,205),(1045,205),(1340,245),(285,510),(560,606),(1055,606),(1325,525),(250,375),(1350,385)]
    colors = [T['purple'],T['cyan'],T['green'],T['amber'],T['pink'],T['blue'],T['green'],T['purple'],T['cyan'],T['amber']]
    for i, (p, (x,y), color) in enumerate(zip(projects, coords, colors)):
        s.append(f'<path class="dash" d="M{cx} {cy} C{(cx+x)//2} {cy}, {(cx+x)//2} {y}, {x} {y}" stroke="{color}" stroke-opacity="0.30" stroke-width="2"/>')
    s.append('<g id="edit-nebula-core-node" class="pulse">')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="78" fill="rgba(15,23,42,.94)" stroke="url(#neon)" stroke-width="4"/>')
    s.append(f'<text id="edit-nebula-core" x="{cx}" y="{cy-8}" text-anchor="middle" class="title" font-size="32">fishman7337</text>')
    s.append(f'<text x="{cx}" y="{cy+24}" text-anchor="middle" class="mono" font-size="17" fill="{T["muted"]}">AI portfolio graph</text>')
    s.append('</g>')
    for i, (p, (x,y), color) in enumerate(zip(projects, coords, colors)):
        bw = 300 if len(p['name']) > 18 else 280
        bh = 108
        bx, by = x - bw/2, y - bh/2
        s.append(f'<g id="edit-project-{i+1}" class="float{ "A" if i%2==0 else "B" }" style="animation-delay:{i*.12:.2f}s">')
        s.append(f'<rect x="{bx:.0f}" y="{by:.0f}" width="{bw}" height="{bh}" rx="22" fill="rgba(16,26,53,.92)" stroke="{color}" stroke-opacity="0.42" filter="url(#cardShadow)"/>')
        s.append(f'<circle cx="{bx+32:.0f}" cy="{by+32:.0f}" r="12" fill="{color}" opacity="0.85"/>')
        name_lines = wrap(p['name'], 20)[:2]
        for j, line in enumerate(name_lines):
            s.append(f'<text id="edit-project-name-{i+1}-{j+1}" x="{bx+54:.0f}" y="{by+31+j*20:.0f}" class="title" font-size="18">{esc(line)}</text>')
        s.append(f'<text id="edit-project-theme-{i+1}" x="{bx+54:.0f}" y="{by+72:.0f}" class="mono" font-size="14" fill="{color}">{esc(ellipsize(p["theme"], 24))}</text>')
        s.append(f'<text x="{bx+54:.0f}" y="{by+94:.0f}" class="body" font-size="12">{esc(ellipsize(p["repo"], 30))}</text>')
        s.append('</g>')
    s.append(svg_footer())
    return '\n'.join(s)


def make_skill_constellation() -> str:
    width, height = 1600, 1060
    skills = DATA['skills']
    s = [svg_header(width, height, 'Skill constellation matrix', 'Animated technology and capability matrix'), bg(width, height)]
    s.append(section_head('skills', 'Technical Stack', 'A practical stack for reproducible experiments, applied AI products, data systems, and trustworthy deployment.', 'CAPABILITY MATRIX'))
    colors = [T['cyan'], T['purple'], T['green'], T['amber'], T['pink'], T['blue']]
    x0, y0 = 70, 170
    cw, ch = 470, 250
    gapx, gapy = 35, 30
    for idx, (domain, items) in enumerate(skills.items()):
        row, col = divmod(idx, 3)
        x = x0 + col * (cw + gapx)
        y = y0 + row * (ch + gapy)
        color = colors[idx % len(colors)]
        s.append(f'<g id="edit-skill-domain-{idx+1}" class="float{ "A" if idx%2==0 else "B" }" style="animation-delay:{idx*.1:.2f}s">')
        s.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="28" fill="url(#panelGrad)" stroke="{color}" stroke-opacity="0.36" filter="url(#cardShadow)"/>')
        s.append(f'<text id="edit-skill-title-{idx+1}" x="{x+30}" y="{y+42}" class="title" font-size="27">{esc(domain)}</text>')
        s.append(mini_meter(x+335, y+25, [18+idx*3, 29, 22+idx*2, 35, 27, 40], color, width=92))
        for j, item in enumerate(items):
            chip_x = x + 30 + (j % 2) * 205
            chip_y = y + 68 + (j // 2) * 34
            w = 188
            s.append(f'<rect x="{chip_x}" y="{chip_y}" width="{w}" height="28" rx="14" fill="rgba(2,6,23,.58)" stroke="{color}" stroke-opacity="0.24"/>')
            s.append(f'<text id="edit-skill-{idx+1}-{j+1}" x="{chip_x+14}" y="{chip_y+19}" class="mono" font-size="12" fill="{T["text"]}">{esc(ellipsize(item, 21))}</text>')
        s.append('</g>')
    s.append(svg_footer())
    return '\n'.join(s)


def make_timeline() -> str:
    width, height = 1600, 560
    items = DATA['timeline']
    s = [svg_header(width, height, 'Timeline roadmap', 'Animated roadmap timeline'), bg(width, height)]
    s.append(section_head('roadmap', 'Roadmap / Build Log', 'The through-line: post evidence, harden systems, and keep claims bounded by reproducible work.', 'BUILD HISTORY'))
    yline = 340
    s.append(f'<rect x="86" y="{yline-38}" width="1428" height="76" rx="38" fill="rgba(2,6,23,.34)" stroke="{T["cyan"]}" stroke-opacity="0.12"/>')
    s.append(f'<path class="dash" d="M180 {yline} H1420" stroke="url(#neon)" stroke-width="5"/>')
    colors = [T['cyan'], T['purple'], T['green'], T['amber']]
    xs = [230, 610, 990, 1335]
    for i, item in enumerate(items):
        x = xs[i]
        color = colors[i]
        s.append(f'<g id="edit-timeline-item-{i+1}">')
        s.append(f'<g id="edit-timeline-marker-{i+1}" class="pulse" style="animation-delay:{i*.25:.2f}s">')
        s.append(f'<circle cx="{x}" cy="{yline}" r="26" fill="rgba(15,23,42,.94)" stroke="{color}" stroke-width="4"/>')
        s.append(f'<text id="edit-timeline-date-{i+1}" x="{x}" y="{yline+6}" text-anchor="middle" class="mono" font-size="15" font-weight="900" fill="{color}">{esc(item["date"])}</text>')
        s.append('</g>')
        bx = x - 175
        by = 180 if i % 2 == 0 else 430
        s.append(f'<rect x="{bx}" y="{by}" width="350" height="120" rx="24" fill="rgba(16,26,53,.91)" stroke="{color}" stroke-opacity="0.36" filter="url(#cardShadow)"/>')
        s.append(f'<text id="edit-timeline-title-{i+1}" x="{bx+24}" y="{by+39}" class="title" font-size="24">{esc(item["title"])}</text>')
        for j, line in enumerate(wrap(item['desc'], 40)[:2]):
            s.append(f'<text id="edit-timeline-desc-{i+1}-{j+1}" x="{bx+24}" y="{by+72+j*23}" class="body" font-size="16">{esc(line)}</text>')
        s.append('</g>')
    s.append(svg_footer())
    return '\n'.join(s)


def make_terminal_lab() -> str:
    width, height = 1600, 560
    s = [svg_header(width, height, 'Terminal lab card', 'Animated terminal simulation card'), bg(width, height)]
    s.append(section_head('terminal', 'Research Terminal', 'A cinematic boot sequence for reproducible experiments, docs, evaluation, and contact routes.', 'BOOT LOG'))
    # terminal window
    s.append(f'<rect x="100" y="165" width="1400" height="330" rx="28" fill="rgba(2,6,23,.88)" stroke="{T["cyan"]}" stroke-opacity="0.30" filter="url(#cardShadow)"/>')
    s.append(f'<rect x="100" y="165" width="1400" height="54" rx="28" fill="rgba(16,26,53,.95)"/>')
    for i, color in enumerate(['#FF5F56','#FFBD2E','#27C93F']):
        s.append(f'<circle cx="{138+i*34}" cy="192" r="10" fill="{color}"/>')
    s.append(f'<text x="238" y="199" class="mono" font-size="17" fill="{T["muted"]}">fishman7337@research-os:~/portfolio</text>')
    lines = [
        ('$ whoami', I['name'] + ' — ' + I['role']),
        ('$ cat focus.txt', 'Quantum GANs | CV/ROS | Data Viz | Neo4j | K8s/GCP MLOps'),
        ('$ run experiment --mode honest-baseline', 'baseline recorded · metrics tracked · claims bounded'),
        ('$ deploy portfolio --mode cyberdeck', 'profile visuals synced · checks passed · ready for review'),
        ('$ contact --linkedin --email', 'linkedin.com/in/goh-kun-ming-58573430a/ · ' + I['email']),
    ]
    y = 262
    for i, (cmd, out) in enumerate(lines):
        s.append(f'<text id="edit-terminal-cmd-{i+1}" x="140" y="{y+i*48}" class="mono" font-size="17" fill="{T["green"]}">{esc(ellipsize(cmd, 48))}</text>')
        s.append(f'<text id="edit-terminal-out-{i+1}" x="610" y="{y+i*48}" class="mono" font-size="15" fill="{T["text"]}">{esc(ellipsize(out, 86))}</text>')
    s.append(f'<rect class="blink" x="140" y="464" width="16" height="25" fill="{T["cyan"]}" opacity="0.9"/>')
    s.append(svg_footer())
    return '\n'.join(s)


def make_footer_wave() -> str:
    width, height = 1600, 260
    s = [svg_header(width, height, 'Footer wave', 'Animated footer wave'), bg(width, height)]
    s.append(f'<path d="M420 54 H1180" class="hairline" opacity="0.8"/>')
    s.append(f'<path class="wave" d="M-40 176 C220 106, 380 246, 620 176 C860 106, 1030 246, 1260 176 C1420 130, 1540 130, 1640 156 L1640 260 L-40 260 Z" fill="url(#neon)" opacity="0.26"/>')
    s.append(f'<path class="wave" d="M-40 202 C240 142, 420 250, 660 198 C880 150, 1050 230, 1268 190 C1440 160, 1540 164, 1640 190 L1640 260 L-40 260 Z" fill="{T["cyan"]}" opacity="0.14" style="animation-duration:10s"/>')
    s.append(f'<text id="edit-footer-motto" x="800" y="96" text-anchor="middle" class="title" font-size="38">{esc(I["motto"])}</text>')
    s.append(f'<text id="edit-footer-contact" x="800" y="139" text-anchor="middle" class="mono" font-size="18" fill="{T["muted"]}">@{esc(I["username"])} · {esc(I["location"])} · {esc(I["email"])}</text>')
    s.append(f'<rect x="586" y="160" width="428" height="34" rx="17" fill="rgba(2,6,23,.54)" stroke="{T["green"]}" stroke-opacity="0.25"/>')
    s.append(f'<text x="800" y="183" text-anchor="middle" class="label" font-size="14" fill="{T["green"]}">research | systems | responsible AI</text>')
    s.append(svg_footer())
    return '\n'.join(s)


def main() -> None:
    assets = {
        'hero-cyberdeck.svg': make_hero(),
        'mission-control.svg': make_mission(),
        'quantum-lab.svg': make_quantum_lab(),
        'project-nebula.svg': make_project_nebula(),
        'skill-constellation.svg': make_skill_constellation(),
        'timeline-roadmap.svg': make_timeline(),
        'terminal-lab.svg': make_terminal_lab(),
        'footer-wave.svg': make_footer_wave(),
    }
    for name, content in assets.items():
        (ASSETS / name).write_text(content, encoding='utf-8')
    print(f'Generated {len(assets)} SVG assets in {ASSETS}')


if __name__ == '__main__':
    main()
