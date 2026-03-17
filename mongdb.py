from pymongo import MongoClient
import os

# Atlas connection string
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://cleversiddhant123:<db_password>@cluster0.c9euidi.mongodb.net/?appName=Cluster0")
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["college_timetable"]
timetable_collection = db["timetable"]

print("✅ MongoDB Atlas connected successfully!")

