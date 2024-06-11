from .d1_controller import D1Controller
from .exito_controller import ExitoController

from flask import Blueprint, render_template, request

app = Blueprint('main', __name__)

@app.route("/home")
@app.route("/")
def home_page():
    return render_template('home.html')

@app.route("/products", methods=['GET', 'POST'])
def products():
    store = request.form.get('store', None)
    latitud = request.form.get('latitud', None)
    longitud = request.form.get('longitud', None)
    product = request.form.get('product', None)
    ubicaciones = {}
    products = []

    if latitud and longitud:
        ubicaciones = D1Controller(product).locations(latitud, longitud)

    if store == 'action1':
        products = D1Controller(product).get_products()
    elif store == 'action2':
        products = ExitoController(product).get_products()

    return render_template('products.html', products=products, product=product, ubicaciones=ubicaciones)


if __name__ == "__main__":
    app.run(debug=True)
