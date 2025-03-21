from flask import Flask, render_template, request
from simulacion.juego import Juego

# Inicializamos la aplicación de Flask
app = Flask(__name__)

# Definimos las rutas de la aplicación
# / es la ruta principal de la aplicación


@app.route("/")
def index():
    return render_template("index.html")


# Inicializamos la aplicación de Flask
#if __name__ == "__main__":
#    app.run(debug=True)


# Crear y simular un juego
juego = Juego(num_rondas=3)
resultados = juego.simular()

# Imprimir resultados
print(f"Ganador del juego: {resultados['ganador_final']}")
print("\nResultados por ronda:")
for ronda in resultados['rondas']:
    print(f"Ronda {ronda['numero_ronda']}: {ronda['puntajes']}")