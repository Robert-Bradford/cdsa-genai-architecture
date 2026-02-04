from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class Patient(BaseModel):
    id: str
    age: int
    sex: str
    height_in: float = Field(..., description="Height in inches")
    weight_lb: float = Field(..., description="Weight in pounds")

    @property
    def bmi(self) -> float:
        """Calculate BMI using imperial formula: 703 × weight(lb) / height(in)^2"""
        return round((703 * self.weight_lb) / (self.height_in ** 2), 1)


class Vitals(BaseModel):
    blood_pressure: Optional[str]
    heart_rate: Optional[int]


class Labs(BaseModel):
    hba1c: Optional[float]
    ldl: Optional[float]


class ClinicalInput(BaseModel):
    patient: Patient
    vitals: Optional[Vitals]
    labs: Optional[Labs]
    symptoms: Optional[List[str]]
    notes: Optional[str]
    timestamp: datetime
