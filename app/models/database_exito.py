import pymysql

class DB_Exito:

    @classmethod
    def create_connection(cls):
        return pymysql.connect(
            host='localhost',
            user='liana',
            password='lia2619',
            database='price'
        )

    @classmethod
    def save_data_to_mysql(cls, search_criteria, names, prices, images=None):
        connection = cls.create_connection()
        cursor = connection.cursor()

        for name, price, image in zip(names, prices, images):
            if image is None:
                sql = "INSERT INTO products_exito (search_criteria, name, price, link_img) SELECT %s, %s, %s, NULL FROM DUAL WHERE NOT EXISTS (SELECT * FROM products_exito WHERE name = %s)"
                cursor.execute(sql, (search_criteria, name.strip(), price.strip(), name.strip()))
            else:
                sql = "INSERT INTO products_exito (search_criteria, name, price, link_img) SELECT %s, %s, %s, %s FROM DUAL WHERE NOT EXISTS (SELECT * FROM products_exito WHERE name = %s)"
                cursor.execute(sql, (search_criteria, name.strip(), price.strip(), image.strip(), name.strip()))

        connection.commit()
        cursor.close()
        connection.close()
    
    @classmethod
    def get_data_to_mysql(cls, search_criteria):
        names = cls.get_names_to_mysql(search_criteria)
        prices = cls.get_prices_to_mysql(search_criteria)
        links = cls.get_links_to_mysql(search_criteria)
        return names, prices, links

    @classmethod
    def get_names_to_mysql(cls, search_criteria):
        connection = cls.create_connection()
        cursor = connection.cursor()

        query = "SELECT name FROM products_exito WHERE search_criteria = %s"
        cursor.execute(query, (search_criteria,))

        results = cursor.fetchall()

        cursor.close()
        connection.close()

        product_names = [row[0] for row in results]
        return product_names

    @classmethod
    def get_prices_to_mysql(cls, search_criteria):
        connection = cls.create_connection()
        cursor = connection.cursor()

        query = "SELECT price FROM products_exito WHERE search_criteria = %s"
        cursor.execute(query, (search_criteria,))

        results = cursor.fetchall()

        cursor.close()
        connection.close()

        product_prices = [row[0] for row in results]
        return product_prices

    @classmethod
    def get_links_to_mysql(cls, search_criteria):
        connection = cls.create_connection()
        cursor = connection.cursor()

        query = "SELECT link_img FROM products_exito WHERE search_criteria = %s"
        cursor.execute(query, (search_criteria,))

        results = cursor.fetchall()

        cursor.close()
        connection.close()

        product_links = [row[0] for row in results]
        return product_links