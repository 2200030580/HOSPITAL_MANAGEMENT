import gc
import importlib

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import create_app


# shared in-memory engine for all tests
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    # import models so they register with Base
    import app.models.patient  # noqa: F401
    import app.models.doctor  # noqa: F401
    import app.models.appointment  # noqa: F401

    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)

    # dispose test engine
    try:
        engine.dispose()
    except Exception as e:
        print(f"Failed to dispose test engine: {e}")

    # also dispose the app database engine if it was created during tests
    try:
        dbmod = importlib.import_module("app.database")

        if hasattr(dbmod, "engine"):
            try:
                dbmod.engine.dispose()
            except Exception as e:
                print(f"Failed to dispose app database engine: {e}")

        gc.collect()

    except Exception as e:
        print(f"Failed to cleanup test resources: {e}")


def pytest_sessionfinish(session, exitstatus):
    # final cleanup: ensure engines disposed and garbage collected
    try:
        engine.dispose()
    except Exception as e:
        print(f"Failed to dispose test engine: {e}")

    try:
        dbmod = importlib.import_module("app.database")

        if hasattr(dbmod, "engine"):
            try:
                dbmod.engine.dispose()
            except Exception as e:
                print(f"Failed to dispose app database engine: {e}")

        gc.collect()

    except Exception as e:
        print(f"Failed to cleanup test resources: {e}")


@pytest.fixture()
def db_session():
    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()


@pytest.fixture()
def client():
    app = create_app()

    def override_get_db():
        db = TestingSessionLocal()

        try:
            yield db

        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c