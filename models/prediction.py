from pydantic import BaseModel

class PredictionInput (BaseModel):
    structureType: str
    abutmentType: str
    total_Width: float
    number_of_Spans: int
    total_Length: float
    year: int

class Prediction (BaseModel):
    user_id: str
    input_list: PredictionInput
    total_Cost: float
    project_id: str
    abutmentTypeES: str
    structureTypeES: str
    hasRequest: bool

    class Config:
        arbitrary_types_allowed = True