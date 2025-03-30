from flask import Flask, render_template, redirect, url_for, session, send_file, jsonify, request
from simulacion.juego import Juego
from simulacion.equipo import Equipo
import numpy as np
import json
import time

app = Flask(__name__)
app.secret_key = "tu_clave_secreta"

# Variables globales
equipo_1 = Equipo("Los tiguere", 5)
equipo_2 = Equipo("Los jaguares", 5)
todos_resultados = []  # Variable global para almacenar todos los resultados

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


# Función para cargar resultados al iniciar la aplicación
def cargar_resultados():
    global todos_resultados
    try:
        with open("resultados_acumulados.json", "r") as f:
            todos_resultados = json.load(f)
        print(f"Cargados {len(todos_resultados)} juegos de resultados")
    except (FileNotFoundError, json.JSONDecodeError):
        todos_resultados = []
        print("No se encontraron resultados previos o el archivo está corrupto")


# Cargar resultados al iniciar
cargar_resultados()


# Función para buscar un juego por ID
def buscar_juego_por_id(juego_id):
    global todos_resultados
    for juego in todos_resultados:
        if str(juego["id_juego"]) == str(juego_id):
            return juego
    return None


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/jugar", methods=["POST"])
def jugar():
    tiempo_inicio = time.time()
    print("Iniciando simulación...")

    total_juegos = 200
    global equipo_1, equipo_2, todos_resultados
    
    # Reiniciar la lista de resultados
    todos_resultados = []
    ultimo_juego = None

    for i in range(total_juegos):
        if i % 1000 == 0:
            print(f"Progreso: {i}/{total_juegos} juegos ({i/total_juegos*100:.1f}%)")

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
                    "puntaje": juego.equipo_ganador_juego.puntaje_juego
                    if hasattr(juego.equipo_ganador_juego, "puntaje_juego") and juego.equipo_ganador_juego is not None
                    else (juego.equipo_ganador_juego.puntaje_total if hasattr(juego.equipo_ganador_juego, "puntaje_total") else 0),
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
    print(f"Simulación completada en {tiempo_total:.2f} segundos")

    session["game_id"] = juego.id_juego

    # Importante: devolver una respuesta válida
    return redirect(url_for("resultados"))


@app.route("/resultados", methods=["GET"])
def resultados():
    # Obtener el ID del juego de la sesión
    game_id = session.get("game_id", None)
    global equipo_1, equipo_2, todos_resultados

    # Verificar si se solicita un juego específico
    juego_id_solicitado = request.args.get('juego_id', None)
    
    try:
        # Si no hay resultados en memoria, cargarlos del archivo
        if not todos_resultados:
            cargar_resultados()

        # Determinar qué juego mostrar
        if juego_id_solicitado:
            juego_especifico = buscar_juego_por_id(juego_id_solicitado)
            if juego_especifico:
                ultimo_juego = juego_especifico
            else:
                # Si no se encuentra, usar el último
                ultimo_juego = todos_resultados[-1] if todos_resultados else None
        else:
            # Si no se solicita un juego específico, usar el último
            ultimo_juego = todos_resultados[-1] if todos_resultados else None
            
        # Procesar el juego seleccionado
        if ultimo_juego:
            # Crear datos para pasar a la plantilla
            simulacion_data = {
                "id_juego": ultimo_juego["id_juego"],
                "equipo1": {
                    "nombre": ultimo_juego["equipo_1"]["nombre"],
                    "rondas_ganadas": ultimo_juego["equipo_1"]["rondas_ganadas"],
                    "puntaje_total": ultimo_juego["equipo_1"]["puntaje_total"],
                    "jugadores": [
                        {
                            "nombre": jugador.nombre,
                            "genero": jugador.genero,
                        }
                        for jugador in equipo_1.jugadores
                    ]
                },
                "equipo2": {
                    "nombre": ultimo_juego["equipo_2"]["nombre"],
                    "rondas_ganadas": ultimo_juego["equipo_2"]["rondas_ganadas"],
                    "puntaje_total": ultimo_juego["equipo_2"]["puntaje_total"],
                    "jugadores": [
                        {
                            "nombre": jugador.nombre,
                            "genero": jugador.genero,
                        }
                        for jugador in equipo_2.jugadores
                    ]
                },
                "historial_puntajes": [],  # No tenemos historial de rondas detallado
                "jugador_con_mas_suerte": ultimo_juego["jugador_con_mas_suerte"],
                "jugador_con_mas_experiencia": ultimo_juego[
                    "jugador_con_mas_experiencia"
                ],
                "equipo_ganador": ultimo_juego["equipo_ganador"],
                "total_juegos": len(todos_resultados),
                "numero_juego": ultimo_juego["numero_juego"],
            }

            resultado_final = f"Simulación completada con éxito: {len(todos_resultados)} juegos simulados"

        else:
            # Datos predeterminados si no hay resultados
            simulacion_data = {
                "id_juego": game_id,
                "equipo1": {
                    "nombre": "Los tiguere",
                    "rondas_ganadas": 0,
                    "puntaje_total": 0,
                },
                "equipo2": {
                    "nombre": "Los jaguares",
                    "rondas_ganadas": 0,
                    "puntaje_total": 0,
                },
                "historial_puntajes": [],
                "total_juegos": 0,
            }
            resultado_final = "No hay resultados disponibles"

    except Exception as e:
        # Manejar error general
        print(f"Error en resultados: {str(e)}")
        simulacion_data = {
            "id_juego": game_id,
            "equipo1": {
                "nombre": "Los tiguere",
                "rondas_ganadas": 0,
                "puntaje_total": 0,
            },
            "equipo2": {
                "nombre": "Los jaguares",
                "rondas_ganadas": 0,
                "puntaje_total": 0,
            },
            "historial_puntajes": [],
            "total_juegos": 0,
        }
        resultado_final = f"Error al cargar resultados: {str(e)}"

    return render_template(
        "resultados.html",
        simulacion_data=simulacion_data,
        resultado_final=resultado_final,
    )


# Nueva ruta para buscar un juego específico por ID
@app.route("/buscar_juego", methods=["GET"])
def buscar_juego():
    juego_id = request.args.get('id', '')
    return redirect(url_for('resultados', juego_id=juego_id))


@app.route("/resultados_acumulados.json")
def serve_json():
    return send_file("resultados_acumulados.json", mimetype="application/json")


@app.route("/graficas", methods=["GET"])
def graficas():
    return render_template("graficas.html")


if __name__ == "__main__":
    app.run(debug=True)