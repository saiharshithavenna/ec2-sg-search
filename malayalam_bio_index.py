import json

# Load the JSON data from the file
with open('simpleghar.bio_malayalam.json', 'r', encoding='utf-8') as f:
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

# Specify the path for the new JSON file
output_file_path = 'updated_simpleghar.bio_index_malayalam.json'

# Write the updated data to the new JSON file
with open(output_file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Updated data has been written to:", output_file_path)
