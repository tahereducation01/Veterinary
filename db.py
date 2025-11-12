import os
from flask_pymongo import PyMongo

def init_db(app):
    app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
    mongo = PyMongo(app)
    return mongo
