def test_create_appointment_api(client):
    # create patient
    rp = client.post("/patients", json={"name": "Pt", "email": "pt@example.com"})
    assert rp.status_code == 200  # nosec B101
    pid = rp.json()["id"]

    # create doctor
    rd = client.post("/doctors", json={"name": "Dr A", "specialization": "Gen"})
    assert rd.status_code == 200  # nosec B101
    did = rd.json()["id"]

    # create appointment
    ap = client.post(
        "/appointments",
        json={
            "patient_id": pid,
            "doctor_id": did,
            "appointment_start": "2026-09-01T09:00:00",
            "appointment_end": "2026-09-01T09:30:00",
        },
    )
    assert ap.status_code == 200  # nosec B101
    aid = ap.json()["id"]

    g = client.get(f"/appointments/{aid}")
    assert g.status_code == 200  # nosec B101
    assert g.json()["patient_id"] == pid  # nosec B101


def test_reject_overlapping_appointment_api(client):
    # create patient
    rp = client.post("/patients", json={"name": "Pt2", "email": "pt2@example.com"})
    assert rp.status_code == 200  # nosec B101
    pid = rp.json()["id"]

    # create doctor
    rd = client.post("/doctors", json={"name": "Dr B", "specialization": "Gen"})
    assert rd.status_code == 200  # nosec B101
    did = rd.json()["id"]

    # create initial appointment 09:00-10:00
    ap1 = client.post(
        "/appointments",
        json={
            "patient_id": pid,
            "doctor_id": did,
            "appointment_start": "2026-09-02T09:00:00",
            "appointment_end": "2026-09-02T10:00:00",
        },
    )
    assert ap1.status_code == 200  # nosec B101

    # overlapping appointment 09:30-10:30 should be rejected
    ap2 = client.post(
        "/appointments",
        json={
            "patient_id": pid,
            "doctor_id": did,
            "appointment_start": "2026-09-02T09:30:00",
            "appointment_end": "2026-09-02T10:30:00",
        },
    )
    assert ap2.status_code == 400  # nosec B101

    # adjacent appointment 10:00-11:00 should be allowed
    ap3 = client.post(
        "/appointments",
        json={
            "patient_id": pid,
            "doctor_id": did,
            "appointment_start": "2026-09-02T10:00:00",
            "appointment_end": "2026-09-02T11:00:00",
        },
    )
    assert ap3.status_code == 200  # nosec B101


def test_create_appointment_missing_end_returns_400(client, db_session):
    # create patient and doctor via client to exercise routers
    rp = client.post(
        "/patients", json={"name": "Alice", "email": "alice@example.com", "phone": "1"}
    )
    assert rp.status_code == 200  # nosec B101
    pid = rp.json()["id"]
    rd = client.post("/doctors", json={"name": "Dr X", "specialization": "Spec"})
    assert rd.status_code == 200  # nosec B101
    did = rd.json()["id"]

    payload = {
        "patient_id": pid,
        "doctor_id": did,
        "appointment_start": "2026-08-20T09:00:00",
        # missing appointment_end
        "reason": "Missing end",
    }

    res = client.post("/appointments/", json=payload)
    assert res.status_code == 400  # nosec B101
    assert "appointment_end" in res.json().get("detail", "")  # nosec B101


def test_delete_appointment_service_and_not_found(client, db_session):
    db = db_session
    # create patient and doctor
    rp = client.post(
        "/patients", json={"name": "Carol", "email": "carol@example.com", "phone": "2"}
    )
    assert rp.status_code == 200  # nosec B101
    pid = rp.json()["id"]
    rd = client.post("/doctors", json={"name": "Dr Y", "specialization": "Spec"})
    assert rd.status_code == 200  # nosec B101
    did = rd.json()["id"]

    ap = client.post(
        "/appointments",
        json={
            "patient_id": pid,
            "doctor_id": did,
            "appointment_start": "2026-08-21T11:00:00",
            "appointment_end": "2026-08-21T11:20:00",
        },
    )
    assert ap.status_code == 200  # nosec B101
    aid = ap.json()["id"]

    # delete via service to cover service logic
    from app.services.appointment_service import delete_appointment

    deleted = delete_appointment(db, aid)
    assert deleted is True  # nosec B101

    # GET should now return 404
    res = client.get(f"/appointments/{aid}")
    assert res.status_code == 404  # nosec B101
