from pydantic import BaseModel
from models.prediction import Prediction

class Request(BaseModel):
    prediction_id: str
    request_type: str
    user_id: str
    user_name: str
    date: str
    original_prediction_object: Prediction
    new_prediction_object: Prediction
    status: str
    project_id: str

    # Configuración para permitir convertir a dict recursivamente
    class Config:
        arbitrary_types_allowed = True
