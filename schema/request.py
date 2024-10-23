def individual_serializer(request) -> dict:
    return {
        # _ its because mongo has and specific way finding a column 
        "id": str(request["_id"]),
        "title": request["title"],
        "description": request["description"],
        "status": request["status"],
        "user_id": request["user_id"],
        "admin_id": request["admin_id"],
        "prediction_id": request["prediction_id"],
        "change_prediction_object": request["change_prediction_object"],
    }

def list_serializer(requests) -> list:
    return [individual_serializer(request) for request in requests]