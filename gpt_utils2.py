import csv
import time
import openai
import json
import os

def ask_gpt(product_name):
    try:
        openai.api_key = "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"
        
        prompt = f"""
            product_name: {product_name}
            instructions: Create a concise and generic name for the product without mentioning any brand, specific features, characteristics, color, size, or capacity. Avoid including measurements as well.

            Response format: 
            {{
                "generic_tag": "Generic product tag"
            }}
            Generate the whole response in valid JSON format only.

            
            """
        
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}]
        )

        response = completion["choices"][0]["message"]["content"]
        
        # Extract tag value from the response
        tag = json.loads(response)["generic_tag"]
        
        return tag
    except Exception as e:
        if "429" in str(e):  # Check if the exception message contains '429', indicating a rate limit error
            print("Rate limit reached. Waiting for 20 seconds before retrying...")
            time.sleep(20)
            return ask_gpt(product_name)
        else:
            raise e  # Re-raise the exception if it's not a rate limit error


# Read existing data from filtered_products.csv and add product tags
with open('filtered_products.csv', mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['tag']  # Add 'tag' as a new fieldname
    
    # Write data to a temporary file
    with open('output_temp.csv', mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # Iterate through each row and add the product tag
        for row in reader:
            product_name = row["Product Name"]
            if product_name.strip(): 
                generic_tag = ask_gpt(product_name)
            else:
                generic_tag = "" 
            print(f" {generic_tag}")  # Print for verification
            row['tag'] = generic_tag
            writer.writerow(row)

# Replace the original file with the temporary file
os.replace('output_temp.csv', 'filtered_products.csv')

print("Product tags have been added to the filtered_products.csv file.")
