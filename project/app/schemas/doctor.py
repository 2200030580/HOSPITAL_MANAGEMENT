from pydantic import BaseModel, ConfigDict


class DoctorBase(BaseModel):
    name: str
    specialization: str | None = None


class DoctorCreate(DoctorBase):
    pass


class DoctorRead(DoctorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
