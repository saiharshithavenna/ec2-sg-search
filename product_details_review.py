import csv
import requests
import time
import logging
import pymongo
import json
 
import re
from fastapi import FastAPI
 
app = FastAPI()
 
 
mongodb_uri = "mongodb+srv://sgcom_moderator:jgmrEz9tkqKQIRl4@simpleghar-com-moderato.xyvcsdq.mongodb.net/"
client = pymongo.MongoClient(mongodb_uri )
db = client["simpleghar1"]
collection_raw=db["products_raw"]
collection_product=db["products"]
 
logging.basicConfig(filename='api_requests2.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
 
api_key = "6h8hgj72pe735gpinf05mvap2hslkcnem3dsrhc9b1j92he253mhls1n4fu1e91l"
 
 
def get_category_by_asin(asin):
   
    doc = collection_product.find_one({"asin": asin})
    if doc is not None:
        print("data is in db")
    return doc
 
#data=get_category_by_asin("B0CBPHPGYV")
#print(data)
 
def get_product_details(asin, api_key, retries=0):

    print(f"Fetching product details for ASIN: {asin}")
    start_time = time.time()
    product_data = get_category_by_asin(asin)
    end_time = time.time()
    
    if not product_data:
        try:
            start_time = time.time()  # Record start time of the request
            url = f"https://api.keepa.com/product?key={api_key}&domain=10&asin={asin}&stats=180&offers=40"
            response = requests.get(url)
            response.raise_for_status()  
            data = response.json()
            collection_raw.insert_one({
                "asin":asin,
                "raw_data":data
            })
            end_time = time.time()  # Record end time of the request
            response_time = end_time - start_time  # Calculate response time
            title = data['products'][0]['title']
            description_list = data["products"][0]["features"]
            if description_list:
                if isinstance(description_list, str):
                    description = description_list  
                else:
                    description = "\n".join(description_list)
            else:
                description = None
            
            if data.get('products') and data['products'][0].get("categoryTree") and data['products'][0]["categoryTree"][-1].get("name"):
                category = data['products'][0]["categoryTree"][-1]["name"]
            else:
                return "null"
            
            images_csv = data['products'][0].get('imagesCSV')
            if images_csv:
                image_filenames = images_csv.split(',')
                base_url = "https://images-na.ssl-images-amazon.com/images/I/"
                if image_filenames:
                    image_urls = base_url + image_filenames[0]
                else:
                    image_urls = "null"
            else:

               image_urls = "null"
            
            stats = data['products'][0]['stats']
 
            price_avg = []
            for key, array in stats.items():
                if isinstance(array, list) and len(array) > 18:  
                    value = array[18]  
                    price_avg.append(value)
 
            filtered_values = []
            for value in price_avg:
                if isinstance(value, int):
                    filtered_values.append(value)
 
            price_history = filtered_values[1:-4]
            price_history = [value / 100 for value in price_history]
           
            current = stats["current"]
            if len(current) >= 18:
                rank = current[3]
                rating = current[16] / 10
                rating_count = current[17]
                price = current[18] / 100
 
            product_url = f"https://www.amazon.in/dp/{asin}?linkCode=ll1&tag=simpleghar-21"
 
            if rank is not None:
                if price > 0:
                    min = stats["min"][1][1]
                    min_price = min / 100
                    max = stats["max"][1][1]
                    max_price = max / 100
                    avg = stats["avg"][18]
                    avg_price = avg / 100
                else:
                    min_price = "null"
                    max_price = "null"
                    avg_price = "null"
 
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
                    'description': description,
                    'price_range':{
                        "min": min_price,
                        "avg": avg_price,
                        "max": max_price
                    },
                    'product_url': product_url,
                }
                collection_product.insert_one({
                    "asin": asin,
                    "raw_data": product
                })
                print(product)
            end_time = time.time()  
            response_time = end_time - start_time
            logging.info(f"Inserted product details for ASIN {asin} into MongoDB")
            logging.info(f"ASIN: {asin}, Response Time: {response_time:.2f} seconds")
       
        except requests.exceptions.RequestException as e:
            print(f"Error fetching product details for ASIN {asin}: {e}")
            logging.error(f"Error fetching product details for ASIN {asin}: {e}")
            if retries < 3:
                print(f"Retrying request for ASIN {asin}... ")
                time.sleep(80)
                retries += 1 # Wait for 60 seconds before retrying
            else:
                print(f"Max retries exceeded for ASIN {asin}. Unable to fetch product details.")
                return None
 
        except (KeyError, IndexError) as e:
            print(f"Error processing product details for ASIN {asin}: {e}")
            logging.error(f"Error processing product details for ASIN {asin}: {e}")
            if retries < 3:
                logging.info(f"Retrying request for ASIN {asin}... ")
                time.sleep(80)
                retries += 1  # Wait for 60 seconds before retrying
            else:
                logging.error(f"Max retries exceeded for ASIN {asin}. Unable to fetch product details.")
                return None

 

 
def update_csv(input_file, api_key):
    try:
 
        with open(input_file, 'r', encoding='utf-8') as csv_input:
            reader = csv.DictReader(csv_input)
           
            for row in reader:
                asin = row['ASIN']
                print("asin is:",asin)
                data = get_product_details(asin, api_key)
    except IOError as e:
        logging.error(f"Error reading or writing to file: {e}")
 
input_file = 'asins.csv'
 
 
update_csv(input_file,api_key)
 
