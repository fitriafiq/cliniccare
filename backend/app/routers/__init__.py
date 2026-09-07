from fastapi import APIRouter
from .consultation import router as consultation_router
from .diagnosis import router as diagnosis_router

api_router = APIRouter()

api_router.include_router(consultation_router)
api_router.include_router(diagnosis_router)