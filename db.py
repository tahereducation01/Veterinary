import os
from flask_pymongo import PyMongo

def init_db(app):
    mongo_uri = os.environ.get("MONGO_URI")
    
    if not mongo_uri:
        print("❌ MONGO_URI not found in environment variables.")
        return None

    print(f"📡 Connecting to MongoDB at: {mongo_uri}")
    app.config["MONGO_URI"] = mongo_uri
    mongo = PyMongo(app)
    print("✅ MongoDB connection established successfully!")
    return mongo
