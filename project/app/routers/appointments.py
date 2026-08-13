from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.appointment import AppointmentCreate, AppointmentRead
from app.services.appointment_service import create_appointment, get_appointments, get_appointment
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=AppointmentRead)
def create(appt: AppointmentCreate, db: Session = Depends(get_db)):
    try:
        return create_appointment(db, appt)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[AppointmentRead])
def list_appts(db: Session = Depends(get_db)):
    return get_appointments(db)

@router.get("/{appointment_id}", response_model=AppointmentRead)
def read(appointment_id: int, db: Session = Depends(get_db)):
    appt = get_appointment(db, appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt





