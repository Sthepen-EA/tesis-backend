def individual_serializer(user) -> dict:
    return {
        # _ its because mongo has and specific way finding a column 
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "phone": user["phone"],
        "state": user["state"],
        "password": user["password"],
        "role": user["role"]
    }

def list_serializer(users) -> list:
    return [individual_serializer(user) for user in users]
