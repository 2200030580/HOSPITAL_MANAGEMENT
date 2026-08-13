from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.patient import PatientCreate, PatientRead
from app.services.patient_service import create_patient, get_patients, get_patient
from app.database import get_db

router = APIRouter()


@router.post("/", response_model=PatientRead)
def create(p: PatientCreate, db: Session = Depends(get_db)):
    return create_patient(db, p)


@router.get("/", response_model=list[PatientRead])
def list_patients(db: Session = Depends(get_db)):
    return get_patients(db)


@router.get("/{patient_id}", response_model=PatientRead)
def read(patient_id: int, db: Session = Depends(get_db)):
    pat = get_patient(db, patient_id)
    if not pat:
        raise HTTPException(status_code=404, detail="Patient not found")
    return pat


