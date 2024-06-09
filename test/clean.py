# Description: This script reads an HTML file, removes script and style tags, and writes the modified HTML to a new file.
# The script uses the BeautifulSoup library to parse the HTML content and remove specific tags.

import os
from bs4 import BeautifulSoup


def extract_filename_without_extension(input_file):
    """
    Extracts the filename without the extension from the given input file path.

    Parameters
    ----------
        input_file (str): The path of the input file.

    Returns
    -------
        str: The filename without the extension.

    Example
    -------
        >>> extract_filename_without_extension('/path/to/file.txt')
        'file'
    """
    filename = os.path.basename(input_file)
    return os.path.splitext(filename)[0]


def read_html_file(input_file):
    """
    Reads the contents of an HTML file and returns it as a string.

    Parameters
    ----------
        input_file (str): The path to the HTML file to be read.

    Returns
    -------
        str: The contents of the HTML file as a string.
    """
    with open(input_file, "r", encoding="utf-8") as file:
        return file.read()


def remove_script_and_style_tags(soup):
    """
    Removes script and style tags from the given BeautifulSoup object.

    Parameters
    ----------
    - soup: A BeautifulSoup object representing the HTML document.

    Returns
    -------
    None
    """
    for tag in soup(["script", "style"]):
        tag.extract()


def format_html(soup):
    """
    Formats the given BeautifulSoup object as a prettified HTML string.

    Parameters
    ----------
        soup (BeautifulSoup): The BeautifulSoup object to format.

    Returns
    -------
        str: The prettified HTML string.
    """
    return soup.prettify()


def create_output_directory(output_dir):
    """
    Creates the output directory if it doesn't exist.

    Parameters
    ----------
        output_dir (str): The path of the output directory.

    Returns
    -------
        None
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def write_html_to_file(cleaned_html, output_file):
    """
    Writes the cleaned HTML content to a file.

    Parameters
    ----------
        cleaned_html (str): The cleaned HTML content to be written.
        output_file (str): The path of the output file.

    Returns
    -------
        None
    """
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(cleaned_html)


def remove_unnecessary_tags(input_file, output_dir):
    """
    Removes unnecessary tags from an HTML file and writes the cleaned HTML to an output file.

    Parameters
    ----------
        input_file (str): The path to the input HTML file.
        output_dir (str): The directory where the cleaned HTML file will be saved.

    Returns
    -------
        None
    """
    filename_no_ext = extract_filename_without_extension(input_file)
    html_content = read_html_file(input_file)
    soup = BeautifulSoup(html_content, "html.parser")

    remove_script_and_style_tags(soup)
    cleaned_html = format_html(soup)

    create_output_directory(output_dir)
    output_file = os.path.join(output_dir, f"cleaned_{filename_no_ext}.html")
    write_html_to_file(cleaned_html, output_file)


def main():
    input_file = "data/page.html"
    output_dir = "data"

    remove_unnecessary_tags(input_file, output_dir)

if __name__ == "__main__":
    main()
