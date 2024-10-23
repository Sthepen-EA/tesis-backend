from fastapi import APIRouter, HTTPException
from models.user import User
from models.user import UserLogin
from config.database import user_collection
from schema.user import list_serializer
from bson import ObjectId


router = APIRouter()

@router.get("/user/")
async def get_users():
    return list_serializer(user_collection.find())
    
@router.post("/user/create")
async def post_user(user: User):
    user_collection.insert_one(dict(user))  

@router.put("/user/{id}")
async def put_user(id: str, user: User):
    user_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)})

@router.delete("/user/{id}")
async def delete_user(id: str):
    user_collection.find_one_and_delete({"_id": ObjectId(id)})

@router.post("/login")
async def post_user(user: UserLogin):
    db_user = get_user_by_credentials(user.email, user.password)
    
    if db_user:
        return {"success": True, "message": "Login successful"}
    else:
        return {"success": False, "message": "Invalid email or password"}
    
# Función auxiliar para obtener un usuario por email y contraseña
def get_user_by_credentials(email: str, password: str):
    return user_collection.find_one({"email": email, "password": password})