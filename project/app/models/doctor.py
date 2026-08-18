from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=True)

    appointments = relationship(
        "Appointment", back_populates="doctor", cascade="all, delete-orphan"
    )
