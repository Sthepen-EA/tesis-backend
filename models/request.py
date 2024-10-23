from pydantic import BaseModel
from models.prediction import Prediction

class Request(BaseModel):
    title: str
    description: str
    status: bool
    user_id: str
    admin_id: str
    prediction_id: str
    change_prediction_object: Prediction

    # Configuración para permitir convertir a dict recursivamente
    class Config:
        arbitrary_types_allowed = True
