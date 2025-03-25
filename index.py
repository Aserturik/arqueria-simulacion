from flask import Flask, render_template, redirect, url_for
from simulacion.juego import Juego

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/jugar", methods=["POST"])
def jugar():
    juego = Juego(
        "Arqueros del Norte", "Arqueras del Sur", num_jugadores=5, num_rondas=10
    )
    juego.jugar_partida_completa()
    imagen = juego.generar_imagen_resultados()
    # Se arma un resumen del resultado final (según la lógica del juego)
    resultado_final = (
        f"{juego.equipo1.nombre}: {juego.equipo1.rondas_ganadas} rondas vs "
        f"{juego.equipo2.nombre}: {juego.equipo2.rondas_ganadas} rondas."
    )
    return render_template(
        "resultados.html", resultado_final=resultado_final, imagen=imagen
    )


if __name__ == "__main__":
    app.run(debug=True)
