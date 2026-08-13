"""Model package initializer: import models so SQLAlchemy metadata is populated."""

# Import model modules so they are registered with SQLAlchemy metadata
from .patient import Patient
from .doctor import Doctor
from .appointment import Appointment

