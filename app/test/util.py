import pymysql

def create_connection():
    return pymysql.connect(
        host='localhost',
        user='liana',
        password='lia2619',
        database='price'
    )

def save_data_to_mysql(search_criteria, names, prices, images=None):
    connection = create_connection()
    cursor = connection.cursor()

    for name, price, image in zip(names, prices, images):
        if image is None:
            sql = "INSERT INTO products (search_criteria, name, price, link_img) SELECT %s, %s, %s, NULL FROM DUAL WHERE NOT EXISTS (SELECT * FROM products WHERE name = %s)"
            cursor.execute(sql, (search_criteria, name.strip(), price.strip(), name.strip()))
        else:
            sql = "INSERT INTO products (search_criteria, name, price, link_img) SELECT %s, %s, %s, %s FROM DUAL WHERE NOT EXISTS (SELECT * FROM products WHERE name = %s)"
            cursor.execute(sql, (search_criteria, name.strip(), price.strip(), image.strip(), name.strip()))

    connection.commit()
    cursor.close()
    connection.close()


