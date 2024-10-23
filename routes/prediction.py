from fastapi import APIRouter
from models.prediction import Prediction
from config.database import cost_estimation_collection
from schema.prediction import list_serializer
from bson import ObjectId

router = APIRouter()


@router.get("/estimation/")
async def get_predictions():
    return list_serializer(cost_estimation_collection.find())
    
@router.post("/estimation/predict")
async def post_predict(cost_prediction: Prediction):
    cost_estimation_collection.insert_one(dict(cost_prediction))  

@router.put("/estimation/{id}")
async def put_predict(id: str, cost_prediction: Prediction):
    cost_estimation_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(cost_prediction)})

@router.delete("/estimation/{id}")
async def delete_predict(id: str):
    cost_estimation_collection.find_one_and_delete({"_id": ObjectId(id)})