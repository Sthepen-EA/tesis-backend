# schema/request.py
def individual_serializer(request) -> dict:
    return {
        "id": str(request["_id"]),
        "prediction_id": request["prediction_id"],
        "request_type": request["request_type"],
        "user_id": request["user_id"],
        "user_name": request["user_name"],
        "date": request["date"],
        "original_prediction_object": {
            **request["original_prediction_object"],
            "_id": str(request["original_prediction_object"].get("_id", ""))
        } if request.get("original_prediction_object") else None,
        "new_prediction_object": request["new_prediction_object"],
        "status": request["status"],
        "project_id": request["project_id"],
    }

def list_serializer(requests) -> list:
    return [individual_serializer(request) for request in requests]
