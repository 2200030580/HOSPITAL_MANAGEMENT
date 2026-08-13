from sqlalchemy.orm import Session
from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentCreate


def create_appointment(db: Session, appt: AppointmentCreate):
    # appointment_end must be provided
    if appt.appointment_end is None:
        raise ValueError("appointment_end is required")

    # check overlapping appointments for the same doctor
    overlapping = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == appt.doctor_id,
            Appointment.appointment_start < appt.appointment_end,
            Appointment.appointment_end > appt.appointment_start,
        )
        .first()
    )
    if overlapping:
        raise ValueError("appointment time overlaps an existing appointment for this doctor")

    db_appt = Appointment(**appt.model_dump())
    db.add(db_appt)
    db.commit()
    db.refresh(db_appt)
    return db_appt


def get_appointments(db: Session):
    return db.query(Appointment).all()


def get_appointment(db: Session, appointment_id: int):
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()


def delete_appointment(db: Session, appointment_id: int):
    appt = get_appointment(db, appointment_id)
    if appt:
        db.delete(appt)
        db.commit()
        return True
    return False
