from bs4 import BeautifulSoup

def get_soup(file_path):
    with open(file_path, 'r') as file:
        html = file.read()

    soup = BeautifulSoup(html, 'html.parser')
    return soup

def find_tags_with_class(soup, tag, class_name):
    return soup.find(f'{tag}', class_=class_name)

def findAll_tags_with_class(soup, tag, class_name):
    return soup.find_all(f'{tag}', class_=class_name)

def find_tags_without_class(soup, tag, parent, child):
    return soup.find(f'{tag}', parent == child)

def findAll_tags_without_class(soup, tag, parent, child):
    return soup.find_all(f'{tag}', parent == child)