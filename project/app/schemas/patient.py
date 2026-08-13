from pydantic import BaseModel, ConfigDict


class PatientBase(BaseModel):
    name: str
    email: str
    phone: str | None = None


class PatientCreate(PatientBase):
    pass


class PatientRead(PatientBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
