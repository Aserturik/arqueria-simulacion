from flask import Flask, render_template, redirect, url_for, session, request
from simulacion.juego import Juego
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
    juego = Juego(
        "Arqueros del Norte", "Arqueras del Sur", num_jugadores=5, num_rondas=10
    )

    # Al iniciar la simulación se crea o resetea el JSON
    inicial_data = {
        "equipo1": {
            "nombre": juego.equipo1.nombre,
            "rondas_ganadas": juego.equipo1.rondas_ganadas,  # normalmente 0
            "puntaje_total": juego.equipo1.puntaje_total,  # valor inicial
        },
        "equipo2": {
            "nombre": juego.equipo2.nombre,
            "rondas_ganadas": juego.equipo2.rondas_ganadas,
            "puntaje_total": juego.equipo2.puntaje_total,
        },
        "simulacion": {},  # Aquí se guardará el juego actual
    }
    with open(JSON_FILE, "w") as f:
        json.dump(inicial_data, f)

    # Se ejecuta la simulación (en este ejemplo se asume que el método juega la partida completa y actualiza los datos)
    juego.jugar_partida_completa()

    # Preparar los datos de la simulación
    simulacion_data = {
        "id_juego": juego.id_juego,
        "historial_puntajes": juego.historial_puntajes,
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
        "blanco": {
            "tiros": juego.blanco.tiros,
            "RADIO_CENTRAL": juego.blanco.RADIO_CENTRAL,
            "RADIO_INTERMEDIA": juego.blanco.RADIO_INTERMEDIA,
            "RADIO_EXTERIOR": juego.blanco.RADIO_EXTERIOR,
        },
    }
    simulacion_data = convert_numpy(simulacion_data)

    # Se actualiza el JSON con los datos del juego actual (sobreescribiendo lo previo)
    with open(JSON_FILE, "r") as f:
        data = json.load(f)
    data["simulacion"] = simulacion_data
    with open(JSON_FILE, "w") as f:
        json.dump(data, f)

    session["game_id"] = (
        juego.id_juego
    )  # Opcional, para usar en otra ruta si se requiere

    resultado_final = (
        f"{juego.equipo1.nombre}: {juego.equipo1.rondas_ganadas} rondas vs "
        f"{juego.equipo2.nombre}: {juego.equipo2.rondas_ganadas} rondas."
    )
    return render_template(
        "resultados.html",
        resultado_final=resultado_final,
        simulacion_data=simulacion_data,
    )


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
