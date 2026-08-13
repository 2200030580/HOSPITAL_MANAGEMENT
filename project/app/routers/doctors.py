from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.doctor import DoctorCreate, DoctorRead
from app.services.doctor_service import create_doctor, get_doctors, get_doctor
from app.database import get_db

router = APIRouter()


@router.post("/", response_model=DoctorRead)
def create(d: DoctorCreate, db: Session = Depends(get_db)):
    return create_doctor(db, d)


@router.get("/", response_model=list[DoctorRead])
def list_doctors(db: Session = Depends(get_db)):
    return get_doctors(db)


@router.get("/{doctor_id}", response_model=DoctorRead)
def read(doctor_id: int, db: Session = Depends(get_db)):
    doc = get_doctor(db, doctor_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doc


