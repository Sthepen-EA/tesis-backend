def individual_serializer(cost_prediction) -> dict:
    return {
        # _ its because mongo has and specific way finding a column 
        "id": str(cost_prediction["_id"]),
        "structureType": cost_prediction["structureType"],
        "superstructureType": cost_prediction["superstructureType"],
        "abutmentType": cost_prediction["abutmentType"],
        "piles": cost_prediction["piles"],
        "maintenance_Protection_of_Traffic": cost_prediction["maintenance_Protection_of_Traffic"],
        "total_Width": cost_prediction["total_Width"],
        "number_of_Spans": cost_prediction["number_of_Spans"],
        "total_Length": cost_prediction["total_Length"],
        "total_Cost": cost_prediction["total_Cost"],
        "year": cost_prediction["year"],
        "month": cost_prediction["month"],
        "day": cost_prediction["day"]
    }

def list_serializer(cost_predictions) -> list:
    return [individual_serializer(cost_prediction) for cost_prediction in cost_predictions]
