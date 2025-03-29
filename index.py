from flask import Flask, render_template, redirect, url_for, session, request, send_file
from simulacion.juego import Juego
from simulacion.equipo import Equipo
import numpy as np
import json

app = Flask(__name__)
app.secret_key = "tu_clave_secreta"  # necesaria para usar session

JSON_FILE = "simulacion_data.json"


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
    equipo_1 = Equipo("Lo tiguere", 5)
    equipo_2 = Equipo("Los jaguares", 5)

    # Para resultados acumulados, creamos o limpiamos el archivo al inicio
    with open("resultados_acumulados.json", "w") as f:
        f.write("[\n")  # Iniciamos el array JSON

    total_juegos = 100
    # Guarda solo el último juego para mostrar en la interfaz
    ultimo_juego = None

    for i in range(total_juegos):
        # Crear y jugar el juego
        print(f"\n--- JUEGO {i + 1} ---")
        juego = Juego(equipo_1, equipo_2, num_rondas=10, juego_actual=i + 1)
        juego.jugar_juego_completo()

        resultado_juegos = {
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
                    "experiencia": juego.jugador_con_mas_experiencia.experiencia,
                }
                if isinstance(juego.jugador_con_mas_experiencia, object)
                and hasattr(juego.jugador_con_mas_experiencia, "nombre")
                else "No determinado"
            ),
            "equipo_ganador": {
                "nombre": juego.equipo_ganador_juego.nombre,
                "puntaje": juego.equipo_ganador_juego.puntaje_juego,
            },
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

        # Guardar solo el último juego completo para la interfaz
        if i == total_juegos - 1:
            ultimo_juego = {
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
                        "experiencia": juego.jugador_con_mas_experiencia.experiencia,
                    }
                    if isinstance(juego.jugador_con_mas_experiencia, object)
                    and hasattr(juego.jugador_con_mas_experiencia, "nombre")
                    else "No determinado"
                ),
                "equipo1": {
                    "nombre": juego.equipo1.nombre,
                    "rondas_ganadas": juego.equipo1.rondas_ganadas,
                    "puntaje_total": juego.equipo1.juegos_ganados,
                },
                "equipo2": {
                    "nombre": juego.equipo2.nombre,
                    "rondas_ganadas": juego.equipo2.rondas_ganadas,
                    "puntaje_total": juego.equipo2.juegos_ganados,
                },
            }

            # Escribir cada resultado individual al archivo con coma solo si no es el último
        with open("resultados_acumulados.json", "a") as f:
            f.write(json.dumps(convert_numpy(resultado_juegos), indent=2))
            if i < total_juegos - 1:
                f.write(",\n")
            else:
                f.write("\n]")  # Cerramos el array JSON al final

    session["game_id"] = juego.id_juego

    resultado_final = (
        # Mostrar el puntaje de las rondas ganadas por cada equipo
        f"{juego.equipo1.nombre}: {juego.equipo1.rondas_ganadas} rondas vs "
        f"{juego.equipo2.nombre}: {juego.equipo2.rondas_ganadas} rondas."
    )
    # Mostrar los equipos y sus integrantes con equipos.mostrar_jugadores()
    equipo_1.mostrar_jugadores()
    equipo_2.mostrar_jugadores()
    # mostrar los juegos ganados por cada equipo
    print(f"\n--- RESULTADO FINAL DEL JUEGO ---")
    print(
        "equipo 1: ",
        juego.equipo1.juegos_ganados,
        "juegos ganados",
        "rondas ganadas: ",
        juego.equipo1.rondas_ganadas,
    )
    print(
        "equipo 2: ",
        juego.equipo2.juegos_ganados,
        "juegos ganados",
        "rondas ganadas: ",
        juego.equipo2.rondas_ganadas,
    )
    print("")
    print("")

    return render_template(
        "resultados.html",
        resultado_final=resultado_final,
        simulacion_data=convert_numpy(ultimo_juego),
    )


@app.route("/resultados_acumulados.json")
def serve_json():
    return send_file("resultados_acumulados.json", mimetype="application/json")


@app.route("/graficas", methods=["GET"])
def graficas():
    return render_template("graficas.html")


if __name__ == "__main__":
    app.run(debug=True)
