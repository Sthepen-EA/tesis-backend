from pydantic import BaseModel

class Prediction (BaseModel):
    structureType: str
    superstructureType: str
    abutmentType: str
    piles: str
    maintenance_Protection_of_Traffic: str
    total_Width: float
    number_of_Spans: int
    total_Length: float
    total_Cost: float
    year: int
    month: int
    day: int