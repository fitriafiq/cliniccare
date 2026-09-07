from sqlalchemy import String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.database import Base

class Diagnosis(Base):
    __tablename__ = "diagnosis_codes"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String, unique=True)
    description: Mapped[str] = mapped_column(String)
    consultations = relationship("ConsultationDiagnosis", back_populates="diagnosis")


class Consultation(Base):
    __tablename__ = "consultations"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_name: Mapped[str] = mapped_column(String, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    diagnoses = relationship("ConsultationDiagnosis", back_populates="consultation", cascade="all, delete-orphan")

    @property
    def diagnosis_ids(self) -> list[int]:
        return [cd.diagnosis_id for cd in self.diagnoses]


class ConsultationDiagnosis(Base):
    __tablename__ = "consultation_diagnoses"

    consultation_id: Mapped[int] = mapped_column(ForeignKey("consultations.id"), primary_key=True)
    diagnosis_id: Mapped[int] = mapped_column(ForeignKey("diagnosis_codes.id"), primary_key=True)
    consultation = relationship("Consultation", back_populates="diagnoses")
    diagnosis = relationship("Diagnosis", back_populates="consultations")