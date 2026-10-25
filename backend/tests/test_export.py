def test_export_csv(client):
    r = client.get("/api/orders/export.csv")
    assert r.status_code == 200 and r.headers["content-type"].startswith("text/csv")
    assert r.text.splitlines()[0] == "id,product,quantity,total,created_at"
