import requests
import json

# Your Keepa API key
API_KEY = '6h8hgj72pe735gpinf05mvap2hslkcnem3dsrhc9b1j92he253mhls1n4fu1e91l'

# ASIN of the product you want to retrieve pricing history for
asin = 'B0B1B3T96K'

# Construct the request URL
url = f'https://api.keepa.com/product?key={API_KEY}&domain=10&asin={asin}&history=1'


# Make the GET request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    
    # Check if the response contains product data
    if 'products' in data and data['products']:
        product_data = data['products'][0]
        
        # Check if the product data contains stats
        if 'stats' in product_data:
            stats = product_data['stats']
            
            # Check if stats is not None
            if stats is not None:
                # Check if the stats contain lowest and list prices
                if 'lowest' in stats and 'listPrice' in stats:
                    lowest_price = stats['lowest']
                    list_price = stats['listPrice']
                    
                    print(f"Lowest Price: {lowest_price}")
                    print(f"List Price: {list_price}")
                else:
                    print("Lowest or list price not available.")
            else:
                print("Stats are None for this product.")
        else:
            print("Stats not available for this product.")
    else:
        print("Product data not available.")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")