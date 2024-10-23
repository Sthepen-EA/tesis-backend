from fastapi import FastAPI
from routes.request import router as request_router
from routes.prediction import router as prediction_router
from routes.user import router as user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(prediction_router)
app.include_router(request_router)
