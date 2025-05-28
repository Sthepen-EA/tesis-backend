def individual_serializer(cost_prediction) -> dict:
    return {
        # _ its because mongo has and specific way finding a column 
        "id": str(cost_prediction["_id"]),
        "user_id": cost_prediction["user_id"],
        "input_list": cost_prediction["input_list"],
        "total_Cost": cost_prediction["total_Cost"],
        "project_id": cost_prediction["project_id"],
        "abutmentTypeES": cost_prediction["abutmentTypeES"],
        "structureTypeES": cost_prediction["structureTypeES"],
    }

def list_serializer(cost_predictions) -> list:
    return [individual_serializer(cost_prediction) for cost_prediction in cost_predictions]