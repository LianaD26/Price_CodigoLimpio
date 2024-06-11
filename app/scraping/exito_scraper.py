# web scraping exito

import os
from selenium import webdriver
from test.collect import ensure_data_directory_exists,configure_chrome_options,save_page_html, create_chrome_service
from test.clean import remove_unnecessary_tags
from test.parser_ import get_soup, findAll_tags_without_class, find_tags_with_class, findAll_tags_with_class

class ExitoScraper:
    def __init__(self, name_product) -> None:
        self.name = name_product
        self.url = f"https://www.exito.com/s?q={self.name}&sort=score_desc&page=0"
        self.data_dir = "data_Exito"
        self.binary_location = "/usr/bin/brave-browser"

        ensure_data_directory_exists(self.data_dir)
        self.options = configure_chrome_options(self.binary_location)
        self.service = create_chrome_service()

    def scrape(self):
        with webdriver.Chrome(service=self.service, options=self.options) as driver:
            file_path = os.path.join(self.data_dir, f"{self.name}.html")
            save_page_html(driver, f"{self.url}", file_path, 'img.imagen_plp')
        
        # Clean data
        cleaned_dir = "cleaned_data_Exito"
        ensure_data_directory_exists(cleaned_dir)

        input_file = os.path.join(self.data_dir, f"{self.name}.html")
        output_dir = cleaned_dir
        remove_unnecessary_tags(input_file, output_dir)

        # Parse data

        input_file = os.path.join(cleaned_dir, f"cleaned_{self.name}.html")
        soup = get_soup(input_file)

        # product
        mi_div = find_tags_with_class(soup, 'div', 'product-grid_fs-product-grid___qKN2')
        products = findAll_tags_with_class(mi_div, 'a', 'link_fs-link__J1sGD')

        names = []
        imgs = []

        for product in products:
            if product.text.strip() != '': 
                names.append(product.text.strip())
            else:
                i = find_tags_with_class(product, 'img', 'imagen_plp')
                imgs.append(i['src'])
        
        data = {}
        for i in range(len(names)):
            if i < len(names) and  i < len(imgs):
                data[names[i]] = [imgs[i]]

        l = findAll_tags_without_class(mi_div, 'h3', 'data-fs-product-card-title', 'true')
        names2 = []
        price = []
        for pr in l:
            products_name = findAll_tags_with_class(pr, 'a', 'link_fs-link__J1sGD')
            products_price = findAll_tags_with_class(pr, 'p', 'ProductPrice_container__price__XmMWA')
            for na in products_name:
                if na.text.strip() != '': 
                    names2.append(na.text.strip())
            for pi in products_price:
                    if pi.text.strip() != '':
                        price.append(pi.text.strip())

        data2 = {}
        for i in range(len(names2)):
            data2[names2[i]] = price[i]

        for i in range(len(data)):
            if list(data.keys())[i] == list(data2.keys())[i]:
                name = list(data.keys())[i]
                price = list(data2.keys())[i]
                data[name].append(data2[price])

        # data that I must return
        names_ = list(data.keys())
        prices_ = [data[x][1] for x in names]
        links_ = [data[x][0] for x in names]

        return names_, prices_, links_