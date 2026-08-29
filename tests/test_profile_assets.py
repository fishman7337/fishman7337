"""Tests for profile content and deterministic SVG generation."""

from __future__ import annotations

import importlib.util
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
    assert len(content["experience"]) == 3
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


def test_readme_uses_the_spatial_portfolio_visual_system() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    for asset in [
        "spatial-hero.svg",
        "spatial-hero-mobile.svg",
        "capability-map.svg",
        "capability-map-mobile.svg",
        "world-generative-vision.svg",
        "world-data-intelligence.svg",
        "world-ai-product-system.svg",
        "curiosity-knot-wireframe.svg",
        "tool-constellation.svg",
        "spatial-footer.svg",
        "spatial-footer-mobile.svg",
    ]:
        assert f"./assets/{asset}" in readme

    assert "Applied AI & Analytics Student" in (REPO_ROOT / "content" / "profile.yml").read_text(
        encoding="utf-8"
    )
    assert readme.count("<details") >= 14
    assert "What I bring to a team" in readme
    assert "Experience in practice" in readme
    assert "public LinkedIn experience" in readme


def test_readme_has_substantive_public_biography() -> None:
    """Keep the profile person-led instead of relying on artwork alone."""
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    for section in [
        "## About me",
        "### A quick read",
        "## How I approach a problem",
        "## What teammates can expect from me",
        "## Learning and research direction",
        "### Problems I want to keep exploring",
        "### The environments where I contribute best",
    ]:
        assert section in readme

    assert "AI academia" in readme
    assert "teaching and mentoring" in readme.lower()
    assert "<details open>" in readme


def test_employer_facing_claims_have_public_evidence_links() -> None:
    """Keep experience and project claims connected to public records."""
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    assert "https://www.linkedin.com/in/gohkunming/details/experience/" in readme
    assert "https://www.linkedin.com/in/gohkunming/details/certifications/" in readme
    assert readme.count("https://github.com/fishman7337/") >= 12
    assert "business-impact claims" in readme


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


def test_readme_mesh_claims_match_the_generator() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    assert "1,728 vertices" in readme
    assert "3,456 triangular faces" in readme
    assert "./assets/models/curiosity-knot.stl" in readme
    assert "./assets/models/curiosity-knot.obj" in readme


def test_profile_does_not_use_retired_identity_framing() -> None:
    """Keep earlier affiliations and paper-index branding out of the profile."""
    paths = [
        REPO_ROOT / "README.md",
        REPO_ROOT / "content" / "profile.yml",
        REPO_ROOT / "scripts" / "build_assets.py",
        REPO_ROOT / "manifest.json",
        *sorted((REPO_ROOT / "docs").glob("*.md")),
    ]
    retired = ("ra" + "id", "rs" + "af", "ae" + "ther", "ar" + "xiv", "or" + "cid")

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
