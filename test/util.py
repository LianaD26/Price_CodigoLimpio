import os
import csv
import pandas as pd
from difflib import SequenceMatcher

from collect import ensure_data_directory_exists


def read_csv_file(file_path):
    """
    Reads the content of a CSV file and returns it as a list of dictionaries.

    Parameters
    ----------
    - file_path (str): The path of the CSV file to read.

    Returns
    -------
    - list: A list of dictionaries where each dictionary represents a row in the CSV file.
    """
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)
    
def write_to_csv(data, file_path):
    """
    Writes the data to a CSV file.

    Parameters
    ----------
    - data (list of dict): The data to write to the CSV file.
    - file_path (str): The path of the CSV file to write to.

    Returns
    -------
    - None
    """
    ensure_data_directory_exists("data")

    # Check if the csv file already exists
    file_exists = os.path.isfile(file_path)

    # write data to csv file
    with open(file_path, mode='a', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())

        # write header if the file is empty
        if not file_exists:
            writer.writeheader()

        for row in data:
            writer.writerow(row)


def convert_price_to_number(csv_file):
    """
    Convert the price column in a CSV file to numbers.

    Parameters
    ----------
    csv_file (str): The path to the CSV file.

    Returns
    -------
    None
    """
    # Read the CSV into a DataFrame
    df = pd.read_csv(csv_file)

    # Convert the price column to numbers
    df['price'] = df['price'].str.replace('$', '').str.replace(',', '').str.replace('.', '').astype(float)

    # Write the modified DataFrame back to a CSV file
    df.to_csv(csv_file, index=False)

def similar(a, b):
    """
    Calculates the similarity ratio between two strings.

    Parameters
    ----------
    a (str): The first string.
    b (str): The second string.

    Returns
    -------
    float: The similarity ratio between the two strings.
    """
    return SequenceMatcher(None, a, b).ratio()


def get_lowest_price_product(product_name, csv_file):
    """
    Get the product with the lowest price from a CSV file.

    Parameters
    ----------
    - product_name (str): The name of the product to search for.
    - csv_file (str): The path to the CSV file.

    Returns
    -------
    - dict: A dictionary representing the product with the lowest price.
    """
     # Read the CSV file
    data = read_csv_file(csv_file)

     # Find similar product names
    similar_products = []
    for d in data:
        if product_name.lower() in d['name'].lower():
            similar_products.append((d, 1.0))
            continue
        similarity_score = similar(product_name.lower(), d['name'].lower())
        if similarity_score > 0.32:  # Adjust the threshold as needed
            similar_products.append((d, similarity_score))

    if not similar_products:
        return None
    
   # Find the product with the lowest price among similar products
    lowest_price_product = min(similar_products, key=lambda x: float(x[0]['price']))

    return lowest_price_product


def main():
    data = [
        {'name': 'John Doe', 'age': 30, 'city': 'New York'},
        {'name': 'Jane Smith', 'age': 25, 'city': 'Chicago'},
        {'name': 'Tom Brown', 'age': 35, 'city': 'Boston'}
    ]

    file_path = "data/test.csv"

    for d in data:
        write_to_csv([d], file_path)

    # convert_price_to_number("data/output.csv")

    lowest = get_lowest_price_product(input(""), "data/output.csv")
    print(f"The product with the lowest price is: {lowest}")

if __name__ == "__main__":
    main()
