from flask import Flask, render_template, request
from .test import main


app = Flask(__name__)

@app.route("/home")
@app.route("/")
def home_page():
    return render_template('home.html')

@app.route("/products", methods=['GET', 'POST'])
def products_page():
    if request.method == 'POST':
        store = request.form.get('store', None)
        product = request.form['product']
        controller = main.MainController(product)
        controller.main()
        #action = request.form['action']
        return render_template('products.html')
    else:
        return render_template('home.html')



if __name__ == "__main__":
    app.run(debug=True)

