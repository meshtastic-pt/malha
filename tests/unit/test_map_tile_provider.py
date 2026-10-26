"""Regression tests for the map tile provider and its attribution."""

from pathlib import Path

import pytest

TEMPLATES_DIR = Path(__file__).parents[2] / "src" / "malla" / "templates"
STATIC_DIR = Path(__file__).parents[2] / "src" / "malla" / "static"
MAP_TEMPLATES = (
    "map.html",
    "node_detail.html",
    "packet_detail.html",
    "line_of_sight.html",
)


@pytest.mark.parametrize("template_name", MAP_TEMPLATES)
def test_maps_use_shared_openfreemap_assets(template_name):
    template = (TEMPLATES_DIR / template_name).read_text(encoding="utf-8")

    assert "components/openfreemap_css.html" in template
    assert "components/openfreemap_js.html" in template
    assert "js/openfreemap.js" in template
    assert "basemaps.cartocdn.com" not in template
    assert "carto.com/attributions" not in template


def test_openfreemap_supports_both_themes_and_required_attribution():
    script = (STATIC_DIR / "js" / "openfreemap.js").read_text(encoding="utf-8")

    assert "https://tiles.openfreemap.org/styles/liberty" in script
    assert "https://tiles.openfreemap.org/styles/dark" in script
    assert "https://www.openstreetmap.org/copyright" in script
    assert ">OpenStreetMap</a> contributors" in script
    assert ">OpenFreeMap</a>" in script
