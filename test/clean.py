# Description: This script reads an HTML file, removes script and style tags, and writes the modified HTML to a new file.
# The script uses the BeautifulSoup library to parse the HTML content and remove specific tags.

import os
from bs4 import BeautifulSoup

def remove_unnecessary_tags(input_file, output_dir):
    # Extract filename without extension
    filename = os.path.basename(input_file)
    filename_no_ext = os.path.splitext(filename)[0]

    with open(input_file, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # Remove script and style tags
    for tag in soup(["script", "style"]):
        tag.extract()

    # Format the HTML
    cleaned_html = soup.prettify()

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Write modified HTML to output file
    output_file = os.path.join(output_dir, f"cleaned_{filename_no_ext}.html")
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(cleaned_html)

def main():
    input_file = "data/page.html"
    output_dir = "data"

    remove_unnecessary_tags(input_file, output_dir)

if __name__ == "__main__":
    main()
