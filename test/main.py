import os
from selenium import webdriver
from collect import (
    ensure_data_directory_exists,
    configure_firefox_options,
    create_firefox_service,
    save_page_html,
)
from clean import (
    remove_unnecessary_tags,
)
from parser import (
    get_soup,
    get_divs_with_class,
    get_p_contents,
)
from util import (
    write_to_csv,
    convert_price_to_number,
    get_lowest_price_product
)

def main():
    # Collect data
    topics = [
        "jugo",
        "galletas",
        "leche",
        "pan",
        "arroz",
        "pasta",
    ]

    url = "https://domicilios.tiendasd1.com/search?name="
    data_dir = "data"
    binary_location = "/usr/bin/firefox-developer-edition"

    ensure_data_directory_exists(data_dir)
    options = configure_firefox_options(binary_location)
    service = create_firefox_service()

    for topic in topics:
        with webdriver.Firefox(service=service, options=options) as driver:
            file_path = os.path.join(data_dir, f"{topic}.html")
            save_page_html(driver, f"{url}{topic}", file_path)
    
    # Clean data
    cleaned_dir = "cleaned_data"
    ensure_data_directory_exists(cleaned_dir)

    for topic in topics:
        input_file = os.path.join(data_dir, f"{topic}.html")
        output_dir = cleaned_dir
        remove_unnecessary_tags(input_file, output_dir)

    # Parse data
    parsed_data = []

    for topic in topics:
        input_file = os.path.join(cleaned_dir, f"cleaned_{topic}.html")
        soup = get_soup(input_file)
        content = "general__content"
        divs = get_divs_with_class(soup, content)
        
        for div in divs:
            content = get_p_contents(div)
            parsed_data.append(content)

    # Write parsed data to CSV
    csv_file = "data/output.csv"
    write_to_csv(parsed_data, csv_file)

    # Convert price column to numbers
    convert_price_to_number(csv_file)

    prod = input("Enter a product name to search for the lowest price: ")
    # Get lowest price product
    lowest = get_lowest_price_product(prod, csv_file)

    print(f"The product with the lowest price is: {lowest}")


if __name__ == "__main__":
    main()
