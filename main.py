from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.request import router as request_router
from routes.prediction import router as prediction_router
from routes.user import router as user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(prediction_router)
app.include_router(request_router)


origins = [
    "http://localhost:4200",  # tu frontend Angular
    "http://127.0.0.1:4200",  # por si acaso
]

app.add_middleware(
    CORSMiddleware,
    allow_origins="*", 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)