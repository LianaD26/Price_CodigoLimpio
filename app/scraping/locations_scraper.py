from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from test.collect import configure_chrome_options,create_chrome_service

def scraper():
    binary_location = "/usr/bin/brave-browser"
    options = configure_chrome_options(binary_location)
    service = create_chrome_service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://www.tiendeo.com.co/Tiendas/medellin/tiendas-d1')
    wait = WebDriverWait(driver, 40)
    element2 = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.sc-c8168687-2')))

    html = driver.page_source
    print(driver.title)
    driver.quit()

    return html