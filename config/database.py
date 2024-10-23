from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:admin@cluster0.nd3jn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client.cost_estimation_db

cost_estimation_collection = db["cost_estimation_collection"]
user_collection = db["user_collection"]
request_collection = db["request_collection"]

# Here we create the db and collection (its like a table of RDBS)