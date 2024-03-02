import csv
import requests
import time
import logging
import pymongo
import json
from fastapi import HTTPException
import re
from fastapi import FastAPI
import os 
app = FastAPI()
 
mongodb_uri = "mongodb+srv://sgcom_moderator:jgmrEz9tkqKQIRl4@simpleghar-com-moderato.xyvcsdq.mongodb.net/"
 
client = pymongo.MongoClient(mongodb_uri )
db = client["product"]
collection = db["product1"]
 
 
logging.basicConfig(filename='api_requests.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
 
api_key = "6h8hgj72pe735gpinf05mvap2hslkcnem3dsrhc9b1j92he253mhls1n4fu1e91l"
 




def get_product_details(asin, api_key, retries=0):
    retries += 1
    try:
        start_time = time.time() 
        url = f"https://api.keepa.com/product?key={api_key}&domain=10&asin={asin}&stats=180&offers=40"
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        end_time = time.time()  
        response_time = end_time - start_time  

        title = data['products'][0]['title']
        description_list = data["products"][0]["features"]
        description = "\n".join(description_list) if description_list else None  

        category = data['products'][0]["categoryTree"][-1]["name"]
        images_csv = data['products'][0]['imagesCSV']
        image_filenames = images_csv.split(',')
        base_url = "https://images-na.ssl-images-amazon.com/images/I/"
        image_urls = base_url + image_filenames[0]
        stats = data['products'][0]['stats']

        price_avg = [array[1] for array in stats.values() if isinstance(array, list) and len(array) > 18]
        price_history = price_avg[1:-4]

        current = stats["current"]
        rank = current[3] if len(current) >= 18 else None
        rating = current[16] / 10 if len(current) >= 18 else None
        rating_count = current[17] if len(current) >= 18 else None
        price = current[1] / 100 if len(current) >= 18 else None

        product = {
            'asin': asin,
            'category': category,
            'rank': rank,
            'image_urls': image_urls,
            'rating': rating,
            'rating_count': rating_count,
            'price': price,
            'price_history': price_history,
            'title': title,
            'description': description
        }
        collection.insert_one(product)
        logging.info(f"Inserted product details for ASIN {asin} into MongoDB")
        logging.info(f"ASIN: {asin}, Response Time: {response_time:.2f} seconds")
        print("Data retrieved:", product)
        return product

    except requests.exceptions.RequestException as e:
        print(f"Error fetching product details for ASIN {asin}: {e}")
        logging.error(f"Error fetching product details for ASIN {asin}: {e}")
        if retries < 3:
            print(f"Retrying request for ASIN {asin}... Attempt {retries}/{retries}")
            time.sleep(80) 
            retries += 1
            return get_product_details(asin, api_key, retries)
        else:
            print(f"Max retries exceeded for ASIN {asin}. Unable to fetch product details.")
            return None

    except (KeyError, IndexError) as e:
        print(f"Error processing product details for ASIN {asin}: {e}")
        logging.error(f"Error processing product details for ASIN {asin}: {e}")
        if retries < 3:
            logging.info(f"Retrying request for ASIN {asin}... Attempt {retries}/{retries}")
            time.sleep(80) 
            retries += 1
            return get_product_details(asin, api_key, retries)
        else:
            logging.error(f"Max retries exceeded for ASIN {asin}. Unable to fetch product details.")
            return None

def process_asins_csv(filename):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            asin = row[0].strip()  # Assuming ASIN is in the first column
            get_product_details(asin, api_key)

if __name__ == "__main__":
    asins_csv = "asins.csv" # Change to the path of your asins.csv file
    if os.path.exists(asins_csv):
        process_asins_csv(asins_csv)
    else:
        print(f"File not found: {asins_csv}")
