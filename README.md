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
├── modelos/                  # Módulos de generación de números aleatorios
│   ├── __init__.py
│   ├── linear_congruence.py  # Implementación del generador congruencial lineal
│   ├── prng.py              # Clase base abstracta para generadores
│   ├── random_wrapper.py     # Wrapper compatible con el módulo random de Python
│   └── pruebas/             # Pruebas estadísticas para validar los generadores
│       ├── __init__.py
│       ├── average_test.py
│       ├── chi_square_test.py
│       ├── ks_test.py       # Prueba de Kolmogorov-Smirnov
│       ├── poker_test.py    # Prueba de independencia
│       └── variance_test.py
├── simulacion/              # Lógica de la simulación de arquería
│   ├── __init__.py
│   ├── blanco_objetivo.py   # Modelado del blanco y puntuación
│   ├── equipo.py           # Gestión de equipos
│   ├── juego.py            # Control del flujo del juego
│   ├── jugador.py          # Modelado de jugadores y habilidades
│   └── ronda.py            # Gestión de rondas de tiro
├── static/                 # Archivos estáticos
│   ├── styles.css
│   └── js/
│       └── scripts.js
├── templates/              # Plantillas HTML
│   ├── graficas.html
│   ├── index.html
│   ├── resultados.html
│   └── partials/          # Componentes HTML reutilizables
│       ├── _resumen_actual.html
│       └── _todos_juegos.html
├── utils/                 # Utilidades
│   └── graficas.py       # Generación de gráficas y visualizaciones
├── tests/                # Pruebas unitarias
│   └── test_linear_congruence.py
├── index.py             # Punto de entrada de la aplicación web
└── resultados_acumulados.json  # Almacenamiento de resultados

```

## Sistema de Generación de Números Pseudoaleatorios

El proyecto implementa su propio sistema de generación de números pseudoaleatorios para garantizar la calidad y reproducibilidad de las simulaciones. El sistema incluye:

### Generador Congruencial Lineal

- Implementa el método congruencial lineal: X\_(n+1) = (a \* X_n + c) mod m
- Utiliza parámetros optimizados:
  - m = 2^31 - 1 (Número primo de Mersenne)
  - a = 1597 (multiplicador)
  - c = 51749 (incremento)
- Garantiza un período máximo y buenas propiedades estadísticas

### Validación Estadística

El generador ha sido validado mediante diversas pruebas estadísticas:

- Prueba Chi-cuadrado para uniformidad
- Prueba de Kolmogorov-Smirnov
- Prueba de varianza
- Prueba de póker para independencia
- Test de promedios
- Reproducibilidad con semillas

### Integración con la Simulación

- Wrapper compatible con la interfaz del módulo `random` de Python
- Generación de valores con distribuciones específicas (normal, uniforme)
- Métodos para selección aleatoria, mezcla y muestreo

## Instalación y Ejecución

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### 1. Clonar el repositorio

```bash
git clone https://github.com/Aserturik/arqueria-simulacion
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
pip install flask matplotlib numpy names scipy
```

### 4. Ejecutar la aplicación

```bash
python index.py
```

La aplicación estará disponible en http://localhost:5000/

## Funcionamiento de la Simulación

1. Inicialización:

   - Se crean dos equipos con 5 jugadores cada uno
   - Cada jugador recibe atributos aleatorios de resistencia y suerte

2. Desarrollo del Juego:

   - Se simulan 20000 juegos consecutivos
   - Cada juego consta de 10 rondas
   - Los tiros se generan usando el generador pseudoaleatorio validado
   - La precisión del tiro depende de las habilidades del jugador

3. Puntuación:

   - Los puntos se asignan según la distancia al centro del blanco
   - Se consideran factores como la suerte y la fatiga del jugador

4. Resultados:
   - Se registran estadísticas detalladas de cada juego
   - Los resultados se visualizan mediante gráficas y tablas
   - Se mantiene un historial completo de todas las simulaciones
