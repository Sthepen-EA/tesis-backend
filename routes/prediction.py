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
    return list_serializer(cost_estimation_collection.find())

@router.post("/estimation/predict")
async def post_predict(cost_prediction: PredictionInput):
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

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en la predicción: {e}")

    # Crear la instancia de Prediction para almacenar en la base de datos
    new_prediction = Prediction(
        input_list=cost_prediction,
        total_Cost=float(prediccion[0])
    )

    # Guardar la predicción en la base de datos
    result = cost_estimation_collection.insert_one(new_prediction.dict())

    # Devolver la predicción junto con el ID generado
    return {
        "prediction_id": str(result.inserted_id),
        "predicted_cost": float(prediccion[0])
    }

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
