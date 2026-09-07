from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime
from typing import Annotated

class ConsultationCreate(BaseModel):
    patient_name: str = Field(min_length=1, max_length=100)
    notes: str | None = Field(default=None, min_length=1, max_length=5000)
    diagnosis_ids: list[Annotated[int, Field(gt=0)]] = Field(min_length=1)

    @field_validator("patient_name", "notes")
    @classmethod
    def strip_and_check_not_blank(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value

    @field_validator("diagnosis_ids")
    @classmethod
    def no_duplicate_ids(cls, value: list[int]) -> list[int]:
        if len(set(value)) != len(value):
            raise ValueError("diagnosis_ids must not contain duplicates")
        return value


class ConsultationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_name: str
    notes: str | None
    diagnosis_ids: list[int]
    created_at: datetime