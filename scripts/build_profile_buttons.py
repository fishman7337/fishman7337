#!/usr/bin/env python3
"""Generate polished local SVG buttons for the profile README."""
from __future__ import annotations

from pathlib import Path
import html
import re
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "profile-buttons"
OUT.mkdir(parents=True, exist_ok=True)


BUTTONS = [
    ("github", 174, "GitHub", "fishman7337", "https://cdn.simpleicons.org/github/FFFFFF"),
    ("linkedin", 204, "LinkedIn", "Goh Kun Ming", "https://api.iconify.design/simple-icons:linkedin.svg?color=%230A66C2"),
    ("email", 174, "Email", "say hello", "https://cdn.simpleicons.org/gmail/EA4335"),
    ("orcid", 184, "ORCID", "research id", "https://cdn.simpleicons.org/orcid/A6CE39"),
    ("arxiv", 174, "arXiv", "2508.09209", "https://cdn.simpleicons.org/arxiv/B31B1B"),
    ("read-preprint", 226, "Read preprint", "arXiv:2508.09209", "https://cdn.simpleicons.org/arxiv/B31B1B"),
    ("public-work", 184, "Public work", "portfolio ready", ""),
    ("research-grade", 206, "Research grade", "honest evaluation", ""),
    ("ai-systems", 174, "AI systems", "ML + MLOps", ""),
    ("singapore", 174, "Singapore", "SP DAAA", ""),
    ("quantum-ml", 190, "Quantum ML", "research domain", ""),
    ("gans", 142, "GANs", "model family", ""),
    ("qiskit", 154, "Qiskit", "tooling", "https://cdn.simpleicons.org/qiskit/6929C4"),
    ("fid-kid", 154, "FID / KID", "evaluation", ""),
]


def fetch_icon(url: str) -> tuple[str, str, str | None] | None:
    if not url:
        return None
    request = Request(url, headers={"User-Agent": "fishman7337-profile-readme"})
    with urlopen(request, timeout=20) as response:
        svg = response.read().decode("utf-8")
    match = re.search(r"<svg\b([^>]*)>(.*)</svg>", svg, flags=re.I | re.S)
    if not match:
        raise ValueError(f"Could not parse SVG from {url}")
    attrs, inner = match.group(1), match.group(2)
    viewbox = re.search(r'viewBox="([^"]+)"', attrs, flags=re.I)
    inner = re.sub(r"<(title|desc|metadata)\b[^>]*>.*?</\1>", "", inner, flags=re.I | re.S)
    simple_icon_color = re.search(r"cdn\.simpleicons\.org/[^/]+/([0-9A-Fa-f]{3,8})", url)
    fill = f"#{simple_icon_color.group(1)}" if simple_icon_color else None
    return viewbox.group(1) if viewbox else "0 0 24 24", inner.strip(), fill


def button(slug: str, width: int, title: str, subtitle: str, icon: tuple[str, str, str | None] | None) -> str:
    title_esc = html.escape(title)
    subtitle_esc = html.escape(subtitle)
    if icon:
        viewbox, inner, fill = icon
        fill_attr = f' fill="{html.escape(fill)}" color="{html.escape(fill)}"' if fill else ""
        mark = f'<svg x="17" y="15" width="24" height="24" viewBox="{html.escape(viewbox)}" preserveAspectRatio="xMidYMid meet"{fill_attr}>{inner}</svg>'
    else:
        mark = f'<text x="29" y="33" text-anchor="middle" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="14" font-weight="900" fill="#E0F2FE">{html.escape(title[:2].upper())}</text>'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="54" viewBox="0 0 {width} 54" role="img" aria-labelledby="title desc">
<title id="title">{title_esc}</title>
<desc id="desc">{title_esc} profile button</desc>
<defs>
  <linearGradient id="bg-{slug}" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#111827"/>
    <stop offset="52%" stop-color="#0B1F2A"/>
    <stop offset="100%" stop-color="#061F1B"/>
  </linearGradient>
  <linearGradient id="stroke-{slug}" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#22D3EE"/>
    <stop offset="46%" stop-color="#A78BFA"/>
    <stop offset="100%" stop-color="#FB7185"/>
  </linearGradient>
  <filter id="shadow-{slug}" x="-16%" y="-32%" width="132%" height="164%">
    <feDropShadow dx="0" dy="7" stdDeviation="7" flood-color="#020617" flood-opacity="0.45"/>
  </filter>
</defs>
<rect x="2" y="2" width="{width - 4}" height="50" rx="14" fill="url(#bg-{slug})" stroke="url(#stroke-{slug})" stroke-width="1.3" filter="url(#shadow-{slug})"/>
<rect x="10" y="9" width="38" height="36" rx="11" fill="#020617" opacity="0.72"/>
<rect x="11" y="10" width="36" height="34" rx="10" fill="#F8FAFC" opacity="0.08"/>
{mark}
<text x="60" y="24" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="13" font-weight="800" fill="#ECFEFF">{title_esc}</text>
<text x="60" y="39" font-family="JetBrains Mono, Consolas, monospace" font-size="9" font-weight="700" fill="#9EEBD9">{subtitle_esc}</text>
</svg>
'''


def main() -> None:
    seen = set()
    for slug, width, title, subtitle, source in BUTTONS:
        if slug in seen:
            raise SystemExit(f"Duplicate button slug: {slug}")
        seen.add(slug)
        (OUT / f"{slug}.svg").write_text(button(slug, width, title, subtitle, fetch_icon(source)), encoding="utf-8")
    print(f"Generated {len(BUTTONS)} profile buttons in {OUT}")


if __name__ == "__main__":
    main()
