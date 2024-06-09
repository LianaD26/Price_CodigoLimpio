from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re

class WebScraper:

    def __init__(self, name_product) -> None:
        self.url = f"https://domicilios.tiendasd1.com/search?name={name_product}"


    def start_browser(self):
        # Configurar opciones de Brave
        options = Options()
        options.binary_location = "/usr/bin/brave-browser"

        # Crear instancia de servicio para ChromeDriver
        service = Service('/usr/local/bin/chromedriver/chromedriver')

        # Iniciar el navegador
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(self.url)

        self.html = driver.page_source
        driver.quit()

    def get_div_tags(self):
        self.soup = BeautifulSoup(self.html, 'html.parser')

        divi = self.soup.findAll('div')
        first_div_elements = []
        for element in divi:
            first_div = self.get_first_div_with_regex(element)
            if first_div:
                first_div_elements.append(first_div)

        return first_div_elements

    def web_scraping_d1(self):
        dd = self.soup.find('div', {'class': 'banners-container'})
        for i in dd:
            print(i)

    def get_first_div_with_regex(self, element):
        div_pattern = re.compile(r'<*[^>]*>')

        element_str = str(element)
        match = div_pattern.search(element_str)
        if match:
            return match.group(0)
        return None
