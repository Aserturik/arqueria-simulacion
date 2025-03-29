import random
import math
from dataclasses import asdict, dataclass
from typing import List, Dict


@dataclass
class Lanzamiento:
    coordenadas: List[float]
    zona: int
    puntaje: int


@dataclass
class JugadorTiros:
    jugador_id: str
    nombre: str
    genero: str
    lanzamientos: List[Lanzamiento]


class Blanco:
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
        """Realiza un tiro y devuelve el puntaje obtenido"""
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
        """Crea una nueva entrada para un jugador"""
        self.players[jugador.user_id] = JugadorTiros(
            jugador_id=jugador.user_id,
            nombre=jugador.nombre,
            genero=jugador.genero,
            lanzamientos=[],
        )

    def _ajustar_probabilidades(self, jugador) -> Dict[str, float]:
        """Ajusta las probabilidades según habilidades del jugador"""
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
        """Genera coordenadas del tiro usando random estándar"""
        # Seleccionar zona
        zona = random.choices(
            population=list(probs.keys()), weights=list(probs.values()), k=1
        )[0]

        # Calcular radio según zona
        if zona == "ERROR":
            radio = random.uniform(
                self.RADIO_EXTERIOR, self.RADIO_EXTERIOR * self.RADIO_ERROR_MULTIPLIER
            )
        elif zona == "EXTERIOR":
            radio = random.uniform(self.RADIO_INTERMEDIA, self.RADIO_EXTERIOR)
        elif zona == "INTERMEDIA":
            radio = random.uniform(self.RADIO_CENTRAL, self.RADIO_INTERMEDIA)
        else:  # CENTRAL
            radio = random.uniform(0, self.RADIO_CENTRAL)

        # Generar coordenadas polares
        angulo = random.uniform(0, 2 * math.pi)
        x = round(radio * math.cos(angulo), 2)
        y = round(radio * math.sin(angulo), 2)

        return zona, [x, y]

    def obtener_tiros_serializables(self) -> List[dict]:
        """Devuelve los datos en formato JSON optimizado"""
        return [asdict(player) for player in self.players.values()]

    def reset(self):
        """Reinicia todos los registros"""
        self.players.clear()
