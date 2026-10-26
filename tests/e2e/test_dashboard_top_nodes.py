"""End-to-end coverage for the active-node ranking."""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_top_nodes_are_presented_as_a_responsive_ranking(
    page: Page, test_server_url: str
):
    """Render active nodes as ranking cards instead of a nested table."""
    page.goto(test_server_url)
    page.wait_for_selector("#topNodesLoading", state="hidden", timeout=20000)

    ranking = page.locator("#topNodesRanking")
    items = ranking.locator(".top-node-item")

    expect(ranking).to_be_visible()
    expect(items.first).to_be_visible()
    expect(ranking.locator("table")).to_have_count(0)
    expect(items.first.locator(".top-node-rank .bi-trophy-fill")).to_be_visible()
    expect(items.first.locator(".top-node-activity-bar")).to_be_visible()

    page.set_viewport_size({"width": 390, "height": 844})
    first_box = items.nth(0).bounding_box()
    second_box = items.nth(1).bounding_box()

    assert first_box is not None
    assert second_box is not None
    assert abs(first_box["x"] - second_box["x"]) < 1
    assert second_box["y"] > first_box["y"]
