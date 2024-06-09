import os
import csv
import pandas as pd

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


def main():
    data = [
        {'name': 'John Doe', 'age': 30, 'city': 'New York'},
        {'name': 'Jane Smith', 'age': 25, 'city': 'Chicago'},
        {'name': 'Tom Brown', 'age': 35, 'city': 'Boston'}
    ]

    file_path = "data/test.csv"

    for d in data:
        write_to_csv([d], file_path)

    convert_price_to_number("data/output.csv")

if __name__ == "__main__":
    main()
