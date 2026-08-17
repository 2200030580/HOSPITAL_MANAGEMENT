from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
import app.models.patient  # ensure models are registered with Base.metadata
import app.models.doctor
import app.models.appointment
from app.main import create_app


# create a single shared in-memory engine and session factory for all requests
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
    resp = client.post("/patients", json={"name": "API User", "email": "api@example.com"})
    assert resp.status_code == 200  # nosec B101
    data = resp.json()
    assert "id" in data  # nosec B101
    pid = data["id"]

    r2 = client.get(f"/patients/{pid}")
    assert r2.status_code == 200  # nosec B101
    assert r2.json()["email"] == "api@example.com"  # nosec B101
