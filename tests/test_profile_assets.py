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
