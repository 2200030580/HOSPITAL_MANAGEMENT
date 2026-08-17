from app.services.doctor_service import create_doctor, get_doctor, get_doctors
from app.schemas.doctor import DoctorCreate


def test_doctor_service_create_get(db_session):
    payload = DoctorCreate(name="Dr Test", specialization="Cardiology")
    created = create_doctor(db_session, payload)
    assert created.name == "Dr Test"  # nosec B101

    fetched = get_doctor(db_session, created.id)
    assert fetched is not None  # nosec B101
    assert fetched.id == created.id  # nosec B101

    all_docs = get_doctors(db_session)
    assert any(d.id == created.id for d in all_docs)  # nosec B101
