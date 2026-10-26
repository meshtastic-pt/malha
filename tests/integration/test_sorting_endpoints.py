import pytest


def _is_sorted(values, ascending=True):
    """Utility to check if list is sorted, treating None as extreme."""
    # Replace None with extreme values for comparison
    extreme = float("inf") if ascending else float("-inf")
    norm = [v if v is not None else extreme for v in values]
    return all(
        (norm[i] <= norm[i + 1]) if ascending else (norm[i] >= norm[i + 1])
        for i in range(len(norm) - 1)
    )


@pytest.mark.integration
@pytest.mark.api
@pytest.mark.parametrize(
    "sort_by,api_field",
    [
        ("from_node", "from_node_id"),
        ("to_node", "to_node_id"),
        ("hops", "hops"),
    ],
)
def test_packets_sorting(client, sort_by, api_field):
    """Verify that /api/packets/data supports sorting by the given field when ungrouped."""
    for order in ("asc", "desc"):
        resp = client.get(
            f"/api/packets/data?limit=25&sort_by={sort_by}&sort_order={order}&group_packets=false"
        )
        assert resp.status_code == 200
        data = resp.get_json()
        rows = data["data"]
        values = [row.get(api_field) for row in rows]
        if len(values) > 1:
            assert _is_sorted(values, ascending=(order == "asc")), (
                f"Packet sorting failed for {sort_by} {order}"
            )


@pytest.mark.integration
@pytest.mark.api
@pytest.mark.parametrize(
    "malicious",
    [
        "id;DROP TABLE packet_history",
        "(SELECT CASE WHEN 1=1 THEN timestamp ELSE id END)",
        "1=1",
        "timestamp-- ",
        "rssi UNION SELECT 1",
    ],
)
def test_packets_sort_by_injection_is_neutralized(client, malicious):
    """A malicious sort_by must never reach the SQL ORDER BY clause.

    Unknown sort columns fall back to the default ordering, so the endpoint
    returns 200 with the same rows as the default timestamp-desc query rather
    than a 500 from a broken/injected statement.
    """
    resp = client.get(
        "/api/packets/data",
        query_string={
            "limit": 25,
            "sort_by": malicious,
            "sort_order": "desc",
            "group_packets": "false",
        },
    )
    assert resp.status_code == 200

    baseline = client.get(
        "/api/packets/data",
        query_string={
            "limit": 25,
            "sort_by": "timestamp",
            "sort_order": "desc",
            "group_packets": "false",
        },
    ).get_json()["data"]
    got = resp.get_json()["data"]
    assert [row.get("id") for row in got] == [row.get("id") for row in baseline]


@pytest.mark.integration
@pytest.mark.api
def test_packets_sort_order_injection_is_neutralized(client):
    """A malicious sort_order must be normalized to ASC/DESC, never interpolated."""
    resp = client.get(
        "/api/packets/data",
        query_string={
            "limit": 25,
            "sort_by": "timestamp",
            "sort_order": "asc); DROP TABLE packet_history;--",
            "group_packets": "false",
        },
    )
    assert resp.status_code == 200


@pytest.mark.integration
@pytest.mark.api
@pytest.mark.parametrize(
    "sort_by,api_field",
    [
        ("from_node", "from_node_id"),
        ("to_node", "to_node_id"),
        ("hops", "hops"),
    ],
)
def test_traceroute_sorting(client, sort_by, api_field):
    """Verify that /api/traceroute/data supports sorting by the given field when ungrouped."""
    for order in ("asc", "desc"):
        resp = client.get(
            f"/api/traceroute/data?limit=25&sort_by={sort_by}&sort_order={order}&group_packets=false"
        )
        assert resp.status_code == 200
        data = resp.get_json()
        rows = data["data"]
        values = [row.get(api_field) for row in rows]
        if len(values) > 1:
            assert _is_sorted(values, ascending=(order == "asc")), (
                f"Traceroute sorting failed for {sort_by} {order}"
            )
