from scraping.exito_scraper import ExitoScraper
from models.database_exito import DB_Exito

class ExitoController:
    def __init__(self, product_name):
        self.product_name = product_name
    
    def get_products(self):
        scraper = ExitoScraper(self.product_name)
        nombres, precios, links = scraper.scrape()
        # save that information on db
        self.save_product_db(nombres, precios, links)

        # get all the information from db
        nombres_db, precios_db, links_db = DB_Exito.get_data_to_mysql(self.product_name)
        
        products_format = self.format_products(nombres_db, precios_db, links_db)
        return products_format
    
    def save_product_db(self, names, prices, links_imgs):
        DB_Exito.save_data_to_mysql(self.product_name, names, prices, links_imgs)

    def format_products(self, nombres, precios, links):
        products = []
        for i in range(len(nombres)):
            if i < len(links):
                product = {
                    "name": nombres[i],
                    "price": precios[i],
                    "link" : links[i]
                }
                products.append(product)
            else:
                product = {
                    "name": nombres[i],
                    "price": precios[i],
                    "link" : "Without image..."
                }
                products.append(product)
        return products