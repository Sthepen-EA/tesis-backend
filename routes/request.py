from fastapi import APIRouter, HTTPException
from models.request import Request
from config.database import request_collection, cost_estimation_collection
from schema.request import list_serializer
from bson import ObjectId
from bson.errors import InvalidId

router = APIRouter()

@router.get("/request/")
async def get_requests():
    return list_serializer(request_collection.find())
    
@router.post("/request/create")
async def post_request(request: Request):
    # Convertimos todo el objeto Request y sus campos anidados a un diccionario
    request_data = request.dict()
    
    # Convertir el objeto Prediction anidado a diccionario
    request_data['change_prediction_object'] = request.change_prediction_object.dict()

    # Insertar la solicitud en la colección
    request_collection.insert_one(request_data)
    return {"message": "Request created successfully"}

@router.put("/request/{id}") 
async def put_request(id: str, request: Request):
    request_data = request.dict()

    # Si el status está en True, actualizamos la estimación de costos
    if request.status:
        prediction_id = request.prediction_id
        cost_prediction = request.change_prediction_object.dict()

        try:
            # Intentamos convertir prediction_id a ObjectId
            prediction_object_id = ObjectId(prediction_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid prediction_id format")
        
        # Actualizamos la estimación de costos
        result = cost_estimation_collection.find_one_and_update(
            {"_id": prediction_object_id}, 
            {"$set": cost_prediction}
        )
        
        if result is None:
            raise HTTPException(status_code=404, detail="Cost estimation not found")

    # Convertir Prediction a diccionario antes de actualizar el request
    request_data['change_prediction_object'] = request.change_prediction_object.dict()

    # Actualizamos la solicitud en la colección de requests
    result = request_collection.find_one_and_update(
        {"_id": ObjectId(id)}, 
        {"$set": request_data}
    )
    
    if result is None:
        raise HTTPException(status_code=404, detail="Request not found")

    return {"message": "Request and cost estimation updated successfully"}

@router.delete("/request/{id}")
async def delete_request(id: str):
    result = request_collection.find_one_and_delete({"_id": ObjectId(id)})
    if result is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return {"message": "Request deleted successfully"}
