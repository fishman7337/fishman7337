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
    assert len(content["projects"]) >= 3
    assert all(project.get("name") and project.get("desc") for project in content["projects"])


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
