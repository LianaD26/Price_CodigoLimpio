from flask import Flask
from controllers.main_controller import app as main_blueprint

app = Flask(__name__)

# Forma de organizar los módulos de mi aplicación
app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
