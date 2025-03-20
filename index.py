from flask import Flask, render_template, request

# Inicializamos la aplicación de Flask
app = Flask(__name__)

# Definimos las rutas de la aplicación
# / es la ruta principal de la aplicación


@app.route("/")
def index():
    return render_template("index.html")


# Inicializamos la aplicación de Flask
if __name__ == "__main__":
    app.run(debug=True)
