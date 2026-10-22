"""Tests for profile content and deterministic SVG generation."""

from __future__ import annotations

import importlib.util
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]


def load_build_assets():
    """Load the asset builder from its script path for isolated tests."""

    path = REPO_ROOT / "scripts" / "build_assets.py"
    spec = importlib.util.spec_from_file_location("build_assets", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_telemetry_assets():
    """Load the telemetry builder from its script path for isolated tests."""

    path = REPO_ROOT / "scripts" / "build_github_telemetry_cards.py"
    spec = importlib.util.spec_from_file_location("build_github_telemetry_cards", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_script(filename: str):
    """Load another profile-generation script for focused validation."""

    path = REPO_ROOT / "scripts" / filename
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_profile_content_has_required_identity_and_project_evidence() -> None:
    content = yaml.safe_load((REPO_ROOT / "content" / "profile.yml").read_text(encoding="utf-8"))

    assert content["identity"]["name"] == "Goh Kun Ming"
    assert content["identity"]["username"] == "fishman7337"
    assert content["theme"]["cyan"].startswith("#")
    assert len(content["projects"]) >= 6
    assert all(project.get("name") and project.get("desc") for project in content["projects"])
    assert len(content["capabilities"]) == 4
    assert len(content["experience"]) == 5
    assert any(item["organisation"] == "RSAF RAiD · AETHER" for item in content["experience"])
    assert content["experience"][0]["type"] == "Internship"
    assert content["identity"]["website"] == "https://gohkunming.dev/"
    assert len(content["credentials"]) >= 5
    assert len(content["approach"]) == 6
    assert len(content["collaboration"]["strengths"]) >= 5
    assert "AI academia" in content["about"]["long_term_direction"]


def test_text_helpers_escape_and_bound_content() -> None:
    assets = load_build_assets()

    assert assets.esc('<leaf title="AI">') == "&lt;leaf title=&quot;AI&quot;&gt;"
    assert assets.wrap("alpha beta gamma", width=10) == ["alpha beta", "gamma"]
    assert assets.ellipsize("abcdefgh", 5) == "abcd…"


def test_main_generates_well_formed_svg_assets(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    assets = load_build_assets()
    monkeypatch.setattr(assets, "ASSETS", tmp_path)

    assets.main()

    generated = sorted(tmp_path.glob("*.svg"))
    assert len(generated) == 10
    for path in generated:
        root = ET.parse(path).getroot()
        assert root.tag.endswith("svg")
        assert root.attrib["viewBox"]


def test_recruiter_assets_reproduce_committed_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Catch missing or stale published artwork after editing its generator."""
    assets = load_script("build_recruiter_assets.py")
    monkeypatch.setattr(assets, "ASSETS", tmp_path)
    assets.main()
    generated = sorted(tmp_path.glob("*.svg"))
    assert len(generated) == 8
    assert sum(path.stat().st_size for path in generated) < 250_000
    for path in generated:
        assert path.read_bytes() == (REPO_ROOT / "assets" / path.name).read_bytes()


def test_readme_has_substantive_public_biography() -> None:
    """Keep current work and internship status visible without image rendering."""
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    visible_intro = readme.split("## Selected work")[0]
    for fact in [
        "Goh Kun Ming",
        "Research Engineer intern",
        "Pragnition Labs",
        "Singapore Polytechnic",
    ]:
        assert fact in visible_intro
    assert "research and academia" in readme
    assert "teaching and mentoring" in readme.lower()
    assert "Oct 2026–present" in readme
    assert "AI Research Intern · RSAF RAiD · AETHER" in readme
    assert "Apr–Aug 2026" in readme


def test_readme_local_references_and_navigation_resolve() -> None:
    """Prevent broken relative links and fragment navigation after redesigns."""
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    local_links = re.findall(r'(?:href|src|srcset)="(\./[^"]+)"|\]\((\./[^)]+)\)', readme)
    assert local_links
    for html_link, md_link in local_links:
        target = html_link or md_link
        assert (REPO_ROOT / target.split("#")[0]).is_file(), target
    headings = re.findall(r"^#{1,6} (.+)$", readme, flags=re.MULTILINE)
    anchors = {re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-") for heading in headings}
    for fragment in re.findall(r'href="#([^"]+)"', readme):
        assert fragment in anchors, fragment


def test_readme_images_have_intentional_alt_text() -> None:
    """Keep image alternatives and separate narrow-screen hero/workflow views."""
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    image_tags = re.findall(r"<img\b[^>]*>", readme)
    assert image_tags
    for tag in image_tags:
        assert re.search(r'\balt="[^"]+"', tag), tag
    assert 'media="(max-width: 600px)"' in readme
    assert "profile-hero-mobile.gif" in readme
    assert "process-applied-mobile.gif" in readme
    assert "process-research-mobile.gif" in readme


def test_vector_source_assets_have_accessible_metadata_and_reduced_motion() -> None:
    """Protect SVG semantics, static fallback, motion preferences and self-containment."""
    asset_names = {path.name for path in (REPO_ROOT / "assets").glob("recruiter-*.svg")}
    assert asset_names
    for asset_name in asset_names:
        svg = (REPO_ROOT / "assets" / asset_name).read_text(encoding="utf-8")
        root = ET.fromstring(svg)
        assert root.attrib.get("role") == "img"
        assert root.attrib["viewBox"]
        assert root.find("{http://www.w3.org/2000/svg}title") is not None
        assert root.find("{http://www.w3.org/2000/svg}desc") is not None
        assert "prefers-reduced-motion:reduce" in svg
        assert "animation:none" in svg
        for element in root.iter():
            assert element.tag.split("}")[-1] not in {"script", "foreignObject", "animate", "image"}
            for attr, value in element.attrib.items():
                assert not attr.lower().startswith("on")
                if attr.split("}")[-1] == "href":
                    assert value.startswith("#")


def test_core_visual_palette_has_enhanced_text_contrast() -> None:
    """Keep the primary SVG text pairings above a 7:1 contrast ratio."""

    def luminance(hex_color: str) -> float:
        channels = [int(hex_color[index : index + 2], 16) / 255 for index in (1, 3, 5)]
        linear = [
            channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4
            for channel in channels
        ]
        return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

    def contrast(foreground: str, background: str) -> float:
        lighter, darker = sorted((luminance(foreground), luminance(background)), reverse=True)
        return (lighter + 0.05) / (darker + 0.05)

    for foreground, background in [
        ("#FFF9EF", "#050814"),
        ("#C9C6D4", "#050814"),
        ("#63D9D1", "#111725"),
        ("#FFF9EF", "#111725"),
        ("#F4F0E8", "#08111C"),
        ("#64E2CB", "#08111C"),
        ("#FFA58A", "#08111C"),
        ("#B8ADFF", "#08111C"),
        ("#A5B4BF", "#08111C"),
    ]:
        assert contrast(foreground, background) >= 7


def test_employer_facing_claims_have_public_evidence_links() -> None:
    """Keep experience and project claims connected to public records."""
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    assert "https://www.linkedin.com/in/gohkunming/details/experience/" in readme
    assert "https://www.linkedin.com/in/gohkunming/details/certifications/" in readme
    assert readme.count("https://github.com/fishman7337/") >= 12
    assert "https://gohkunming.dev/#experience" in readme


def test_3d_mesh_generation_is_well_formed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    mesh = load_script("build_3d_mesh.py")
    models = tmp_path / "models"
    monkeypatch.setattr(mesh, "ASSETS", tmp_path)
    monkeypatch.setattr(mesh, "MODELS", models)

    mesh.main()

    stl = (models / "curiosity-knot.stl").read_text(encoding="ascii")
    obj = (models / "curiosity-knot.obj").read_text(encoding="ascii")
    preview = tmp_path / "curiosity-knot-wireframe.svg"

    assert stl.startswith("solid curiosity_knot")
    assert stl.count("facet normal") == 3456
    assert sum(line.startswith("v ") for line in obj.splitlines()) == 1728
    assert sum(line.startswith("f ") for line in obj.splitlines()) == 3456
    assert ET.parse(preview).getroot().tag.endswith("svg")


def test_readme_keeps_calls_to_action_public_facing() -> None:
    """Keep project evidence and contact links free of artwork production controls."""
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "./scripts/" not in readme
    assert "./assets/models/" not in readme
    assert "Explore the experiments" in readme
    assert "Email Kun Ming" in readme


def test_profile_does_not_use_unrequested_publication_branding() -> None:
    """Keep publication-index framing outside the requested professional profile."""
    paths = [
        REPO_ROOT / "README.md",
        REPO_ROOT / "content" / "profile.yml",
        REPO_ROOT / "scripts" / "build_assets.py",
        REPO_ROOT / "manifest.json",
        *sorted((REPO_ROOT / "docs").glob("*.md")),
    ]
    retired = ("ar" + "xiv", "or" + "cid")

    for path in paths:
        text = path.read_text(encoding="utf-8").lower()
        assert all(term not in text for term in retired)


def test_telemetry_fetch_uses_offline_fallback_for_network_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    telemetry = load_telemetry_assets()

    def fail_fetch(_url: str) -> object:
        raise telemetry.urllib.error.URLError("offline")

    monkeypatch.setattr(telemetry, "fetch_json", fail_fetch)

    profile, repos, languages, is_live = telemetry.fetch_repos()

    assert not is_live
    assert profile["public_repos"] == len(telemetry.FALLBACK_REPOS)
    assert repos == telemetry.FALLBACK_REPOS
    assert languages == telemetry.FALLBACK_LANG_BYTES


def test_telemetry_fetch_does_not_hide_programming_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    telemetry = load_telemetry_assets()

    def fail_fetch(_url: str) -> object:
        raise AssertionError("unexpected implementation defect")

    monkeypatch.setattr(telemetry, "fetch_json", fail_fetch)

    with pytest.raises(AssertionError, match="implementation defect"):
        telemetry.fetch_repos()


def test_telemetry_fetch_does_not_hide_url_validation_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Keep URL-integrity failures visible instead of using stale data."""
    telemetry = load_telemetry_assets()

    def fail_validation(_url: str) -> object:
        raise ValueError("GitHub telemetry URLs must use https://api.github.com")

    monkeypatch.setattr(telemetry, "fetch_json", fail_validation)

    with pytest.raises(ValueError, match="https://api.github.com"):
        telemetry.fetch_repos()


@pytest.mark.parametrize(
    ("filename", "arguments"),
    [
        ("build_logo_cards.py", ("unsafe", "file:///tmp/icon.svg")),
        ("build_profile_buttons.py", ("file:///tmp/icon.svg",)),
    ],
)
def test_remote_asset_fetchers_reject_non_https_urls(
    filename: str,
    arguments: tuple[str, ...],
) -> None:
    assets = load_script(filename)

    with pytest.raises(ValueError, match="HTTPS"):
        assets.fetch_icon(*arguments)


def test_telemetry_fetch_rejects_non_github_hosts() -> None:
    telemetry = load_telemetry_assets()

    with pytest.raises(ValueError, match="api.github.com"):
        telemetry.fetch_json("https://example.com/repos")
