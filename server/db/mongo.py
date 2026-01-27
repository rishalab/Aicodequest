from pymongo import MongoClient

# MongoDB connection (local)
client = MongoClient("mongodb://localhost:27017/")
db = client["AIQuest"]

sessions=db["sessions"]