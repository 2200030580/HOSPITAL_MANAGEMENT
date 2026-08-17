from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.services.patient_service import create_patient, get_patient
from app.schemas.patient import PatientCreate


def test_patient_service_create_get():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSession()

    payload = PatientCreate(name="Test User", email="test@example.com", phone="123456")
    created = create_patient(db, payload)
    assert created.email == "test@example.com"  # nosec B101

    fetched = get_patient(db, created.id)
    assert fetched is not None  # nosec B101
    assert fetched.id == created.id  # nosec B101
    db.close()
