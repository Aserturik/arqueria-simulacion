import math
from dataclasses import asdict, dataclass
from typing import List, Dict
from modelos.random_wrapper import uniform, choices

@dataclass
class Lanzamiento:
    """
    Estructura de datos que representa un lanzamiento individual.
    
    Attributes:
        coordenadas (List[float]): Coordenadas [x, y] donde impactó el tiro
        zona (int): Identificador numérico de la zona impactada
        puntaje (int): Puntuación obtenida por el tiro
    """
    coordenadas: List[float]
    zona: int
    puntaje: int


@dataclass
class JugadorTiros:
    """
    Estructura de datos que agrupa los tiros de un jugador.
    
    Attributes:
        jugador_id (str): Identificador único del jugador
        nombre (str): Nombre del jugador
        genero (str): Género del jugador ('M' o 'F')
        lanzamientos (List[Lanzamiento]): Lista de todos los tiros realizados
    """
    jugador_id: str
    nombre: str
    genero: str
    lanzamientos: List[Lanzamiento]


class Blanco:
    """
    Representa el blanco de tiro con arco y maneja la lógica de puntuación.
    Implementa un sistema de zonas concéntricas con diferentes puntajes y 
    probabilidades basadas en el género y habilidades del tirador.
    
    Attributes:
        ZONAS (dict): Mapeo de zonas a puntajes
        RADIO_* (float): Radios de las diferentes zonas del blanco
        PROBABILIDADES (dict): Probabilidades base de acierto por género y zona
    """

    # Mapeo zona -> puntaje (nombre a valor numérico)
    ZONAS = {"CENTRAL": 10, "INTERMEDIA": 9, "EXTERIOR": 8, "ERROR": 0}

    # Parámetros de radios
    RADIO_CENTRAL = 1.0
    RADIO_INTERMEDIA = 3.0
    RADIO_EXTERIOR = 5.0
    RADIO_ERROR_MULTIPLIER = 1.5  # Multiplicador para tiros fuera del blanco

    # Coste de resistencia
    TIRO_RESISTENCIA_COST = 5

    # Probabilidades base
    PROBABILIDADES = {
        "M": {"CENTRAL": 0.20, "INTERMEDIA": 0.33, "EXTERIOR": 0.40, "ERROR": 0.07},
        "F": {"CENTRAL": 0.30, "INTERMEDIA": 0.38, "EXTERIOR": 0.27, "ERROR": 0.05},
    }

    def __init__(self):
        self.players: Dict[str, JugadorTiros] = {}  # JugadorID -> Datos

    def realizar_tiro(self, jugador) -> int:
        """
        Procesa un intento de tiro y calcula su resultado.

        Args:
            jugador (Jugador): El jugador que realiza el tiro

        Returns:
            int: Puntaje obtenido en el tiro

        Efectos:
            - Reduce la resistencia del jugador
            - Incrementa el contador de tiros
            - Registra el tiro en el historial del jugador
        """
        # Verificar resistencia
        # if jugador.resistencia_actual < self.TIRO_RESISTENCIA_COST:
        #    return self.ZONAS["ERROR"]

        # Actualizar estado del jugador
        jugador.resistencia_actual -= self.TIRO_RESISTENCIA_COST
        jugador.tiros_realizados += 1

        # Calcular probabilidades ajustadas
        probs = self._ajustar_probabilidades(jugador)
        zona, coordenadas = self._generar_tiro(probs)
        puntaje = self.ZONAS[zona]

        # Registrar el tiro
        if jugador.user_id not in self.players:
            self._registrar_nuevo_jugador(jugador)

        self.players[jugador.user_id].lanzamientos.append(
            Lanzamiento(coordenadas=coordenadas, zona=self.ZONAS[zona], puntaje=puntaje)
        )

        return puntaje

    def realizar_tiro_desempate(self, jugador):
        """
        Realiza un tiro especial para desempate sin afectar la resistencia.

        Args:
            jugador (Jugador): El jugador que realiza el tiro de desempate

        Returns:
            int: Puntaje obtenido en el tiro

        Efectos:
            - Reinicia la suerte del jugador
            - Registra el tiro en el historial
        """
        # igual que el realizar tiro pero sin restar resistencia
        jugador.reiniciar_suerte()

        probs = self._ajustar_probabilidades(jugador)
        zona, coordenadas = self._generar_tiro(probs)
        puntaje = self.ZONAS[zona]

        if jugador.user_id not in self.players:
            self._registrar_nuevo_jugador(jugador)

        self.players[jugador.user_id].lanzamientos.append(
            Lanzamiento(coordenadas=coordenadas, zona=self.ZONAS[zona], puntaje=puntaje)
        )

        return puntaje

    def _registrar_nuevo_jugador(self, jugador):
        """
        Crea un nuevo registro para un jugador en el sistema.

        Args:
            jugador (Jugador): El jugador a registrar

        Efectos:
            - Crea una nueva entrada en self.players para el jugador
            - Inicializa su lista de lanzamientos
        """
        self.players[jugador.user_id] = JugadorTiros(
            jugador_id=jugador.user_id,
            nombre=jugador.nombre,
            genero=jugador.genero,
            lanzamientos=[],
        )

    def _ajustar_probabilidades(self, jugador) -> Dict[str, float]:
        """
        Ajusta las probabilidades de acierto según las habilidades del jugador.

        Args:
            jugador (Jugador): El jugador cuyas probabilidades se ajustarán

        Returns:
            Dict[str, float]: Probabilidades ajustadas para cada zona

        Proceso:
            1. Copia las probabilidades base según el género
            2. Aumenta prob. de CENTRAL según la suerte
            3. Reduce prob. de ERROR según la experiencia
            4. Normaliza las probabilidades
        """
        probs = self.PROBABILIDADES[jugador.genero].copy()

        # Aumentar probabilidad de CENTRAL por suerte
        factor_suerte = jugador.suerte / 3.0  # Normalizar suerte (rango 0-9)
        probs["CENTRAL"] *= 1 + 0.1 * factor_suerte

        # Reducir probabilidad de ERROR por experiencia
        factor_experiencia = min(1.0, jugador.experiencia / 50.0)
        probs["ERROR"] *= 1 - 0.2 * factor_experiencia

        # Normalizar probabilidades
        total = sum(probs.values())
        return {zona: prob / total for zona, prob in probs.items()}

    def _generar_tiro(self, probs: Dict[str, float]) -> tuple:
        """
        Genera las coordenadas y zona de impacto de un tiro.

        Args:
            probs (Dict[str, float]): Probabilidades ajustadas para cada zona

        Returns:
            tuple: (zona, [x, y]) donde zona es el identificador de la zona impactada
                  y [x, y] son las coordenadas del impacto

        Proceso:
            1. Selecciona la zona de impacto según las probabilidades
            2. Calcula el radio según la zona
            3. Genera coordenadas polares aleatorias
            4. Convierte a coordenadas cartesianas
        """
        # Seleccionar zona
        zona = choices(
            population=list(probs.keys()), 
            weights=list(probs.values()), 
            k=1
        )[0]

        # Calcular radio según zona
        if zona == "ERROR":
            radio = uniform(
                self.RADIO_EXTERIOR, 
                self.RADIO_EXTERIOR * self.RADIO_ERROR_MULTIPLIER
            )
        elif zona == "EXTERIOR":
            radio = uniform(self.RADIO_INTERMEDIA, self.RADIO_EXTERIOR)
        elif zona == "INTERMEDIA":
            radio = uniform(self.RADIO_CENTRAL, self.RADIO_INTERMEDIA)
        else:  # CENTRAL
            radio = uniform(0, self.RADIO_CENTRAL)

        # Generar coordenadas polares
        angulo = uniform(0, 2 * math.pi)
        x = round(radio * math.cos(angulo), 2)
        y = round(radio * math.sin(angulo), 2)

        return zona, [x, y]

    def obtener_tiros_serializables(self) -> List[dict]:
        """
        Convierte el historial de tiros a formato serializable.

        Returns:
            List[dict]: Lista de diccionarios con los datos de tiros
                       de cada jugador en formato JSON
        """
        return [asdict(player) for player in self.players.values()]

    def reset(self):
        """
        Reinicia el historial de tiros del blanco.

        Efectos:
            - Elimina todos los registros de tiros anteriores
        """
        self.players.clear()
