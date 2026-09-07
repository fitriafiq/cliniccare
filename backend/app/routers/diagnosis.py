from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Diagnosis

router = APIRouter(prefix="/diagnosis", tags=["diagnosis"])

@router.get("/")
def get_diagnosis(search: str = None, db: Session = Depends(get_db)):
    if search is None:
        return db.query(Diagnosis).all()
    else:
        return db.query(Diagnosis).filter(Diagnosis.code.contains(search) | Diagnosis.description.contains(search)).all()
