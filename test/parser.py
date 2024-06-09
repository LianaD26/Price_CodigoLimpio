# Print html 

from bs4 import BeautifulSoup

def get_soup(file_path):
    """
    Reads the contents of an HTML file and returns a BeautifulSoup object.

    Parameters
    ----------
    file_path (str): The path to the HTML file.

    Returns
    -------
    BeautifulSoup: A BeautifulSoup object representing the parsed HTML.
    """
    with open(file_path, 'r') as file:
        html = file.read()

    soup = BeautifulSoup(html, 'html.parser')
    return soup

def get_divs_with_class(soup, class_name):
    """
    Returns a list of all div elements with the specified class name.

    Parameters
    ----------
    - soup: BeautifulSoup object representing the HTML document.
    - class_name: The class name to search for.

    Returns
    -------
    - A list of div elements with the specified class name.
    """
    return soup.find_all('div', class_=class_name)

def get_p_contents(div):
    """
    Extracts the contents of `<p>` tags from a given div element.

    Parameters
    ----------
        div (BeautifulSoup): The div element to extract <p> contents from.

    Returns
    -------
        dict: A dictionary containing the extracted contents. The keys are the class names of the <p> tags,
              and the values are the text contents of the <p> tags.
    """
    paragraphs = div.find_all('p')
    content_dict = {}

    for p in paragraphs:
        # If the class is "RAFHO", get the content inside the <span> tag
        if "RAFHO" in p.get('class', []):
            span = p.find('span')
            if span:
                content_dict['RAFHO'] = span.get_text(strip=True)
        # Otherwise, get the text of the <p> tag
        else:
            class_names = [class_name for class_name in p.get('class', [])]
            key = class_names[-1].split('__')[-1]
            content_dict[key] = p.get_text(strip=True)

    return content_dict


def main():
    soup = get_soup('data/cleaned_page.html')

    content = "general__content"

    divs = get_divs_with_class(soup, content)

    for div in divs:
        content = get_p_contents(div)
        print(content)

if __name__ == "__main__":
    main()
