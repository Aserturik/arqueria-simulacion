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
    equipo_1 = Equipo("Arqueros del norte", "M", 5)
    equipo_2 = Equipo("Arqueras del sur", "F", 5)

    # Para resultados acumulados, creamos o limpiamos el archivo al inicio
    with open("resultados_acumulados.json", "w") as f:
        f.write("[\n")  # Iniciamos el array JSON

    total_juegos = 200
    # Guarda solo el último juego para mostrar en la interfaz
    ultimo_juego = None

    for i in range(total_juegos):
        # Crear y jugar el juego
        juego = Juego(equipo_1, equipo_2, num_rondas=10, juego_actual=i + 1)
        juego.jugar_partida_completa()
        print(f"\n--- JUEGO {i + 1} ---")

        # Guardar los resultados básicos (sin incluir todo el historial de rondas)
        resultado_basico = {
            "id_juego": juego.id_juego,
            "numero_juego": juego.juego_actual,
            "equipo_1": {
                "nombre": juego.equipo1.nombre,
                "rondas_ganadas": juego.equipo1.rondas_ganadas,
                "puntaje_total": juego.equipo1.puntaje_total,
            },
            "equipo_2": {
                "nombre": juego.equipo2.nombre,
                "rondas_ganadas": juego.equipo2.rondas_ganadas,
                "puntaje_total": juego.equipo2.puntaje_total,
            },
        }

        # Guardar solo el último juego completo para la interfaz
        if i == total_juegos - 1:
            ultimo_juego = {
                "equipo1": {
                    "nombre": juego.equipo1.nombre,
                    "rondas_ganadas": juego.equipo1.rondas_ganadas,
                    "puntaje_total": juego.equipo1.puntaje_total,
                },
                "equipo2": {
                    "nombre": juego.equipo2.nombre,
                    "rondas_ganadas": juego.equipo2.rondas_ganadas,
                    "puntaje_total": juego.equipo2.puntaje_total,
                },
                "id_juego": juego.id_juego,
                "historial_rondas": juego.historial_rondas,
            }

        # Escribir cada resultado individual al archivo con coma solo si no es el último
        with open("resultados_acumulados.json", "a") as f:
            f.write(json.dumps(convert_numpy(resultado_basico), indent=2))
            if i < total_juegos - 1:
                f.write(",\n")
            else:
                f.write("\n]")  # Cerramos el array JSON al final

    session["game_id"] = juego.id_juego

    resultado_final = (
        f"{juego.equipo1.nombre}: {juego.equipo1.rondas_ganadas} rondas vs "
        f"{juego.equipo2.nombre}: {juego.equipo2.rondas_ganadas} rondas."
    )

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
    game_id = request.args.get("game_id")
    simus = session.get("simulaciones", {})
    if not game_id or game_id not in simus:
        return redirect(url_for("index"))
    sim_data = simus[game_id]
    imagenes = generar_imagenes(sim_data)
    return render_template("graficas.html", imagen=imagenes, id_juego=game_id)


def generar_imagenes(sim_data):
    import io
    import base64
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle

    # 1. Evolución de puntajes por ronda (line plot)
    rondas = [r["ronda"] for r in sim_data["historial_puntajes"]]
    puntajes1 = [r["equipo1"]["puntaje"] for r in sim_data["historial_puntajes"]]
    puntajes2 = [r["equipo2"]["puntaje"] for r in sim_data["historial_puntajes"]]

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(rondas, puntajes1, "o-", label=sim_data["equipo1"]["nombre"])
    ax1.plot(rondas, puntajes2, "o-", label=sim_data["equipo2"]["nombre"])
    ax1.set_xlabel("Ronda")
    ax1.set_ylabel("Puntos")
    ax1.set_title("Evolución de puntajes por ronda")
    ax1.legend()
    ax1.grid(True)

    buf1 = io.BytesIO()
    fig1.savefig(buf1, format="png")
    buf1.seek(0)
    imagen_evolucion = base64.b64encode(buf1.read()).decode("utf-8")
    plt.close(fig1)

    # 2. Puntaje Total Final (bar chart)
    final_puntaje1 = sim_data["equipo1"]["puntaje_total"]
    final_puntaje2 = sim_data["equipo2"]["puntaje_total"]

    fig2, ax2 = plt.subplots(figsize=(6, 6))
    equipos = [sim_data["equipo1"]["nombre"], sim_data["equipo2"]["nombre"]]
    final_puntajes = [final_puntaje1, final_puntaje2]
    ax2.bar(equipos, final_puntajes, color=["blue", "orange"])
    ax2.set_xlabel("Equipo")
    ax2.set_ylabel("Puntaje Total")
    ax2.set_title("Puntaje Total Final")
    ax2.grid(axis="y")

    buf2 = io.BytesIO()
    fig2.savefig(buf2, format="png")
    buf2.seek(0)
    imagen_final = base64.b64encode(buf2.read()).decode("utf-8")
    plt.close(fig2)

    # 3. Visualización del Blanco con disparos
    fig3, ax3 = plt.subplots(figsize=(8, 8))
    ax3.add_patch(
        Circle(
            (0, 0),
            sim_data["blanco"]["RADIO_EXTERIOR"],
            fill=False,
            color="black",
            lw=2,
        )
    )
    ax3.add_patch(
        Circle(
            (0, 0),
            sim_data["blanco"]["RADIO_INTERMEDIA"],
            fill=False,
            color="black",
            lw=2,
        )
    )
    ax3.add_patch(
        Circle(
            (0, 0), sim_data["blanco"]["RADIO_CENTRAL"], fill=False, color="black", lw=2
        )
    )
    lim = sim_data["blanco"]["RADIO_EXTERIOR"] * 1.5
    ax3.set_xlim(-lim, lim)
    ax3.set_ylim(-lim, lim)
    ax3.set_aspect("equal")
    ax3.grid(True)
    for tiro in sim_data["blanco"]["tiros"]:
        x, y = tiro["coordenadas"]
        color = "blue" if tiro["genero"] == "M" else "red"
        ax3.plot(x, y, "o", color=color, markersize=5)
    ax3.set_title("Disparos en el Blanco")

    buf3 = io.BytesIO()
    fig3.savefig(buf3, format="png")
    buf3.seek(0)
    imagen_blanco = base64.b64encode(buf3.read()).decode("utf-8")
    plt.close(fig3)

    return {
        "evolucion": imagen_evolucion,
        "final": imagen_final,
        "blanco": imagen_blanco,
    }


if __name__ == "__main__":
    app.run(debug=True)
