"""Regression tests for the map tile provider and its attribution."""

from pathlib import Path

import pytest


TEMPLATES_DIR = Path(__file__).parents[2] / "src" / "malla" / "templates"
MAP_TEMPLATES = ("map.html", "node_detail.html", "packet_detail.html")
OSM_TILE_URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
OSM_ATTRIBUTION = (
    '&copy; <a href="https://www.openstreetmap.org/copyright">'
    "OpenStreetMap</a> contributors"
)


@pytest.mark.parametrize("template_name", MAP_TEMPLATES)
def test_maps_use_standard_openstreetmap_tiles_with_attribution(template_name):
    template = (TEMPLATES_DIR / template_name).read_text(encoding="utf-8")

    assert OSM_TILE_URL in template
    assert OSM_ATTRIBUTION in template
    assert "basemaps.cartocdn.com" not in template
    assert "carto.com/attributions" not in template


def test_all_openstreetmap_layers_have_attribution():
    for template_name in MAP_TEMPLATES:
        template = (TEMPLATES_DIR / template_name).read_text(encoding="utf-8")

        assert template.count(OSM_TILE_URL) == template.count(OSM_ATTRIBUTION)
