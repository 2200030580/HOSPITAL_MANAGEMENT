"""Model package initializer: import models so SQLAlchemy metadata is populated."""

# Import model modules so they are registered with SQLAlchemy metadata
from .appointment import Appointment as Appointment
from .doctor import Doctor as Doctor
from .patient import Patient as Patient

__all__ = ["Appointment", "Doctor", "Patient"]
