from pymongo import MongoClient
from dotenv import load_dotenv

import os 

load_dotenv()

uri = os.getenv("MOGODB_URI")
try:
    client = MongoClient(uri)

    # Test connection
    print("Successfully connected!")

except Exception as e:
    print("Connection failed:", e)
    

db = client["doc_database"]
collection = db["metadata"]

print(client.list_database_names())


# store only document-level info in MongoDB
def save_metadata(metadata):
    collection.insert_one(metadata)
    
def get_metadata():
    pass
