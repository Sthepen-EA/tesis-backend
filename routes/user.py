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
    # Insertar el usuario y obtener el ID del usuario recién creado
    result = user_collection.insert_one(dict(user))
    user_id = str(result.inserted_id)  # Convertir ObjectId a cadena para enviar como respuesta
    return {"user_id": user_id}  # Retornar el ID del usuario en el response body

@router.put("/user/{id}")
async def put_user(id: str, user: User):
    user_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)})
    return {"message": "User updated successfully"}

@router.delete("/user/{id}")
async def delete_user(id: str):
    user_collection.find_one_and_delete({"_id": ObjectId(id)})
    return {"message": "User deleted successfully"}

@router.post("/login")
async def post_user(user: UserLogin):
    db_user = get_user_by_credentials(user.email, user.password)
    
    if db_user:
        user_id = str(db_user["_id"])  # Extraer el ID del usuario y convertirlo a cadena
        return {"success": True, "message": "Login successful", "user_id": user_id}
    else:
        return {"success": False, "message": "Invalid email or password"}
    
# Función auxiliar para obtener un usuario por email y contraseña
def get_user_by_credentials(email: str, password: str):
    return user_collection.find_one({"email": email, "password": password})
