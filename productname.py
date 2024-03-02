import pandas as pd

# Define a function to extract the short name
def extract_short_name(name):
    indices = [name.find(','), name.find('('), name.find('|')]
    indices = [idx for idx in indices if idx != -1]  # Filter out -1 values
    if indices:  # Check if there are valid indices
        return name[:min(indices)]
    else:
        return name  # Return the original name if no delimiter found

# Read the CSV file into a DataFrame
df = pd.read_csv('asins_with_image_urls.csv')

# Apply the extract_short_name function to each product name in the "Product Name" column
df['Short Name'] = df['Product_title'].apply(extract_short_name)
print(df)
# Save the DataFrame with the short names to a CSV file
df.to_csv('products_short_names.csv', index=False)
          
print("csv file successful")
