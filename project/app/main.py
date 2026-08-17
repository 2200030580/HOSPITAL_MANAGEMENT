from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routers import appointments, patients, doctors


def create_app():
    # Set OpenAPI servers to localhost so docs show `localhost:8001` instead of 127.0.0.1
    app = FastAPI(
        title="Hospital Appointment Management API",
        servers=[{"url": "http://localhost:8001"}],
    )
    app.include_router(appointments.router, prefix="/appointments", tags=["appointments"])
    app.include_router(patients.router, prefix="/patients", tags=["patients"])
    app.include_router(doctors.router, prefix="/doctors", tags=["doctors"])
    @app.get("/")
    def root():
        return RedirectResponse(url="/docs", status_code=302)
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
