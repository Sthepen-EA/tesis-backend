from fastapi import APIRouter, HTTPException
from models.request import Request
from config.database import request_collection, cost_estimation_collection
from schema.request import list_serializer
from bson import ObjectId
from bson.errors import InvalidId

router = APIRouter()

@router.get("/request/")
async def get_requests():
    return list_serializer(request_collection.find().sort("_id", -1))

@router.post("/request/create")
async def post_request(request: Request):
    prediction_id = request.prediction_id

    # Buscar la predicción original en la base de datos
    prediction = cost_estimation_collection.find_one({"_id": ObjectId(prediction_id)})

    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")

    if prediction.get("hasRequest", False):
        raise HTTPException(status_code=400, detail="A request has already been created for this prediction")

    # Convertir los objetos anidados a dict
    request_data = request.dict()
    request_data['original_prediction_object'] = request.original_prediction_object.dict()
    request_data['new_prediction_object'] = request.new_prediction_object.dict()

    # Insertar la solicitud en la colección
    request_collection.insert_one(request_data)

    # Actualizar la predicción y marcarla como solicitada
    cost_estimation_collection.update_one(
        {"_id": ObjectId(request.prediction_id)},
        {"$set": {"hasRequest": True}}
    )

    return {"message": "Request created and prediction updated successfully"}

@router.get("/request-by-user/{user_id}")
async def get_requests_by_user(user_id: str):
    return list_serializer(request_collection.find({"user_id": user_id}).sort("_id", -1))

@router.put("/request/{id}")
async def put_request(id: str, request: Request):
    request_data = request.dict()

    prediction_id = request.prediction_id
    try:
        prediction_object_id = ObjectId(prediction_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid prediction_id format")

    # Obtener la predicción original
    original_prediction = cost_estimation_collection.find_one({"_id": prediction_object_id})
    if original_prediction is None:
        raise HTTPException(status_code=404, detail="Original prediction not found")

    request_data['original_prediction_object'] = original_prediction

    # Si fue aprobado y es edición, actualiza
    if request.status == "Aprobado" and request.request_type == "Edición":
        new_prediction_data = request.new_prediction_object.dict()
        cost_estimation_collection.find_one_and_update(
            {"_id": prediction_object_id}, 
            {"$set": new_prediction_data}
        )

    # Si fue aprobado y es eliminación, elimina
    elif request.status == "Aprobado" and request.request_type == "Eliminación":
        cost_estimation_collection.find_one_and_delete({"_id": prediction_object_id})

    # ✅ En todos los casos de edición o eliminación (aprobado o rechazado), liberar el bloqueo
    if request.request_type in ["Edición", "Eliminación"]:
        cost_estimation_collection.update_one(
            {"_id": prediction_object_id},
            {"$set": {"hasRequest": False}}
        )

    # Actualizar el objeto de la solicitud con los nuevos datos
    request_data['new_prediction_object'] = request.new_prediction_object.dict()

    # Actualizar el request
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
