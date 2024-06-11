# Description: Collects the HTML of a page and saves it to a file.
# The script uses Selenium to open a webpage, wait for the page to load, and save the HTML content to a file.

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions


def ensure_data_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def configure_chrome_options(binary_location):
    options = ChromeOptions()
    options.headless = True
    options.binary_location = binary_location
    return options


def save_page_html(driver, url, file_path, selector):
    driver.get(url)
     # Wait until the page is loaded completely
    wait = WebDriverWait(driver, 40)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
    html = driver.page_source
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html)

def create_chrome_service():
    return ChromeService('/usr/local/bin/chromedriver/chromedriver')
