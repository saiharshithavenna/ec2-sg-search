import csv
import requests
import time
import logging
import pymongo
import json
from fastapi import HTTPException
import re
from fastapi import FastAPI
 
app = FastAPI()
 
mongodb_uri = "mongodb+srv://sgcom_moderator:jgmrEz9tkqKQIRl4@simpleghar-com-moderato.xyvcsdq.mongodb.net/"
 
client = pymongo.MongoClient(mongodb_uri )
db = client["products"]
collection = db["product"]
 
 
logging.basicConfig(filename='api_requests.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
 
api_key = "6h8hgj72pe735gpinf05mvap2hslkcnem3dsrhc9b1j92he253mhls1n4fu1e91l"
 


 
def get_category_by_asin(asin):
    doc = collection.find_one({"asin": asin})
    if doc:
        print("Data retrieved:", doc)
    else:
        print("Data not found for ASIN:", asin)
    return doc


asin="B01LWYDEQ7"
get_category_by_asin(asin)
 
 
def get_product_details(asin, api_key, retries=3):
 
    product_data= get_category_by_asin(asin)
    if not product_data:
 
        for attempt in range(retries):
            try:
                start_time = time.time() 
                url = f"https://api.keepa.com/product?key={api_key}&domain=10&asin={asin}&stats=180&offers=40"
                response = requests.get(url)
                response.raise_for_status()  
                data = response.json()
                end_time = time.time()  
                response_time = end_time - start_time  
                print(asin)
                title = data['products'][0]['title']
                description_list = data["products"][0]["features"]
                if description_list:
                    if isinstance(description_list, str):
                        description = description_list  
                    else:
                        description = "\n".join(description_list)  
                else:
                    description = None  
 
                category = data['products'][0]["categoryTree"][-1]["name"]
                images_csv = data['products'][0]['imagesCSV']
                image_filenames = images_csv.split(',')
                base_url = "https://images-na.ssl-images-amazon.com/images/I/"
                image_urls = base_url + image_filenames[0]
                stats = data['products'][0]['stats']
 
                price_avg = []
                for key, array in stats.items():
                    if isinstance(array, list) and len(array) > 18:  
                        value = array[1]  
                        price_avg.append(value)
 
                filtered_values = []
                for value in price_avg:
                    if isinstance(value, int):
                        filtered_values.append(value)
 
                price_history = filtered_values[1:-4]
               
                current = stats["current"]
                if len(current) >= 18:
                    rank = current[3]
                    rating = current[16] / 10
                    rating_count = current[17]
                    price = current[1] / 100
               
                if rank is not None:
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
                print("data retrieved")
                return product
           
            except requests.exceptions.RequestException as e:
                print(f"Error fetching product details for ASIN {asin}: {e}")
                logging.error(f"Error fetching product details for ASIN {asin}: {e}")
                if attempt < retries - 1:
                    print(f"Retrying request for ASIN {asin}... Attempt {attempt + 1}/{retries}")
                    time.sleep(80) 
                    continue
                else:
                    print(f"Max retries exceeded for ASIN {asin}. Unable to fetch product details.")
                    return None, None, None, None, None, None, None, None, None
 
            except (KeyError, IndexError) as e:
                print(f"Error processing product details for ASIN {asin}: {e}")
                logging.error(f"Error processing product details for ASIN {asin}: {e}")
                if attempt < retries - 1:
                    logging.info(f"Retrying request for ASIN {asin}... Attempt {attempt + 1}/{retries}")
                    time.sleep(80) 
                    continue
                else:
                    logging.error(f"Max retries exceeded for ASIN {asin}. Unable to fetch product details.")
                    return None, None, None, None, None, None, None, None, None
               
    else:
        return product_data



@app.get("/product/{asin}")
async def get_product_details_api(asin: str):
    product_data = get_product_details(asin, api_key)
    if product_data:
        
        product_data['_id'] = str(product_data['_id'])
        return product_data
    else:
        raise HTTPException(status_code=404, detail="Product not found")




@app.get("/product/{asin_or_url:path}")
async def get_product_details_api(asin_or_url: str):
    
    if re.match(r'^[A-Za-z0-9]{10}$', asin_or_url):
        asin = asin_or_url
    else:
       
        asin = extract_asin_from_url(asin_or_url)
        if not asin:
            raise HTTPException(status_code=400, detail="Invalid ASIN or URL provided")

    
    product_data = get_product_details(asin, api_key)
    if product_data:
       
        product_data['_id'] = str(product_data['_id'])
        return product_data
    else:
        raise HTTPException(status_code=404, detail="Product not found")


def extract_asin_from_url(url):
    pattern = r'https://www\.amazon\.in/dp/([A-Z0-9]{10})'
    match = re.findall(pattern, url)
    if match:
        return match[0]  
    return None  



 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
