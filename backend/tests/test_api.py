def test_seeded_products(client):
    r = client.get("/api/products")
    assert r.status_code == 200
    names = [p["name"] for p in r.json()]
    assert "Blue Mug" in names and len(names) == 8


def test_seed_is_idempotent(client):
    from app.seed import seed
    from app.db import SessionLocal
    with SessionLocal() as s:
        seed(s); seed(s)
    assert len(client.get("/api/products").json()) == 8


def test_search(client):
    assert [p["name"] for p in client.get("/api/products?q=mug").json()] == ["Blue Mug", "Red Mug"]


def test_create_and_update_product_persist(client):
    p = client.post("/api/products", json={"name": "Lamp", "price": 30.0, "stock": 4}).json()
    client.put(f"/api/products/{p['id']}", json={"name": "Desk Lamp", "price": 32.5})
    assert client.get(f"/api/products/{p['id']}").json()["name"] == "Desk Lamp"
    assert "Desk Lamp" in [x["name"] for x in client.get("/api/products").json()]


def test_adjust_stock(client):
    assert client.post("/api/products/1/stock", json={"delta": 5}).json()["stock"] == 25
    assert client.post("/api/products/1/stock", json={"delta": -999}).status_code == 409


def test_order_decrements_stock_and_updates_dashboard(client):
    before = client.get("/api/dashboard").json()
    o = client.post("/api/orders", json={"product_id": 1, "quantity": 2})
    assert o.status_code == 201 and o.json()["total"] == 2 * 12.0
    assert client.get("/api/products/1").json()["stock"] == 18
    after = client.get("/api/dashboard").json()
    assert after["order_count"] == before["order_count"] + 1
    assert after["revenue"] == before["revenue"] + 24.0


def test_order_insufficient_stock(client):
    r = client.post("/api/orders", json={"product_id": 1, "quantity": 10_000})
    assert r.status_code == 409 and r.json()["detail"] == "Not enough stock"
    assert client.get("/api/products/1").json()["stock"] == 20
