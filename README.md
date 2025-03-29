# Simulación de Arquería

Este proyecto es una aplicación web desarrollada en Flask que simula competencias de arquería entre equipos. La simulación incluye la generación de jugadores con diferentes habilidades, equipos, y la visualización de resultados mediante gráficos y tablas.

## Características

- Simulación de competencias de arquería entre dos equipos
- Generación aleatoria de jugadores con diferentes géneros y habilidades
- Sistema de puntuación basado en la precisión de los tiros
- Visualización de resultados mediante tablas y gráficos
- Historiales de juegos y rondas
- Interfaz web interactiva para visualizar los resultados

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

```
arqueria-simulacion/
├── modelos/                  # Generadores de números pseudoaleatorios
│   ├── __init__.py
│   ├── config.py
│   ├── distribution.py
│   ├── linear_congruence.py
│   ├── main.py
│   ├── mean_squares.py
│   ├── multiplicative_congruence.py
│   ├── normal_distribution.py
│   ├── prng.py
│   └── uniform_distribution.py
├── simulacion/               # Lógica de la simulación de arquería
│   ├── __init__.py
│   ├── blanco_objetivo.py
│   ├── equipo.py
│   ├── juego.py
│   ├── jugador.py
│   └── ronda.py
├── static/                   # Archivos estáticos CSS
│   ├── index.css
│   └── random_numbers.css
├── templates/                # Plantillas HTML
│   ├── index.html
│   └── resultados.html
├── utils/                    # Utilidades para estadísticas y gráficas
│   ├── estadisticas.py
│   └── graficas.py
├── index.py                  # Punto de entrada de la aplicación
├── simulacion.py             # Script principal de simulación
└── resultados_acumulados.json # Datos de resultados guardados
```
```

## Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd arqueria-simulacion
```

### 2. Crear y activar un entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate     # En Windows
```

### 3. Instalar dependencias 

```bash
pip install flask matplotlib numpy names
```

### 4. Ejecutar la aplicación

```bash
python index.py
```

La aplicación estará disponible en http://127.0.0.1:5000/

## Cómo funciona

- Al iniciar el juego, se crean dos equipos con 5 jugadores cada uno
- Se simulan 50 juegos consecutivos, cada uno con 10 rondas
- Los jugadores realizan tiros al blanco, obteniendo puntos según su precisión
- El sistema registra estadísticas como rondas ganadas, puntajes y el jugador con más suerte
- Al finalizar, se muestran los resultados en tablas y gráficos