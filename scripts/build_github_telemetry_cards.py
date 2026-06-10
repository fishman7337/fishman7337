#!/usr/bin/env python3
"""Generate local GitHub telemetry SVG cards for the profile README.

The README should not depend on third-party dynamic card services at render time.
This script creates checked-in SVG snapshots under assets/github-telemetry using
GitHub's public API, with a small offline fallback if the API is unavailable.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path
import html
import json
import os
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "github-telemetry"
USERNAME = "fishman7337"
SGT = timezone(timedelta(hours=8))

COLORS = {
    "bg": "#0D1117",
    "panel": "#161B22",
    "panel2": "#1B2030",
    "border": "#263244",
    "text": "#E5E7EB",
    "muted": "#94A3B8",
    "cyan": "#22D3EE",
    "blue": "#60A5FA",
    "purple": "#A78BFA",
    "pink": "#F472B6",
    "green": "#34D399",
    "amber": "#F59E0B",
    "orange": "#F97316",
    "red": "#FB7185",
}

PALETTE = [
    COLORS["orange"],
    COLORS["blue"],
    COLORS["green"],
    COLORS["purple"],
    COLORS["pink"],
    COLORS["amber"],
    COLORS["cyan"],
    COLORS["red"],
]

FALLBACK_REPOS = [
    {"name": "fishman7337", "language": "SVG", "stargazers_count": 0, "forks_count": 0, "pushed_at": "2026-06-10T00:00:00Z"},
    {"name": "hybrid-quantum-classical-gan-research", "language": "Python", "stargazers_count": 0, "forks_count": 0, "pushed_at": "2026-06-10T00:00:00Z"},
    {"name": "ISR", "language": "Python", "stargazers_count": 0, "forks_count": 0, "pushed_at": "2026-06-10T00:00:00Z"},
    {"name": "global-security-policy-intelligence", "language": "Python", "stargazers_count": 0, "forks_count": 0, "pushed_at": "2026-06-10T00:00:00Z"},
    {"name": "yubikey-secure-endpoint-system", "language": "Rust", "stargazers_count": 0, "forks_count": 0, "pushed_at": "2026-06-10T00:00:00Z"},
]

FALLBACK_LANG_BYTES = {
    "Jupyter Notebook": 72,
    "Python": 24,
    "Rust": 3,
    "HTML": 1,
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def ellipsize(value: str, limit: int) -> str:
    value = str(value)
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "..."


def github_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "fishman7337-profile-telemetry-generator",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch_json(url: str) -> object:
    request = urllib.request.Request(url, headers=github_headers())
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_repos() -> tuple[dict[str, object], list[dict[str, object]], dict[str, int], bool]:
    try:
        profile = fetch_json(f"https://api.github.com/users/{USERNAME}")
        repos: list[dict[str, object]] = []
        page = 1
        while True:
            chunk = fetch_json(
                f"https://api.github.com/users/{USERNAME}/repos"
                f"?type=owner&sort=updated&direction=desc&per_page=100&page={page}"
            )
            if not isinstance(chunk, list) or not chunk:
                break
            repos.extend(repo for repo in chunk if not repo.get("fork"))
            if len(chunk) < 100:
                break
            page += 1

        language_bytes: Counter[str] = Counter()
        for repo in repos:
            try:
                languages = fetch_json(f"https://api.github.com/repos/{USERNAME}/{repo['name']}/languages")
            except (urllib.error.URLError, TimeoutError, KeyError):
                languages = {}
            if isinstance(languages, dict):
                language_bytes.update({str(k): int(v) for k, v in languages.items()})

        if not repos:
            raise RuntimeError("No public repositories returned")
        return profile if isinstance(profile, dict) else {}, repos, dict(language_bytes), True
    except Exception:
        profile = {"public_repos": len(FALLBACK_REPOS), "followers": 0, "following": 0}
        return profile, FALLBACK_REPOS, FALLBACK_LANG_BYTES, False


def parse_time(value: object) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def svg_open(width: int, height: int, title: str, desc: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f"<title id=\"title\">{esc(title)}</title>",
        f"<desc id=\"desc\">{esc(desc)}</desc>",
        "<defs>",
        "<linearGradient id=\"bg\" x1=\"0\" y1=\"0\" x2=\"1\" y2=\"1\">",
        f"<stop offset=\"0%\" stop-color=\"{COLORS['bg']}\"/>",
        f"<stop offset=\"100%\" stop-color=\"{COLORS['panel2']}\"/>",
        "</linearGradient>",
        "<linearGradient id=\"neon\" x1=\"0\" y1=\"0\" x2=\"1\" y2=\"0\">",
        f"<stop offset=\"0%\" stop-color=\"{COLORS['cyan']}\"/>",
        f"<stop offset=\"50%\" stop-color=\"{COLORS['purple']}\"/>",
        f"<stop offset=\"100%\" stop-color=\"{COLORS['pink']}\"/>",
        "</linearGradient>",
        "<style><![CDATA[",
        ".title{font:800 25px Segoe UI,Inter,Arial,sans-serif;fill:#E5E7EB}",
        ".subtitle{font:700 14px Consolas,Menlo,monospace;fill:#22D3EE}",
        ".label{font:700 13px Consolas,Menlo,monospace;fill:#94A3B8}",
        ".value{font:800 24px Segoe UI,Inter,Arial,sans-serif;fill:#E5E7EB}",
        ".body{font:600 13px Segoe UI,Inter,Arial,sans-serif;fill:#CBD5E1}",
        ".mono{font:600 11px Consolas,Menlo,monospace;fill:#94A3B8}",
        ".axis{stroke:#334155;stroke-width:1}",
        "]]></style>",
        "</defs>",
        f"<rect width=\"{width}\" height=\"{height}\" rx=\"18\" fill=\"url(#bg)\"/>",
        f"<rect x=\"0.5\" y=\"0.5\" width=\"{width - 1}\" height=\"{height - 1}\" rx=\"17.5\" fill=\"none\" stroke=\"{COLORS['border']}\"/>",
        f"<path d=\"M28 56 H{width - 28}\" stroke=\"url(#neon)\" stroke-width=\"2\" opacity=\"0.7\"/>",
        f"<text x=\"28\" y=\"36\" class=\"title\">{esc(title)}</text>",
    ]


def svg_close(parts: list[str], path: Path) -> None:
    parts.append("</svg>\n")
    path.write_text("\n".join(parts), encoding="utf-8")


def metric_box(x: int, y: int, w: int, label: str, value: object, accent: str) -> str:
    return "\n".join(
        [
            f"<rect x=\"{x}\" y=\"{y}\" width=\"{w}\" height=\"72\" rx=\"14\" fill=\"{COLORS['panel']}\" stroke=\"{accent}\" stroke-opacity=\"0.42\"/>",
            f"<text x=\"{x + 16}\" y=\"{y + 28}\" class=\"label\">{esc(label)}</text>",
            f"<text x=\"{x + 16}\" y=\"{y + 58}\" class=\"value\">{esc(value)}</text>",
        ]
    )


def bar_rows(items: list[tuple[str, int]], x: int, y: int, w: int, row_h: int = 28) -> list[str]:
    parts: list[str] = []
    max_value = max((value for _, value in items), default=1)
    for idx, (label, value) in enumerate(items):
        yy = y + idx * row_h
        color = PALETTE[idx % len(PALETTE)]
        bar_w = max(6, int((value / max_value) * w))
        bar_x = x + 172
        parts.append(f"<text x=\"{x}\" y=\"{yy + 14}\" class=\"body\">{esc(ellipsize(label, 18))}</text>")
        parts.append(f"<rect x=\"{bar_x}\" y=\"{yy}\" width=\"{w}\" height=\"14\" rx=\"7\" fill=\"#0F172A\"/>")
        parts.append(f"<rect x=\"{bar_x}\" y=\"{yy}\" width=\"{bar_w}\" height=\"14\" rx=\"7\" fill=\"{color}\"/>")
        parts.append(f"<text x=\"{bar_x + w + 12}\" y=\"{yy + 12}\" class=\"mono\">{value}</text>")
    return parts


def percent_rows(items: list[tuple[str, int]], x: int, y: int, w: int, row_h: int = 30) -> list[str]:
    total = sum(value for _, value in items) or 1
    parts: list[str] = []
    for idx, (label, value) in enumerate(items):
        yy = y + idx * row_h
        pct = value / total
        color = PALETTE[idx % len(PALETTE)]
        bar_x = x + 172
        parts.append(f"<text x=\"{x}\" y=\"{yy + 15}\" class=\"body\">{esc(ellipsize(label, 18))}</text>")
        parts.append(f"<rect x=\"{bar_x}\" y=\"{yy}\" width=\"{w}\" height=\"16\" rx=\"8\" fill=\"#0F172A\"/>")
        parts.append(f"<rect x=\"{bar_x}\" y=\"{yy}\" width=\"{max(6, int(pct * w))}\" height=\"16\" rx=\"8\" fill=\"{color}\"/>")
        parts.append(f"<text x=\"{bar_x + w + 12}\" y=\"{yy + 13}\" class=\"mono\">{pct * 100:4.1f}%</text>")
    return parts


def build_intro() -> None:
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="150" viewBox="0 0 1200 150" role="img" aria-labelledby="title desc">',
        '<title id="title">Applied AI profile intro for Goh Kun Ming</title>',
        '<desc id="desc">Local intro banner for applied AI research, Singapore Polytechnic, quantum GANs, computer vision, sensor fusion, MLOps, and honest evaluation.</desc>',
        "<defs>",
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">',
        f'<stop offset="0%" stop-color="{COLORS["bg"]}"/>',
        '<stop offset="100%" stop-color="#111827"/>',
        "</linearGradient>",
        '<linearGradient id="neon" x1="0" y1="0" x2="1" y2="0">',
        f'<stop offset="0%" stop-color="{COLORS["cyan"]}"/>',
        f'<stop offset="48%" stop-color="{COLORS["purple"]}"/>',
        f'<stop offset="100%" stop-color="{COLORS["pink"]}"/>',
        "</linearGradient>",
        "<style><![CDATA[",
        ".headline{font:900 27px Segoe UI,Inter,Arial,sans-serif;fill:#E5E7EB}",
        ".subhead{font:800 20px Segoe UI,Inter,Arial,sans-serif;fill:#CBD5E1}",
        ".chipText{font:800 15px Consolas,JetBrains Mono,monospace;fill:#22D3EE}",
        ".note{font:700 13px Consolas,JetBrains Mono,monospace;fill:#94A3B8}",
        ".chip{fill:#111827;stroke:#22D3EE;stroke-opacity:.34}",
        "]]></style>",
        "</defs>",
        '<rect width="1200" height="150" rx="22" fill="url(#bg)"/>',
        '<rect x="1" y="1" width="1198" height="148" rx="21" fill="none" stroke="#263244"/>',
        '<path d="M34 32 H1166" stroke="url(#neon)" stroke-width="2" opacity=".78"/>',
        '<text x="600" y="56" text-anchor="middle" class="headline">Goh Kun Ming | Applied AI Research Intern</text>',
        '<text x="600" y="84" text-anchor="middle" class="subhead">Applied AI and Analytics @ Singapore Polytechnic</text>',
        '<g transform="translate(82 106)">',
        '<rect class="chip" x="0" y="-18" width="164" height="32" rx="16"/>',
        '<text x="82" y="3" text-anchor="middle" class="chipText">Quantum GANs</text>',
        '<rect class="chip" x="184" y="-18" width="180" height="32" rx="16"/>',
        '<text x="274" y="3" text-anchor="middle" class="chipText">Computer Vision</text>',
        '<rect class="chip" x="384" y="-18" width="164" height="32" rx="16"/>',
        '<text x="466" y="3" text-anchor="middle" class="chipText">Sensor Fusion</text>',
        '<rect class="chip" x="568" y="-18" width="96" height="32" rx="16"/>',
        '<text x="616" y="3" text-anchor="middle" class="chipText">MLOps</text>',
        '<rect class="chip" x="684" y="-18" width="350" height="32" rx="16"/>',
        '<text x="859" y="3" text-anchor="middle" class="note">Research-grade systems with honest evaluation</text>',
        "</g>",
    ]
    svg_close(parts, ROOT / "assets" / "typing-intro.svg")


def build_profile_details(profile: dict[str, object], repos: list[dict[str, object]], language_bytes: dict[str, int], generated: str, live: bool) -> None:
    top_languages = sorted(language_bytes.items(), key=lambda item: item[1], reverse=True)[:5]
    recent = sorted(repos, key=lambda repo: str(repo.get("pushed_at") or ""), reverse=True)[:4]
    parts = svg_open(960, 440, "GitHub Telemetry Snapshot", "Local checked-in telemetry snapshot for fishman7337.")
    parts.append(f"<text x=\"28\" y=\"78\" class=\"subtitle\">Local SVG snapshot - no third-party card service at README render time</text>")
    metric_y = 102
    for idx, (label, value, color) in enumerate(
        [
            ("Repos", profile.get("public_repos", len(repos)), COLORS["cyan"]),
            ("Stars", sum(int(r.get("stargazers_count") or 0) for r in repos), COLORS["purple"]),
            ("Forks", sum(int(r.get("forks_count") or 0) for r in repos), COLORS["green"]),
            ("Followers", profile.get("followers", 0), COLORS["pink"]),
            ("Timezone", "SGT", COLORS["amber"]),
        ]
    ):
        parts.append(metric_box(28 + idx * 180, metric_y, 150, label, value, color))
    parts.append("<text x=\"28\" y=\"220\" class=\"subtitle\">Top language footprint</text>")
    parts.extend(percent_rows([(k, int(v)) for k, v in top_languages], 28, 244, 270, row_h=26))
    parts.append("<text x=\"520\" y=\"220\" class=\"subtitle\">Recently updated repos</text>")
    for idx, repo in enumerate(recent):
        dt = parse_time(repo.get("pushed_at"))
        when = dt.astimezone(SGT).strftime("%Y-%m-%d %H:%M") if dt else "unknown"
        y = 244 + idx * 42
        color = PALETTE[idx % len(PALETTE)]
        parts.append(f"<rect x=\"520\" y=\"{y - 18}\" width=\"392\" height=\"34\" rx=\"14\" fill=\"{COLORS['panel']}\" stroke=\"{color}\" stroke-opacity=\"0.30\"/>")
        parts.append(f"<circle cx=\"534\" cy=\"{y - 5}\" r=\"5\" fill=\"{color}\"/>")
        parts.append(f"<text x=\"548\" y=\"{y}\" class=\"body\">{esc(ellipsize(str(repo.get('name')), 40))}</text>")
        parts.append(f"<text x=\"548\" y=\"{y + 14}\" class=\"mono\">{esc(when)} SGT</text>")
    source = "live GitHub API" if live else "offline fallback"
    parts.append(f"<text x=\"28\" y=\"418\" class=\"mono\">Generated {esc(generated)} from {esc(source)}. Checked into this repository for reliable README rendering.</text>")
    svg_close(parts, OUT / "profile-details.svg")


def build_stats(profile: dict[str, object], repos: list[dict[str, object]], generated: str) -> None:
    parts = svg_open(470, 280, "Repository Stats", "Repository count, stars, forks, and recency.")
    active_90 = 0
    now = datetime.now(timezone.utc)
    for repo in repos:
        dt = parse_time(repo.get("pushed_at"))
        if dt and (now - dt).days <= 90:
            active_90 += 1
    parts.append(metric_box(28, 84, 190, "Public repos", profile.get("public_repos", len(repos)), COLORS["cyan"]))
    parts.append(metric_box(252, 84, 190, "Updated in 90d", active_90, COLORS["green"]))
    parts.append(metric_box(28, 178, 190, "Stars", sum(int(r.get("stargazers_count") or 0) for r in repos), COLORS["purple"]))
    parts.append(metric_box(252, 178, 190, "Forks", sum(int(r.get("forks_count") or 0) for r in repos), COLORS["pink"]))
    parts.append(f"<text x=\"28\" y=\"262\" class=\"mono\">Snapshot {esc(generated)} UTC+08</text>")
    svg_close(parts, OUT / "stats.svg")


def build_productive_time(repos: list[dict[str, object]], generated: str) -> None:
    counts = [0 for _ in range(24)]
    for repo in repos:
        dt = parse_time(repo.get("pushed_at"))
        if dt:
            counts[dt.astimezone(SGT).hour] += 1
    max_count = max(counts) or 1
    parts = svg_open(470, 280, "Update Time by Repo", "Repository pushed_at timestamps grouped by Singapore time.")
    parts.append("<text x=\"28\" y=\"78\" class=\"subtitle\">Default-branch update hour, Singapore time</text>")
    chart_x, chart_y, chart_w, chart_h = 42, 104, 392, 112
    parts.append(f"<line x1=\"{chart_x}\" y1=\"{chart_y + chart_h}\" x2=\"{chart_x + chart_w}\" y2=\"{chart_y + chart_h}\" class=\"axis\"/>")
    parts.append(f"<line x1=\"{chart_x}\" y1=\"{chart_y}\" x2=\"{chart_x}\" y2=\"{chart_y + chart_h}\" class=\"axis\"/>")
    gap = 3
    bar_w = int((chart_w - gap * 23) / 24)
    for hour, count in enumerate(counts):
        h = int((count / max_count) * (chart_h - 8))
        x = chart_x + hour * (bar_w + gap)
        y = chart_y + chart_h - h
        color = COLORS["cyan"] if count else "#1E293B"
        parts.append(f"<rect x=\"{x}\" y=\"{y}\" width=\"{bar_w}\" height=\"{h}\" rx=\"3\" fill=\"{color}\"/>")
    for hour in [0, 6, 12, 18, 23]:
        x = chart_x + hour * (bar_w + gap)
        parts.append(f"<text x=\"{x}\" y=\"242\" class=\"mono\">{hour}</text>")
    parts.append(f"<text x=\"286\" y=\"262\" class=\"mono\">Snapshot {esc(generated)}</text>")
    svg_close(parts, OUT / "productive-time.svg")


def build_repos_per_language(repos: list[dict[str, object]], generated: str) -> None:
    languages: Counter[str] = Counter()
    for repo in repos:
        language = str(repo.get("language") or "Other")
        languages[language] += 1
    items = languages.most_common(5)
    parts = svg_open(470, 280, "Top Languages by Repo", "Repository primary languages.")
    parts.extend(bar_rows([(k, int(v)) for k, v in items], 28, 88, 186, row_h=30))
    parts.append(f"<text x=\"286\" y=\"262\" class=\"mono\">Snapshot {esc(generated)}</text>")
    svg_close(parts, OUT / "repos-per-language.svg")


def build_language_volume(language_bytes: dict[str, int], generated: str) -> None:
    items = sorted(language_bytes.items(), key=lambda item: item[1], reverse=True)[:5]
    parts = svg_open(470, 280, "Top Languages by Code", "Language bytes across public repositories.")
    parts.extend(percent_rows([(k, int(v)) for k, v in items], 28, 88, 186, row_h=30))
    parts.append(f"<text x=\"286\" y=\"262\" class=\"mono\">Snapshot {esc(generated)}</text>")
    svg_close(parts, OUT / "language-volume.svg")


def build_activity_snapshot(repos: list[dict[str, object]], generated: str) -> None:
    recent = sorted(repos, key=lambda repo: str(repo.get("pushed_at") or ""), reverse=True)[:7]
    parts = svg_open(960, 330, "Recent Repository Activity", "Recent public repository updates served as a local SVG.")
    parts.append("<text x=\"28\" y=\"78\" class=\"subtitle\">Recent default-branch updates from public owner repositories</text>")
    for idx, repo in enumerate(recent):
        x = 34
        y = 108 + idx * 29
        dt = parse_time(repo.get("pushed_at"))
        when = dt.astimezone(SGT).strftime("%Y-%m-%d %H:%M") if dt else "unknown"
        color = PALETTE[idx % len(PALETTE)]
        parts.append(f"<rect x=\"{x}\" y=\"{y - 18}\" width=\"892\" height=\"25\" rx=\"12\" fill=\"{COLORS['panel']}\" stroke=\"{color}\" stroke-opacity=\"0.35\"/>")
        parts.append(f"<circle cx=\"{x + 16}\" cy=\"{y - 5}\" r=\"5\" fill=\"{color}\"/>")
        parts.append(f"<text x=\"{x + 32}\" y=\"{y}\" class=\"body\">{esc(ellipsize(str(repo.get('name')), 64))}</text>")
        parts.append(f"<text x=\"760\" y=\"{y}\" class=\"mono\">{esc(when)} SGT</text>")
    parts.append(f"<text x=\"28\" y=\"308\" class=\"mono\">Snapshot {esc(generated)} - checked into this repository for reliable README rendering</text>")
    svg_close(parts, OUT / "activity-snapshot.svg")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    profile, repos, language_bytes, live = fetch_repos()
    generated = datetime.now(SGT).strftime("%Y-%m-%d %H:%M")
    build_intro()
    build_profile_details(profile, repos, language_bytes, generated, live)
    build_stats(profile, repos, generated)
    build_productive_time(repos, generated)
    build_repos_per_language(repos, generated)
    build_language_volume(language_bytes, generated)
    build_activity_snapshot(repos, generated)
    print(f"Generated {len(list(OUT.glob('*.svg')))} telemetry SVG cards in {OUT}")


if __name__ == "__main__":
    main()
