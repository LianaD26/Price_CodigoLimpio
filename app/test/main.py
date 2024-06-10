import os
from selenium import webdriver
from .collect import ensure_data_directory_exists,configure_chrome_options,save_page_html, create_chrome_service
from .clean import remove_unnecessary_tags
from .parser_ import get_soup, find_tags_with_class, findAll_tags_with_class
from .util import save_data_to_mysql

class MainController:
    def __init__(self, name_product) -> None:
        self.name = name_product
        self.url = f"https://domicilios.tiendasd1.com/search?name={self.name}"
        self.data_dir = "data"
        self.binary_location = "/usr/bin/brave-browser"

        ensure_data_directory_exists(self.data_dir)
        self.options = configure_chrome_options(self.binary_location)
        self.service = create_chrome_service()

    def main(self):
        with webdriver.Chrome(service=self.service, options=self.options) as driver:
            file_path = os.path.join(self.data_dir, f"{self.name}.html")
            save_page_html(driver, f"{self.url}", file_path)
        
        # Clean data
        cleaned_dir = "cleaned_data"
        ensure_data_directory_exists(cleaned_dir)

        input_file = os.path.join(self.data_dir, f"{self.name}.html")
        output_dir = cleaned_dir
        remove_unnecessary_tags(input_file, output_dir)

        # Parse data

        input_file = os.path.join(cleaned_dir, f"cleaned_{self.name}.html")
        soup = get_soup(input_file)
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

        # Save on db
        save_data_to_mysql(self.name, names, prices, links_imgs)
