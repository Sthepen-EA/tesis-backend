def individual_serializer(request) -> dict:
    return {
        # _ its because mongo has and specific way finding a column 
        "id": str(request["_id"]),
        "prediction_id": request["prediction_id"],
        "request_type": request["request_type"],
        "user_id": request["user_id"],
        "date": request["date"],
        "prediction_object": request["prediction_object"],
        "status": request["status"],
    }

def list_serializer(requests) -> list:
    return [individual_serializer(request) for request in requests]