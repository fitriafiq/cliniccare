from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.db.database import get_db
from schemas.consultation import ConsultationResponse, ConsultationCreate
from app.db.models import Consultation, ConsultationDiagnosis, Diagnosis

router = APIRouter(prefix="/consultation", tags=["consultation"])

@router.get("/", response_model=list[ConsultationResponse])
def get_consultations(db: Session = Depends(get_db)):
    return db.query(Consultation).all()


@router.post("/", response_model=ConsultationResponse)
def add_consultation(consultation: ConsultationCreate, db: Session = Depends(get_db)):
    found_ids = {
        row.id for row in db.query(Diagnosis.id).filter(Diagnosis.id.in_(consultation.diagnosis_ids)).all()
    }
    missing_ids = set(consultation.diagnosis_ids) - found_ids
    if missing_ids:
        raise HTTPException(status_code=404, detail=f"diagnosis id(s) not found: {missing_ids}")

    data = consultation.model_dump(exclude={"diagnosis_ids"})
    new_consultation = Consultation(**data)
    for diag_id in consultation.diagnosis_ids:
        new_consultation.diagnoses.append(ConsultationDiagnosis(diagnosis_id=diag_id))

    try:
        db.add(new_consultation)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="failed to save consultation")

    db.refresh(new_consultation)
    return new_consultation
