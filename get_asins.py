import pymongo
import csv

mongodb_uri = "mongodb+srv://sgcom_moderator:jgmrEz9tkqKQIRl4@simpleghar-com-moderato.xyvcsdq.mongodb.net/"
client = pymongo.MongoClient(mongodb_uri )
db = client["simpleghar1"] 
collection = db["high_review_product_1"]

with open('asins.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(['ASIN'])
    

    
    # Retrieve all documents from the MongoDB collection
    documents = collection.find({})
    
    # Iterate through each document
    for document in documents:
        # Access the list of ASINs from the document
        asins_list = document.get("asins", [])
        
        # Iterate through each ASIN in the list
        for asin in asins_list:

                writer.writerow([asin])
