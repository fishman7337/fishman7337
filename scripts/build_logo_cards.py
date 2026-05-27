#!/usr/bin/env python3
"""Generate rounded square logo cards used by the profile README."""
from __future__ import annotations

from pathlib import Path
import html
import re
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "tech-logos"
OUT.mkdir(parents=True, exist_ok=True)


LOGOS = [
    ("python", "Python", "Python", "https://cdn.simpleicons.org/python/3776AB", "https://www.python.org/"),
    ("pytorch", "PyTorch", "PyTorch", "https://cdn.simpleicons.org/pytorch/EE4C2C", "https://pytorch.org/"),
    ("tensorflow", "TensorFlow", "TensorFlow", "https://cdn.simpleicons.org/tensorflow/FF6F00", "https://www.tensorflow.org/"),
    ("keras", "Keras", "Keras", "https://cdn.simpleicons.org/keras/D00000", "https://keras.io/"),
    ("scikit-learn", "scikit-learn", "scikit", "https://cdn.simpleicons.org/scikitlearn/F7931E", "https://scikit-learn.org/"),
    ("qiskit", "Qiskit", "Qiskit", "https://cdn.simpleicons.org/qiskit/6929C4", "https://www.qiskit.org/"),
    ("opencv", "OpenCV", "OpenCV", "https://cdn.simpleicons.org/opencv/5C3EE8", "https://opencv.org/"),
    ("ros", "ROS", "ROS", "https://cdn.simpleicons.org/ros/22314E", "https://www.ros.org/"),
    ("pandas", "Pandas", "Pandas", "https://cdn.simpleicons.org/pandas/150458", "https://pandas.pydata.org/"),
    ("numpy", "NumPy", "NumPy", "https://cdn.simpleicons.org/numpy/013243", "https://numpy.org/"),
    ("matplotlib", "Matplotlib", "MPL", "https://api.iconify.design/logos:matplotlib-icon.svg", "https://matplotlib.org/"),
    ("seaborn", "Seaborn", "Seaborn", "https://api.iconify.design/logos:seaborn-icon.svg", "https://seaborn.pydata.org/"),
    ("statsmodels", "statsmodels", "stats", "", "https://www.statsmodels.org/"),
    ("plotly", "Plotly", "Plotly", "https://cdn.simpleicons.org/plotly/3F4F75", "https://plotly.com/python/"),
    ("dash", "Dash", "Dash", "", "https://dash.plotly.com/"),
    ("tableau", "Tableau", "Tableau", "https://api.iconify.design/logos:tableau-icon.svg", "https://www.tableau.com/"),
    ("power-bi", "Power BI", "Power BI", "https://api.iconify.design/logos:microsoft-power-bi.svg", "https://powerbi.microsoft.com/"),
    ("postgresql", "PostgreSQL", "Postgres", "https://cdn.simpleicons.org/postgresql/4169E1", "https://www.postgresql.org/"),
    ("sqlite", "SQLite", "SQLite", "https://cdn.simpleicons.org/sqlite/003B57", "https://www.sqlite.org/"),
    ("neo4j", "Neo4j", "Neo4j", "https://cdn.simpleicons.org/neo4j/4581C3", "https://neo4j.com/"),
    ("aws", "AWS", "AWS", "https://api.iconify.design/logos:aws.svg", "https://aws.amazon.com/"),
    ("gcp", "Google Cloud", "GCP", "https://cdn.simpleicons.org/googlecloud/4285F4", "https://cloud.google.com/"),
    ("kubernetes", "Kubernetes", "K8s", "https://cdn.simpleicons.org/kubernetes/326CE5", "https://kubernetes.io/"),
    ("docker", "Docker", "Docker", "https://cdn.simpleicons.org/docker/2496ED", "https://www.docker.com/"),
    ("fastapi", "FastAPI", "FastAPI", "https://cdn.simpleicons.org/fastapi/009688", "https://fastapi.tiangolo.com/"),
    ("flask", "Flask", "Flask", "https://cdn.simpleicons.org/flask/111827", "https://flask.palletsprojects.com/"),
    ("github-actions", "GitHub Actions", "Actions", "https://cdn.simpleicons.org/githubactions/2088FF", "https://github.com/features/actions"),
    ("pytest", "pytest", "pytest", "https://cdn.simpleicons.org/pytest/0A9EDC", "https://docs.pytest.org/"),
    ("wandb", "Weights and Biases", "W&B", "https://cdn.simpleicons.org/weightsandbiases/FFBE00", "https://wandb.ai/"),
    ("rust", "Rust", "Rust", "https://cdn.simpleicons.org/rust/111827", "https://www.rust-lang.org/"),
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
    inner = re.sub(r"<(title|desc)\b[^>]*>.*?</\1>", "", inner, flags=re.I | re.S)
    simple_icon_color = re.search(r"cdn\.simpleicons\.org/[^/]+/([0-9A-Fa-f]{3,8})", url)
    fill = f"#{simple_icon_color.group(1)}" if simple_icon_color else None
    return viewbox.group(1) if viewbox else "0 0 24 24", inner.strip(), fill


def text_mark(label: str, color: str = "#22D3EE") -> str:
    fs = 24 if len(label) <= 4 else 18
    return f'<text x="44" y="45" text-anchor="middle" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="{fs}" font-weight="900" fill="{color}">{html.escape(label)}</text>'


def card(slug: str, name: str, label: str, icon: tuple[str, str, str | None] | None) -> str:
    title = html.escape(name)
    label = html.escape(label)
    if icon:
        viewbox, inner, fill = icon
        fill_attr = f' fill="{html.escape(fill)}" color="{html.escape(fill)}"' if fill else ""
        mark = f'<svg x="24" y="13" width="40" height="40" viewBox="{html.escape(viewbox)}" preserveAspectRatio="xMidYMid meet"{fill_attr}>{inner}</svg>'
    elif slug == "dash":
        mark = text_mark("Dash", "#38BDF8")
    else:
        mark = text_mark("SM", "#A78BFA")

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="88" height="88" viewBox="0 0 88 88" role="img" aria-labelledby="title desc">
<title id="title">{title}</title>
<desc id="desc">Rounded square logo card for {title}</desc>
<defs>
  <linearGradient id="card-bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#172033"/>
    <stop offset="54%" stop-color="#0B1F2A"/>
    <stop offset="100%" stop-color="#061F1B"/>
  </linearGradient>
  <linearGradient id="card-stroke" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#22D3EE"/>
    <stop offset="52%" stop-color="#A78BFA"/>
    <stop offset="100%" stop-color="#FB7185"/>
  </linearGradient>
  <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
    <feDropShadow dx="0" dy="7" stdDeviation="8" flood-color="#020617" flood-opacity="0.55"/>
  </filter>
</defs>
<rect x="3" y="3" width="82" height="82" rx="18" fill="url(#card-bg)" stroke="url(#card-stroke)" stroke-width="1.8" opacity="1" filter="url(#shadow)"/>
<rect x="8" y="8" width="72" height="72" rx="15" fill="#020617" opacity="0.38"/>
<rect x="16" y="10" width="56" height="48" rx="14" fill="#F8FAFC" opacity="0.98"/>
<rect x="16" y="10" width="56" height="48" rx="14" fill="none" stroke="#FFFFFF" stroke-opacity="0.72"/>
{mark}
<text x="44" y="73" text-anchor="middle" font-family="JetBrains Mono, Consolas, monospace" font-size="8.7" font-weight="800" fill="#CFFAFE">{label}</text>
</svg>
'''


def main() -> None:
    seen = set()
    for slug, name, label, source, _href in LOGOS:
        if slug in seen:
            raise SystemExit(f"Duplicate logo slug: {slug}")
        seen.add(slug)
        icon = fetch_icon(source)
        (OUT / f"{slug}.svg").write_text(card(slug, name, label, icon), encoding="utf-8")
    print(f"Generated {len(LOGOS)} logo cards in {OUT}")


if __name__ == "__main__":
    main()
