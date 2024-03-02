import csv

# Create a list to store the new price history data
new_price_history_data = []

# Open the input CSV file for reading with explicit encoding
with open('AI_description.csv', newline='', encoding='utf-8') as input_file:
    # Create a reader object to read the input CSV file
    reader = csv.DictReader(input_file)

    # Iterate over each row in the input CSV file
    for row in reader:
        # Remove brackets and split the 'price_history' column into a list of values
        price_history = row['price_history'].strip('[]').split(',')
        # Convert each value to float and format it to two decimal places
        formatted_prices = [float(price) / 100 for price in price_history]
        # Append the new price history data as a separate array
        new_price_history_data.append(formatted_prices)

# Reopen the input CSV file for reading with explicit encoding
with open('AI_description.csv', newline='', encoding='utf-8') as input_file:
    # Create a reader object to read the input CSV file again
    reader = csv.DictReader(input_file)

    # Open a new CSV file for writing the combined data
    with open('combined_data.csv', 'w', newline='', encoding='utf-8') as output_file:
        # Define the fieldnames for the CSV writer based on the input CSV file
        fieldnames = reader.fieldnames + ['new_price_history']
        # Create a writer object to write the combined data to the new CSV file
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        # Write the header row to the new CSV file
        writer.writeheader()
        # Combine each row of input data with the corresponding new price history data
        for row, price_history in zip(reader, new_price_history_data):
            row['new_price_history'] = price_history
            writer.writerow(row)
