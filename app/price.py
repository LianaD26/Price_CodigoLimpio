from flask import Flask, render_template, request
from WebScraper import WebScraper

app = Flask(__name__)

@app.route("/home")
@app.route("/")
def home_page():
    return render_template('home.html')

@app.route("/products", methods=['GET', 'POST'])
def products_page():
    if request.method == 'POST':
        product = request.form['product']
        # Busca el producto en las tiendas
        scraper = WebScraper(product)
        scraper.start_browser()
        #scraped_data = scraper.web_scraping_exito()
        # Pasar los datos obtenidos a la plantilla
        #return render_template('products.html', data=scraped_data)
        return render_template('products.html')
    else:
        return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)

