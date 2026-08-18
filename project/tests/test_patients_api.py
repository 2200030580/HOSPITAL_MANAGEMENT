from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.models.appointment
import app.models.doctor
import app.models.patient
from app.database import Base, get_db
from app.main import create_app

# Create a shared in-memory database for testing
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app = create_app()
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_and_get_patient_api():
    resp = client.post(
        "/patients", json={"name": "API User", "email": "api@example.com"}
    )

    if resp.status_code != 200:
        raise AssertionError(f"Expected status code 200, got {resp.status_code}")

    data = resp.json()

    if "id" not in data:
        raise AssertionError("Response does not contain patient ID")

    pid = data["id"]

    r2 = client.get(f"/patients/{pid}")

    if r2.status_code != 200:
        raise AssertionError(f"Expected status code 200, got {r2.status_code}")

    email = r2.json().get("email")

    if email != "api@example.com":
        raise AssertionError(f"Expected email 'api@example.com', got '{email}'")
