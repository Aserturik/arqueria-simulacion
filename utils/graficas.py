import matplotlib.pyplot as plt
import matplotlib
import io
import base64
import numpy as np
import json
from modelos.random_wrapper import uniform  # Añadir uniform a los imports
matplotlib.use('Agg')  # Configuración para entornos sin GUI

def generar_grafica_puntos_jugadores():
    """
    Genera un gráfico de dispersión que muestra los puntos obtenidos por 
    cada jugador en cada juego simulado.
    
    Returns:
        str: Imagen en formato base64 codificada como string
    """
    try:
        # Cargar datos de juegos
        with open("resultados_acumulados.json", "r") as f:
            todos_resultados = json.load(f)
        
        if not todos_resultados:
            return None
        
        # Crear figura
        plt.figure(figsize=(12, 8))
        
        # Nombres de jugadores (5 de cada equipo)
        nombres_eq1 = ["Jugador 1-1", "Jugador 1-2", "Jugador 1-3", "Jugador 1-4", "Jugador 1-5"]
        nombres_eq2 = ["Jugador 2-1", "Jugador 2-2", "Jugador 2-3", "Jugador 2-4", "Jugador 2-5"]
        
        # Colores para cada jugador
        colores_eq1 = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        colores_eq2 = ['#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        
        # Diccionarios para almacenar los datos por jugador
        datos_jugadores = {}
        for nombre in nombres_eq1 + nombres_eq2:
            datos_jugadores[nombre] = {"juegos": [], "puntos": []}
        
        # Extraer datos de cada juego
        for juego in todos_resultados:
            num_juego = juego["numero_juego"]
            
            # Asignamos puntos del equipo 1 entre sus jugadores
            puntaje_total_eq1 = juego["equipo_1"]["puntaje_total"]
            # Distribuimos los puntos con cierta variabilidad
            puntos_jugadores_eq1 = distribuir_puntos(puntaje_total_eq1, 5)
            
            # Asignamos puntos del equipo 2 entre sus jugadores
            puntaje_total_eq2 = juego["equipo_2"]["puntaje_total"]
            puntos_jugadores_eq2 = distribuir_puntos(puntaje_total_eq2, 5)
            
            # Guardar datos para cada jugador
            for i, nombre in enumerate(nombres_eq1):
                datos_jugadores[nombre]["juegos"].append(num_juego)
                datos_jugadores[nombre]["puntos"].append(puntos_jugadores_eq1[i])
                
            for i, nombre in enumerate(nombres_eq2):
                datos_jugadores[nombre]["juegos"].append(num_juego)
                datos_jugadores[nombre]["puntos"].append(puntos_jugadores_eq2[i])
        
        # Graficar datos de cada jugador
        for i, nombre in enumerate(nombres_eq1):
            plt.scatter(
                datos_jugadores[nombre]["juegos"], 
                datos_jugadores[nombre]["puntos"],
                color=colores_eq1[i], 
                alpha=0.7,
                label=f"{nombre} (Equipo 1)"
            )
            
        for i, nombre in enumerate(nombres_eq2):
            plt.scatter(
                datos_jugadores[nombre]["juegos"], 
                datos_jugadores[nombre]["puntos"],
                color=colores_eq2[i], 
                alpha=0.7,
                label=f"{nombre} (Equipo 2)"
            )
            
        # Configuración del gráfico
        plt.title('Puntos obtenidos por jugador en cada juego', fontsize=16)
        plt.xlabel('Número de juego', fontsize=12)
        plt.ylabel('Puntos obtenidos', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=5, fontsize=10)
        plt.tight_layout()
        
        # Guardar gráfico en memoria
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        
        # Codificar en base64
        encoded_img = base64.b64encode(img.getvalue()).decode('utf-8')
        plt.close()
        
        return encoded_img
    
    except Exception as e:
        print(f"Error al generar gráfica: {str(e)}")
        return None

def distribuir_puntos(total, num_jugadores):
    """
    Distribuye los puntos entre jugadores con cierta variabilidad.
    """
    if total == 0:
        return [0] * num_jugadores
    
    # Base mínima para cada jugador (20% distribuido equitativamente)
    base = (total * 0.2) / num_jugadores
    
    # Resto a distribuir con variabilidad (80%)
    resto = total * 0.8
    
    # Generar factores de distribución aleatorios
    factores = [uniform(0.7, 1.3) for _ in range(num_jugadores)]
    suma_factores = sum(factores)
    
    # Normalizar factores y distribuir resto
    puntos = [base + (factor / suma_factores) * resto for factor in factores]
    
    # Asegurar que la suma sea exactamente igual al total
    ajuste = total - sum(puntos)
    puntos[0] += ajuste
    
    return [round(p) for p in puntos]

def generar_grafica_puntos_jugadores_response():
    """
    Genera una respuesta HTTP con la imagen de la gráfica.
    
    Returns:
        Response: Objeto de respuesta Flask con la imagen
    """
    encoded_img = generar_grafica_puntos_jugadores()
    
    if encoded_img:
        return encoded_img
    else:
        return None