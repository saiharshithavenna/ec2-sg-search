import json

# Load the JSON data from the file
with open('simpleghar.bio_kannada.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Create a dictionary to map IDs to index numbers
id_to_index = {item['_id']['$oid']: idx for idx, item in enumerate(data)}

# Update the index numbers based on IDs
for item in data:
    item['index'] = id_to_index[item['_id']['$oid']]

# Specify the path for the new JSON file
output_file_path = 'updated_simpleghar.bio_index_kannada.json'

# Write the updated data to the new JSON file
with open(output_file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Updated data has been written to:", output_file_path)
