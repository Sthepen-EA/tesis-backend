from fastapi import APIRouter, HTTPException
from models.request import Request
from models.prediction import Prediction
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
    
    # Convertir los objetos Prediction anidados a diccionarios
    request_data['original_prediction_object'] = request.original_prediction_object.dict()
    request_data['new_prediction_object'] = request.new_prediction_object.dict()

    # Insertar la solicitud en la colección
    request_collection.insert_one(request_data)
    return {"message": "Request created successfully"}

@router.get("/request-by-user/{user_id}")
async def get_requests_by_user(user_id: str):
    return list_serializer(request_collection.find({"user_id": user_id}))

@router.put("/request/{id}")
async def put_request(id: str, request: Request):
    request_data = request.dict()

    # Verificar si el estado es "Aprobado" para proceder con la actualización o eliminación
    if request.status == "Aprobado":
        # Buscar y guardar el objeto de predicción original
        prediction_id = request.prediction_id
        try:
            # Intentamos convertir prediction_id a ObjectId
            prediction_object_id = ObjectId(prediction_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid prediction_id format")

        # Obtener la predicción original desde la colección
        original_prediction = cost_estimation_collection.find_one({"_id": prediction_object_id})
        if original_prediction is None:
            raise HTTPException(status_code=404, detail="Original prediction not found")

        # Guardar el objeto original en `original_prediction_object`
        request_data['original_prediction_object'] = original_prediction

        # Verificar si el `request_type` es "Edición" o "Eliminación"
        if request.request_type == "Edición":
            # Convertir `new_prediction_object` a diccionario para actualizarlo
            new_prediction_data = request.new_prediction_object.dict()

            # Actualizar la predicción en la colección de estimaciones de costos
            cost_estimation_collection.find_one_and_update(
                {"_id": prediction_object_id}, 
                {"$set": new_prediction_data}
            )

        elif request.request_type == "Eliminación":
            # Eliminar la predicción en la colección de estimaciones de costos
            cost_estimation_collection.find_one_and_delete({"_id": prediction_object_id})

    # Guardar el `new_prediction_object` en la solicitud
    request_data['new_prediction_object'] = request.new_prediction_object.dict()

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
