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
df = pd.read_csv('AI_description2 (1).csv')

# Apply the extract_short_name function to each product name in the "Product Name" column
df['SN_Product'] = df['Product Name'].apply(extract_short_name)

# Apply the extract_short_name function to each title in the "Title" column
df['SN_Keyword'] = df['Keyword'].apply(extract_short_name)

# Save the DataFrame with the short names to a CSV file
df.to_csv('SN_name_keyword.csv', index=False)
          
print("csv file successful")
