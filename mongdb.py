from pymongo import MongoClient
import os

# Atlas connection string
MONGO_URI = os.environ.get("MONGO_URI", )
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["college_timetable"]
timetable_collection = db["timetable"]

print("✅ MongoDB Atlas connected successfully!")

