from pydantic import BaseModel, model_validator, ConfigDict
from datetime import datetime
from typing import Optional


class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_start: datetime
    appointment_end: Optional[datetime] = None
    reason: Optional[str] = None

    @model_validator(mode="after")
    def check_times(self):
        start = self.appointment_start
        end = self.appointment_end
        if end is not None and start is not None and end <= start:
            raise ValueError("appointment_end must be after appointment_start")
        return self


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentRead(AppointmentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
