from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    session,
    send_file,
    jsonify,
    request,
)
from utils.graficas import generar_grafica_puntos_jugadores_response
from simulacion.juego import Juego
from simulacion.equipo import Equipo
from numpy import int64  # Solo importamos el tipo específico que necesitamos
import json
import threading
import time

app = Flask(__name__)
app.secret_key = "tu_clave_secreta"

# Variables globales
equipo_1 = Equipo("Los tiguere", 5)
equipo_2 = Equipo("Los jaguares", 5)
todos_resultados = []  # Variable global para almacenar todos los resultados

JSON_FILE = "simulacion_data.json"

# Variables para el progreso de la simulación
simulacion_en_progreso = False
progreso_actual = 0
total_juegos_simulacion = 20000
juegos_completados = 0


def convert_numpy(obj):
    """
    Convierte objetos de NumPy a tipos nativos de Python para permitir la serialización JSON.

    Esta función es crucial porque los objetos NumPy (como np.int64) no son directamente
    serializables a JSON. La función recorre recursivamente diccionarios y listas para
    convertir todos los tipos NumPy encontrados.

    Args:
        obj: El objeto a convertir (puede ser dict, list, np.int64 u otro tipo)

    Returns:
        El objeto convertido a tipos nativos de Python
    """
    if isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(x) for x in obj]
    elif isinstance(obj, int64):
        return int(obj)
    else:
        return obj


def cargar_resultados():
    """
    Carga los resultados previos de simulaciones desde un archivo JSON al iniciar la aplicación.

    Esta función permite la persistencia de datos entre ejecuciones de la aplicación,
    facilitando el análisis de simulaciones anteriores. Si el archivo no existe o está
    corrupto, inicializa una lista vacía para almacenar nuevos resultados.

    Utiliza la variable global todos_resultados como almacenamiento principal de los datos
    de simulación en memoria durante la ejecución de la aplicación.
    """
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
    """
    Busca un juego específico por su identificador único en los resultados almacenados.

    Esta función es esencial para la funcionalidad de consulta de juegos individuales,
    permitiendo al usuario revisar detalles de simulaciones específicas sin tener que
    procesar todos los resultados.

    Args:
        juego_id: El identificador único del juego a buscar

    Returns:
        dict: Los datos del juego si se encuentra, None en caso contrario
    """
    global todos_resultados
    for juego in todos_resultados:
        if str(juego["id_juego"]) == str(juego_id):
            return juego
    return None


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/iniciar_simulacion", methods=["POST"])
def iniciar_simulacion():
    global simulacion_en_progreso, progreso_actual, juegos_completados, total_juegos_simulacion

    if simulacion_en_progreso:
        return jsonify({"error": "Ya hay una simulación en progreso"}), 400

    # Resetear variables de progreso
    progreso_actual = 0
    juegos_completados = 0

    # Iniciar la simulación en un hilo separado
    thread = threading.Thread(target=ejecutar_simulacion)
    thread.daemon = True
    thread.start()

    return jsonify({"status": "Simulación iniciada correctamente"})


@app.route('/progreso_simulacion', methods=['GET'])
def progreso_simulacion():
    global progreso_actual, juegos_completados, total_juegos_simulacion
    
    return jsonify({
        "progreso": progreso_actual,
        "juegos_completados": juegos_completados,
        "total_juegos": total_juegos_simulacion
    })

def ejecutar_simulacion():
    """
    Función que ejecuta la simulación en segundo plano, actualizando el progreso.
    """
    global simulacion_en_progreso, progreso_actual, juegos_completados
    global equipo_1, equipo_2, todos_resultados, total_juegos_simulacion
    
    try:
        simulacion_en_progreso = True
        tiempo_inicio = time.time()
        print("Iniciando simulación en segundo plano...")
        
        # Reiniciar la lista de resultados
        todos_resultados = []
        
        for i in range(total_juegos_simulacion):
            if i % 1000 == 0:
                print(f"Progreso: {i}/{total_juegos_simulacion} juegos ({i/total_juegos_simulacion*100:.1f}%)")
            
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
                "genero_con_mas_victorias": juego.genero_con_mas_victorias,
                "generos_victorias_totales": {
                    "M": juego.victorias_por_genero["M"],
                    "F": juego.victorias_por_genero["F"],
                },
                "generos_victorias_globales": {
                    "M": Juego.generos_victorias_totales["M"],
                    "F": Juego.generos_victorias_totales["F"],
                },
                "equipo_ganador": (
                    {
                        "nombre": juego.equipo_ganador_juego.nombre,
                        "puntaje": juego.puntaje_ganador,
                    }
                    if juego.equipo_ganador_juego is not None
                    else {"nombre": "Empate", "puntaje": 0}
                ),
                "numero_juego": juego.juego_actual,
                "equipo_1": {
                    "nombre": juego.equipo1.nombre,
                    "rondas_ganadas": juego.equipo1.rondas_ganadas,
                    "puntaje_total": juego.puntaje_equipo1_final,
                },
                "equipo_2": {
                    "nombre": juego.equipo2.nombre,
                    "rondas_ganadas": juego.equipo2.rondas_ganadas,
                    "puntaje_total": juego.puntaje_equipo2_final,
                },
            }
            
            todos_resultados.append(convert_numpy(resultado_juego))
            
            # Actualizar el progreso
            juegos_completados = i + 1
            progreso_actual = int((i + 1) / total_juegos_simulacion * 100)
        
        # Escribir resultados al archivo
        with open("resultados_acumulados.json", "w") as f:
            json.dump(todos_resultados, f)
        
        tiempo_total = time.time() - tiempo_inicio
        print(f"Simulación completada en {tiempo_total:.2f} segundos")
        
    except Exception as e:
        print(f"Error en la simulación: {str(e)}")
    finally:
        simulacion_en_progreso = False

@app.route("/jugar", methods=["POST"])
def jugar():
    """
    Redirige a la página de resultados para un juego específico identificado por su ID.

    Esta función es un punto de entrada para la consulta de simulaciones específicas,
    simplificando la navegación y búsqueda de resultados históricos. Recibe el ID
    como parámetro GET y redirige a la función resultados con ese parámetro.

    Args (via request.args):
        id: El identificador único del juego a buscar

    Returns:
        Redirección a la página de resultados con el ID del juego especificado
    """
    tiempo_inicio = time.time()
    print("Iniciando simulación...")

    total_juegos = 20000
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
            "genero_con_mas_victorias": juego.genero_con_mas_victorias,
            "generos_victorias_totales": {
                "M": juego.victorias_por_genero["M"],
                "F": juego.victorias_por_genero["F"],
            },
            "generos_victorias_globales": {
                "M": Juego.generos_victorias_totales["M"],
                "F": Juego.generos_victorias_totales["F"],
            },
            "equipo_ganador": (
                {
                    "nombre": juego.equipo_ganador_juego.nombre,
                    "puntaje": juego.puntaje_ganador,
                }
                if juego.equipo_ganador_juego is not None
                else {"nombre": "Empate", "puntaje": 0}
            ),
            "numero_juego": juego.juego_actual,
            "equipo_1": {
                "nombre": juego.equipo1.nombre,
                "rondas_ganadas": juego.equipo1.rondas_ganadas,
                "puntaje_total": juego.puntaje_equipo1_final,
            },
            "equipo_2": {
                "nombre": juego.equipo2.nombre,
                "rondas_ganadas": juego.equipo2.rondas_ganadas,
                "puntaje_total": juego.puntaje_equipo2_final,
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
    """
    Procesa y muestra los resultados de la simulación de arquería.

    Esta función tiene múltiples responsabilidades:
    1. Obtener el ID del juego de la sesión o de los parámetros de la URL
    2. Cargar resultados previos si no están en memoria
    3. Buscar el juego específico solicitado o usar el último juego simulado
    4. Preparar los datos de la simulación para presentarlos en la interfaz, incluyendo:
       - Información de equipos (nombre, rondas ganadas, puntaje)
       - Detalles de jugadores (nombre, género)
       - Estadísticas especiales (jugador con más suerte, con más experiencia)
       - Equipo ganador y su puntaje
       - Estadísticas globales de victorias por género
    5. Manejar errores y proporcionar datos predeterminados si no hay resultados

    La función es altamente dinámica, permitiendo consultar diferentes simulaciones
    históricas o mostrar los resultados más recientes por defecto.

    Returns:
        Renderización de la plantilla resultados.html con los datos procesados
    """
    game_id = session.get("game_id", None)
    global equipo_1, equipo_2, todos_resultados

    # Verificar si se solicita un juego específico
    juego_id_solicitado = request.args.get("juego_id", None)

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
                    ],
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
                    ],
                },
                "historial_puntajes": [],  # No tenemos historial de rondas detallado
                "jugador_con_mas_suerte": ultimo_juego["jugador_con_mas_suerte"],
                "jugador_con_mas_experiencia": ultimo_juego[
                    "jugador_con_mas_experiencia"
                ],
                "equipo_ganador": ultimo_juego["equipo_ganador"],
                "total_juegos": len(todos_resultados),
                "numero_juego": ultimo_juego["numero_juego"],
                "generos_victorias_totales": ultimo_juego["generos_victorias_totales"],
                "generos_victorias_globales": {
                    "M": Juego.generos_victorias_totales["M"],
                    "F": Juego.generos_victorias_totales["F"],
                },
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
    """
    Redirige a la página de resultados para un juego específico identificado por su ID.

    Esta función es un punto de entrada para la consulta de simulaciones específicas,
    simplificando la navegación y búsqueda de resultados históricos. Recibe el ID
    como parámetro GET y redirige a la función resultados con ese parámetro.

    Args (via request.args):
        id: El identificador único del juego a buscar

    Returns:
        Redirección a la página de resultados con el ID del juego especificado
    """
    juego_id = request.args.get("id", "")
    return redirect(url_for("resultados", juego_id=juego_id))


@app.route("/resultados_acumulados.json")
def serve_json():
    """
    Endpoint para servir el archivo JSON de resultados acumulados.
    Permite la descarga del archivo JSON que contiene todos los resultados
    de juegos simulados.
    Returns:
        Respuesta con el archivo JSON como contenido
    """
    return send_file("resultados_acumulados.json", mimetype="application/json")


@app.route("/graficas", methods=["GET"])
def graficas():
    """
    Renderiza la página de gráficas con la imagen generada de los puntos de jugadores.
    Esta función es responsable de generar y mostrar gráficas relacionadas con
    los resultados de los juegos simulados. Utiliza la función
    generar_grafica_puntos_jugadores_response para crear la imagen de la gráfica
    y la pasa a la plantilla HTML para su visualización.
    Returns:
        Renderización de la plantilla graficas.html con la imagen de la gráfica
    """
    grafica_img = generar_grafica_puntos_jugadores_response()
    return render_template("graficas.html", grafica_img=grafica_img)


@app.route("/todos_juegos", methods=["GET"])
def todos_juegos():
    """
    Endpoint para obtener todos los resultados de juegos simulados.
    Devuelve una lista de diccionarios con información sobre cada juego,
    incluyendo jugadores, puntajes y estadísticas.
    """
    global todos_resultados
    return jsonify(todos_resultados)


@app.route("/todos_juegos/<int:id>", methods=["GET"])
def juego_por_id(id):
    """
    Endpoint API que retorna los datos de un juego específico por su número.

    Esta función permite consultar mediante API los detalles completos de una
    simulación específica. A diferencia de buscar_juego_por_id, esta función:
    1. Busca por número de juego, no por ID único
    2. Está diseñada como endpoint API, retornando JSON en lugar de HTML
    3. Maneja el caso de juego no encontrado con un código HTTP apropiado

    Args:
        id: El número de juego a buscar (parámetro de ruta)

    Returns:
        Respuesta JSON con los datos del juego o un mensaje de error con código 404
    """
    global todos_resultados
    juego = next((j for j in todos_resultados if j["numero_juego"] == id), None)
    if juego:
        return jsonify(juego)
    else:
        return jsonify({"error": "Juego no encontrado"}), 404


if __name__ == "__main__":
    app.run(debug=True)
