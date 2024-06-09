# Description: Collects the HTML of a page and saves it to a file.
# The script uses Selenium to open a webpage, wait for the page to load, and save the HTML content to a file.

import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def ensure_data_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def configure_firefox_options(binary_location):
    options = FirefoxOptions()
    options.headless = True
    options.binary_location = binary_location
    return options


def create_firefox_service():
    return FirefoxService(GeckoDriverManager().install())


def save_page_html(driver, url, file_path):
    driver.get(url)
     # Wait until the page is loaded completely (the product image is present)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.prod__figure__img')))
    html = driver.page_source
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html)


def main():
    url = "https://domicilios.tiendasd1.com/search?name=jugo"
    data_dir = "data"
    binary_location = "/usr/bin/firefox-developer-edition"

    ensure_data_directory_exists(data_dir)
    options = configure_firefox_options(binary_location)
    service = create_firefox_service()

    with webdriver.Firefox(service=service, options=options) as driver:
        file_path = os.path.join(data_dir, "page.html")
        save_page_html(driver, url, file_path)


if __name__ == "__main__":
    main()
