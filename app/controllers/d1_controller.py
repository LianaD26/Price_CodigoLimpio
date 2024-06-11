from scraping.d1_scraper import D1Scraper
from models.database_d1 import DB_D1
from math import radians, sin, cos, sqrt, atan2


class D1Controller:
    def __init__(self, product_name):
        self.product_name = product_name
    
    def get_products(self):
        scraper = D1Scraper(self.product_name)
        nombres, precios, links = scraper.scrape()
        # save that information on db
        self.save_product_db(nombres, precios, links)

        # get all the information from db
        nombres_db, precios_db, links_db = DB_D1.get_data_to_mysql(self.product_name)
        
        products_format = self.format_products(nombres_db, precios_db, links_db)
        return products_format
    
    def save_product_db(self, names, prices, links_imgs):
        DB_D1.save_data_to_mysql(self.product_name, names, prices, links_imgs)

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
    
    # obtener las ubicaciones de las tiendas D1 en la ciudad de Medellín

    def locations(self, lat_user, long_user):
        names_stores, locations_stores = D1Scraper.locations()
        radio_tierra_km = 6371.0
        all_locations = {}

        for loc in range(len(locations_stores)):
            #lat, long
            lat = radians(locations_stores[loc][0])
            long = radians(locations_stores[loc][1])
            
            lat_user_rad = radians(float(lat_user))
            long_user_rad = radians(float(long_user))

            dlat = lat - lat_user_rad
            dlong = long - long_user_rad

            # Calcular la distancia utilizando la fórmula del haversine
            a = sin(dlat / 2)**2 + cos(float(lat_user)) * cos(lat) * sin(dlong / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distancia = radio_tierra_km * c
            all_locations[names_stores[loc]] = distancia

        # retorna un dict con clave nombre de la tienda y valor dist en km    
        return all_locations