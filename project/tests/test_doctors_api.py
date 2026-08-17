def test_create_and_get_doctor_api(client):
    resp = client.post("/doctors", json={"name": "API Doc", "specialization": "ENT"})
    assert resp.status_code == 200  # nosec B101
    data = resp.json()
    assert "id" in data  # nosec B101
    did = data["id"]

    r2 = client.get(f"/doctors/{did}")
    assert r2.status_code == 200  # nosec B101
    assert r2.json()["specialization"] == "ENT"  # nosec B101
