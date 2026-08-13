from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.services.appointment_service import create_appointment, get_appointment
from app.schemas.appointment import AppointmentCreate
from app.models.patient import Patient
from app.models.doctor import Doctor
from datetime import datetime


def test_create_and_get_appointment(db_session):
    db = db_session

    # create patient and doctor
    patient = Patient(name="John Doe", email="john@example.com", phone="123")
    doctor = Doctor(name="Dr Smith", specialization="General")
    db.add(patient)
    db.add(doctor)
    db.commit()
    db.refresh(patient)
    db.refresh(doctor)

    payload = AppointmentCreate(
        patient_id=patient.id,
        doctor_id=doctor.id,
        appointment_start=datetime.fromisoformat("2026-08-20T10:00:00"),
        appointment_end=datetime.fromisoformat("2026-08-20T10:30:00"),
        reason="Checkup",
    )

    created = create_appointment(db, payload)
    assert created.patient_id == patient.id
    assert created.doctor_id == doctor.id

    fetched = get_appointment(db, created.id)
    assert fetched is not None
    assert fetched.id == created.id
    # db fixture handles closing
