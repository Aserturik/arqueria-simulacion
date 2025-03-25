import random
import math
from dataclasses import asdict, dataclass
from typing import List, Dict


@dataclass
class Tiro:
    jugador_id: str
    nombre: str
    genero: str
    zona: str  # Nombre de la zona (ej: "CENTRAL")
    puntaje: int  # Puntaje numérico (10, 9, 8, 0)
    coordenadas: List[float]


class Blanco:
    # Mapeo zona -> puntaje
    ZONAS_PUNTAJE = {
        "CENTRAL": 10,
        "INTERMEDIA": 9,
        "EXTERIOR": 8,
        "ERROR": 0
    }

    # Radios de las zonas
    RADIO_CENTRAL = 1.0
    RADIO_INTERMEDIA = 3.0
    RADIO_EXTERIOR = 5.0
    RADIO_ERROR_MULTIPLIER = 1.5

    # Coste de resistencia por tiro
    TIRO_RESISTENCIA_COST = 5

    # Probabilidades base por género (usando nombres de zona)
    PROBABILIDADES = {
        "M": {"CENTRAL": 0.20, "INTERMEDIA": 0.33, "EXTERIOR": 0.40, "ERROR": 0.07},
        "F": {"CENTRAL": 0.30, "INTERMEDIA": 0.38, "EXTERIOR": 0.27, "ERROR": 0.05},
    }

    def __init__(self):
        self.tiros: List[Tiro] = []

    def realizar_tiro(self, jugador) -> int:
        """Devuelve solo el puntaje numérico"""
        if jugador.resistencia_actual < self.TIRO_RESISTENCIA_COST:
            return self.ZONAS_PUNTAJE["ERROR"]

        jugador.resistencia_actual -= self.TIRO_RESISTENCIA_COST
        jugador.tiros_realizados += 1

        # Ajuste dinámico de probabilidades
        probs = self._ajustar_probabilidades(jugador)
        zona, (x, y) = self._generar_tiro(probs)

        puntaje = self.ZONAS_PUNTAJE[zona]
        
        self.tiros.append(
            Tiro(
                jugador_id=jugador.user_id,
                nombre=jugador.nombre,
                genero=jugador.genero,
                zona=zona,
                puntaje=puntaje,
                coordenadas=[round(x, 2), round(y, 2)]
            )
        )

        return puntaje

    def _ajustar_probabilidades(self, jugador) -> Dict[str, float]:
        """Ajusta probabilidades usando experiencia y suerte del jugador"""
        probs = self.PROBABILIDADES[jugador.genero].copy()
        
        # Aumento para CENTRAL por suerte
        probs["CENTRAL"] *= (1 + 0.1 * (jugador.suerte / 3))
        
        # Reducción para ERROR por experiencia
        probs["ERROR"] *= (1 - 0.2 * (min(1.0, jugador.experiencia / 50)))
        
        # Normalización
        total = sum(probs.values())
        return {zona: prob / total for zona, prob in probs.items()}

    def _generar_tiro(self, probs: Dict[str, float]) -> tuple:
        """Genera coordenadas usando solo random estándar"""
        # Selección de zona
        zona = random.choices(
            population=list(probs.keys()),
            weights=list(probs.values()),
            k=1
        )[0]

        # Cálculo de radio según zona
        if zona == "ERROR":
            radio = random.uniform(self.RADIO_EXTERIOR, self.RADIO_EXTERIOR * self.RADIO_ERROR_MULTIPLIER)
        elif zona == "EXTERIOR":
            radio = random.uniform(self.RADIO_INTERMEDIA, self.RADIO_EXTERIOR)
        elif zona == "INTERMEDIA":
            radio = random.uniform(self.RADIO_CENTRAL, self.RADIO_INTERMEDIA)
        else:
            radio = random.uniform(0, self.RADIO_CENTRAL)

        # Coordenadas polares
        angulo = random.uniform(0, 2 * math.pi)
        x = radio * math.cos(angulo)
        y = radio * math.sin(angulo)

        return zona, (x, y)

    def obtener_tiros_serializables(self) -> List[dict]:
        return [asdict(tiro) for tiro in self.tiros]

    def reset(self):
        self.tiros = []