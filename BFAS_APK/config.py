# config.py

from pymongo import MongoClient

# MongoDB configuration
DATABASE_NAME = 'finance_analyzer'
COLLECTION_NAME = 'users'
DB_URI = 'mongodb://localhost:27017/'

# Function to connect to MongoDB and return the collection
def get_db_collection():
    client = MongoClient(DB_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    return collection
