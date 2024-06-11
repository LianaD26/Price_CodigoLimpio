# web scraping D1

import os
from selenium import webdriver
from test.collect import ensure_data_directory_exists,configure_chrome_options,save_page_html, create_chrome_service
from test.clean import remove_unnecessary_tags
from test.parser_ import get_soup, find_tags_with_class, findAll_tags_with_class

from bs4 import BeautifulSoup
from unidecode import unidecode
from .locations_scraper import scraper

class D1Scraper:
    def __init__(self, name_product) -> None:
        self.name = name_product
        self.url = f"https://domicilios.tiendasd1.com/search?name={self.name}"
        self.data_dir = "data_D1"
        self.binary_location = "/usr/bin/brave-browser"

        ensure_data_directory_exists(self.data_dir)
        self.options = configure_chrome_options(self.binary_location)
        self.service = create_chrome_service()

    def scrape(self):
        with webdriver.Chrome(service=self.service, options=self.options) as driver:
            file_path = os.path.join(self.data_dir, f"{self.name}.html")
            save_page_html(driver, f"{self.url}", file_path, 'img.prod__figure__img')
        
        # Clean data
        cleaned_dir = "cleaned_data_D1"
        ensure_data_directory_exists(cleaned_dir)

        input_file = os.path.join(self.data_dir, f"{self.name}.html")
        output_dir = cleaned_dir
        remove_unnecessary_tags(input_file, output_dir)

        # Parse data

        input_file = os.path.join(cleaned_dir, f"cleaned_{self.name}.html")
        soup = get_soup(input_file)

        # products
        products = find_tags_with_class(soup,'div', ['styles__ProductsStyles-sc-824wwv-0', 'jsaLih'])
        
        # prices
        prices = [p.text for p in findAll_tags_with_class(products, 'p', ['CardBasePrice__CardBasePriceStyles-sc-1dlx87w-0 bhSKFL', 'base__price'])]

        all_figures = findAll_tags_with_class(soup, 'figure', ['styles__ImageStyles-sc-j7rcb7-0','CardImage__CardImageStyles-sc-9m4bi8-0','gBUHqz','faGfA'])
        all_imgs = []
        for figure in all_figures:
            imgs = findAll_tags_with_class(figure, 'img', 'prod__figure__img')
            all_imgs.extend(imgs)

        # all imgs
        links_imgs = [img['src'] for img in all_imgs]

        # names
        names = [n.text for n in findAll_tags_with_class(products, 'p', ['CardName__CardNameStyles-sc-147zxke-0', 'bWeSzf', 'prod__name'])]        

        return names, prices, links_imgs
    
    def locations():
        html = scraper()
        soup = BeautifulSoup(html, "html.parser")
        all_stores = soup.find('ul', class_ = ['sc-cVtpRj','dEoNGD','js-print-store-container','js-container-processed-7893'])
        names_loc = []
        for store_card in all_stores:
            div = store_card.find('div', class_ = ['sc-c8168687-3','jEdJDM'])
            span = div.find('span', class_ = ['sc-c8168687-5','cpPFtG'])
            if unidecode(span.text.lower()) not in names_loc:
                names_loc.append(unidecode(span.text.lower()))
        for loc in names_loc:
            print(loc)

        # lat,long
        coordenadas = [[6.238454767320597, -75.57359285952302],[6.245441896989911, -75.57039694933381], [6.239684195186485, -75.56802167631855],
                    [6.245368488019906, -75.56737176282621], [6.240172725502689, -75.5816335916621], [6.249135425660002, -75.56716182049792],
                    [6.251535394500132, -75.57041950700557]]
        
        return names_loc, coordenadas
