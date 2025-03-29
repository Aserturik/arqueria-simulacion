from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    session,
    request,
    send_file,
    jsonify,
)
from simulacion.juego import Juego
from simulacion.equipo import Equipo
import numpy as np
import json
import sys
import io
import time

app = Flask(__name__)
app.secret_key = "tu_clave_secreta"

JSON_FILE = "simulacion_data.json"

# Deshabilitar prints para mejor rendimiento
DEBUG_MODE = False
original_print = print


def silent_print(*args, **kwargs):
    if DEBUG_MODE:
        original_print(*args, **kwargs)


# Reemplazar la función print en todo el programa
print = silent_print


def convert_numpy(obj):
    if isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(x) for x in obj]
    elif isinstance(obj, np.int64):
        return int(obj)
    else:
        return obj


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/jugar", methods=["POST"])
def jugar():
    tiempo_inicio = time.time()
    original_print("Iniciando simulación...")

    equipo_1 = Equipo("Los tiguere", 5)
    equipo_2 = Equipo("Los jaguares", 5)

    total_juegos = 20000
    todos_resultados = []
    ultimo_juego = None

    for i in range(total_juegos):
        if i % 1000 == 0:
            original_print(
                f"Progreso: {i}/{total_juegos} juegos ({i/total_juegos*100:.1f}%)"
            )

        juego = Juego(equipo_1, equipo_2, num_rondas=10, juego_actual=i + 1)
        juego.jugar_juego_completo()

        resultado_juego = {
            "id_juego": juego.id_juego,
            "jugador_con_mas_suerte": (
                {
                    "nombre": juego.jugador_con_mas_suerte.nombre,
                    "user_id": juego.jugador_con_mas_suerte.user_id,
                    "suerte": juego.jugador_con_mas_suerte.suerte,
                }
                if isinstance(juego.jugador_con_mas_suerte, object)
                and hasattr(juego.jugador_con_mas_suerte, "nombre")
                else "No determinado"
            ),
            "jugador_con_mas_experiencia": (
                {
                    "nombre": juego.jugador_con_mas_experiencia.nombre,
                    "user_id": juego.jugador_con_mas_experiencia.user_id,
                    "experiencia": juego.experiencia_maxima,
                }
                if isinstance(juego.jugador_con_mas_experiencia, object)
                and hasattr(juego.jugador_con_mas_experiencia, "nombre")
                else "No determinado"
            ),
            "equipo_ganador": (
                {
                    "nombre": juego.equipo_ganador_juego.nombre,
                    "puntaje": juego.equipo_ganador_juego.puntaje_juego,
                }
                if juego.equipo_ganador_juego is not None
                else {"nombre": "Empate", "puntaje": 0}
            ),
            "numero_juego": juego.juego_actual,
            "equipo_1": {
                "nombre": juego.equipo1.nombre,
                "rondas_ganadas": juego.equipo1.rondas_ganadas,
                "puntaje_total": juego.equipo1.juegos_ganados,
            },
            "equipo_2": {
                "nombre": juego.equipo2.nombre,
                "rondas_ganadas": juego.equipo2.rondas_ganadas,
                "puntaje_total": juego.equipo2.juegos_ganados,
            },
        }

        todos_resultados.append(convert_numpy(resultado_juego))

        # Almacenar información del último juego
        if i == total_juegos - 1:
            ultimo_juego = resultado_juego

    # Escribir resultados al archivo
    with open("resultados_acumulados.json", "w") as f:
        json.dump(todos_resultados, f)

    tiempo_total = time.time() - tiempo_inicio
    original_print(f"Simulación completada en {tiempo_total:.2f} segundos")

    session["game_id"] = juego.id_juego

    # Importante: devolver una respuesta válida
    return redirect(url_for("graficas"))


@app.route("/resultados_acumulados.json")
def serve_json():
    return send_file("resultados_acumulados.json", mimetype="application/json")


@app.route("/graficas", methods=["GET"])
def graficas():
    return render_template("graficas.html")


if __name__ == "__main__":
    app.run(debug=True)
