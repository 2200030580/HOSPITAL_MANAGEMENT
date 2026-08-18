from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.routers import appointments, patients, doctors


def create_app():
    app = FastAPI(
        title="Hospital Appointment Management API",
        description="API for managing patients, doctors, and appointments",
        version="1.0.0",
    )

    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers
    app.include_router(
        appointments.router,
        prefix="/appointments",
        tags=["Appointments"],
    )

    app.include_router(
        patients.router,
        prefix="/patients",
        tags=["Patients"],
    )

    app.include_router(
        doctors.router,
        prefix="/doctors",
        tags=["Doctors"],
    )

    # Redirect root URL to Swagger docs
    @app.get("/", include_in_schema=False)
    def root():
        return RedirectResponse(url="/docs")

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
