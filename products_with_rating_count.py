import requests
import pymongo
import time

key="6h8hgj72pe735gpinf05mvap2hslkcnem3dsrhc9b1j92he253mhls1n4fu1e91l"
# Construct the base URL
url = f"https://api.keepa.com/query?domain=10&key={key}"

mongodb_uri = "mongodb+srv://sgcom_moderator:jgmrEz9tkqKQIRl4@simpleghar-com-moderato.xyvcsdq.mongodb.net/"

client = pymongo.MongoClient(mongodb_uri )
db = client["simpleghar1"] 
collection = db["high_review_product_1"]

duration = 1800  # Half an hour = 30 minutes = 1800 seconds

# Get the current time to calculate the end time
start_time = time.time()
end_time = start_time + duration

# Define the payload for the initial request
initial_payload = {
    "page": 1,
    "perPage": 50,  # Adjust perPage as needed
    "current_COUNT_REVIEWS_gte": 1000
}

# Initialize a list to store all ASINs
all_asins = []

# Make the initial POST request with the payload
response = requests.post(url, json=initial_payload)
data = response.json()

# Extract the asinList from the initial response
asin_list = data.get("asinList", [])

# Add the initial asinList to the list of all ASINs
all_asins.extend(asin_list)

# Check if there are more pages and continue fetching ASINs if needed
total_results = data.get("totalResults", 0)
per_page = initial_payload.get("perPage", 50)
current_page = initial_payload["page"]

while len(all_asins) < total_results and time.time() < end_time:
    # Increment page number for the next request
    current_page += 1
    
    # Define the payload for the next request
    next_payload = {
        "page": current_page,
        "perPage": per_page,
        "current_COUNT_REVIEWS_gte": 1000
    }
    
    # Make the next POST request with the payload
    response = requests.post(url, json=next_payload)
    data = response.json()
    
    # Extract the asinList from the response and add it to the list of all ASINs
    asin_list = data.get("asinList", [])
    collection.insert_one({"asins": asin_list})  # Insert the list of ASINs into MongoDB
    all_asins.extend(asin_list)

# Print all ASINs
print(all_asins)