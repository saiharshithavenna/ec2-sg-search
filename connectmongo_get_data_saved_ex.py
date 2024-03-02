import json
from pymongo import MongoClient
from bson import ObjectId

# Load the JSON data from the file
with open('simpleghar.bio_kannada.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convert the '_id' field to the correct format
for item in data:
    item['_id'] = str(ObjectId(item['_id']['$oid']))

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')  # Assuming MongoDB is running on localhost:27017
db = client['Kannada']  # Replace 'your_database_name' with the name of your database
collection = db['Index_added']  # Replace 'your_collection_name' with the name of your collection

# Insert the data into MongoDB
collection.insert_many(data)

print("Data has been inserted into MongoDB.")
