import json
from pymongo import MongoClient
from bson import ObjectId


with open('simpleghar.bio_kannada.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

id_set = set()

# Check for duplicate _id values
duplicate_ids = []
for item in data:
    item_id = item['_id']['$oid']
    if item_id in id_set:
        duplicate_ids.append(item_id)
    else:
        id_set.add(item_id)

if duplicate_ids:
    print("Duplicate _id values found:", duplicate_ids)
else:
    print("No duplicate _id values found.")

# Create a dictionary to map IDs to index numbers
id_to_index = {item['_id']['$oid']: idx for idx, item in enumerate(data)}

# Update the index numbers based on IDs
for item in data:
    item['index'] = id_to_index[item['_id']['$oid']]

# Generate new unique ObjectId for _id field
for item in data:
    item['_id'] = ObjectId()

for item in data:
    print(item)


client = MongoClient('mongodb://localhost:27017')  
db = client['Kannada'] 
collection = db['Index_added_K']  

# Insert the data into MongoDB
collection.insert_many(data)

print("Data has been inserted into MongoDB.")
