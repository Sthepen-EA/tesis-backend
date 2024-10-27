from pydantic import BaseModel

class PredictionInput (BaseModel):
    structureType: str
    abutmentType: str
    total_Width: float
    number_of_Spans: int
    total_Length: float
    year: int

class Prediction (BaseModel):
    input_list: PredictionInput
    total_Cost: float

    class Config:
        arbitrary_types_allowed = True