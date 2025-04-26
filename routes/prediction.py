from fastapi import APIRouter, HTTPException
from models.prediction import Prediction, PredictionInput
from config.database import cost_estimation_collection
from schema.prediction import list_serializer
from bson import ObjectId
import numpy as np
import pandas as pd
import pickle

router = APIRouter()

# Cargar el modelo y el preprocesador
with open('resources/mejor_modelo_xgboost.pkl', 'rb') as file:
    modelo_xgboost = pickle.load(file)

with open('resources/preprocesador_fs.pkl', 'rb') as file:
    preprocesador = pickle.load(file)

@router.get("/estimation/")
async def get_predictions():
    # Ordenar por _id descendente para obtener el último primero
    resultados = cost_estimation_collection.find().sort("_id", -1)
    return list_serializer(resultados)


@router.get("/estimation-by-user/{user_id}")
async def get_predictions_by_user(user_id: str):
    return list_serializer(cost_estimation_collection.find({"user_id": user_id}))


@router.post("/estimation/predict")
async def post_predict_only(cost_prediction: PredictionInput):
    # Crear un DataFrame con los datos de entrada
    example_input = pd.DataFrame({
        'StructureType': [cost_prediction.structureType],
        'AbutmentType': [cost_prediction.abutmentType],
        'Total Width(M)': [cost_prediction.total_Width],
        'Number of Spans': [cost_prediction.number_of_Spans],
        'Total Length (M)': [cost_prediction.total_Length],
        'Year': [cost_prediction.year]
    })

    try:
        # Aplicar el preprocesamiento
        features_procesadas = preprocesador.transform(example_input)

        # Realizar la predicción en escala logarítmica
        prediccion_log = modelo_xgboost.predict(features_procesadas)

        # Convertir la predicción a la escala original
        prediccion = np.exp(prediccion_log)

        return {
            "predicted_cost": float(prediccion[0])
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en la predicción: {e}")

@router.post("/estimation/save")
async def post_save_prediction(prediction: Prediction):
    try:
        result = cost_estimation_collection.insert_one(prediction.dict())
        return {
            "message": "Predicción guardada correctamente",
            "prediction_id": str(result.inserted_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se pudo guardar la predicción: {e}")


@router.put("/estimation/{id}")
async def put_predict(id: str, cost_prediction: Prediction):
    updated_result = cost_estimation_collection.find_one_and_update(
        {"_id": ObjectId(id)}, 
        {"$set": cost_prediction.dict(exclude={"input_list"})}  # Excluir input_list si no se quiere actualizar
    )
    if not updated_result:
        raise HTTPException(status_code=404, detail="Prediction not found")

@router.delete("/estimation/{id}")
async def delete_predict(id: str):
    result = cost_estimation_collection.find_one_and_delete({"_id": ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail="Prediction not found")
