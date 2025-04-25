from pymongo import MongoClient
from pymongo.collection import Collection

def get_games_collection() -> Collection:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["steam_data"]
    return db["discounted_games"]
