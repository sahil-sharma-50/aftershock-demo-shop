import pytest


@pytest.mark.skip(reason="documents PR1 regression; run manually")
def test_update_product_is_stale_on_pr1(client):
    client.get("/api/products/1")  # warms cache
    client.put("/api/products/1", json={"name": "Blue Mug XL", "price": 12.0})
    assert client.get("/api/products/1").json()["name"] == "Blue Mug"  # stale
