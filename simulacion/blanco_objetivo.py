import numpy as np
import random
from dataclasses import asdict, dataclass
from typing import List, Dict


@dataclass
class Tiro:
    jugador_id: str
    nombre: str
    genero: str
    zona: int
    puntaje: int
    coordenadas: List[float]  # Lista para mejor compatibilidad JSON


class Blanco:
    CENTRAL = 10
    INTERMEDIA = 9
    EXTERIOR = 8
    ERROR = 0

    RADIO_CENTRAL = 1.0
    RADIO_INTERMEDIA = 3.0
    RADIO_EXTERIOR = 5.0
    RADIO_ERROR_MULTIPLIER = 1.5  # Para tiros fuera de la diana

    TIRO_RESISTENCIA_COST = 5  # Costo en resistencia por tiro
    EXPERIENCIA_MAX = 50  # Máximo para normalizar experiencia
    SUERTE_DIVISOR = 3.0  # Factor de ajuste de suerte

    # Factores de ajuste de probabilidades
    FACTOR_AUMENTO_SUERTE = 0.1
    FACTOR_REDUCCION_EXPERIENCIA = 0.2

    PROBABILIDADES = {
        "M": {CENTRAL: 0.20, INTERMEDIA: 0.33, EXTERIOR: 0.40, ERROR: 0.07},
        "F": {CENTRAL: 0.30, INTERMEDIA: 0.38, EXTERIOR: 0.27, ERROR: 0.05},
    }

    def __init__(self):
        self.tiros: List[Tiro] = []  

    def realizar_tiro(self, jugador) -> int:
        if jugador.resistencia_actual < self.TIRO_RESISTENCIA_COST:
            return 0

        jugador.resistencia_actual -= self.TIRO_RESISTENCIA_COST
        jugador.tiros_realizados += 1

        probs = self.PROBABILIDADES[jugador.genero]
        factor_experiencia = min(1.0, jugador.experiencia / self.EXPERIENCIA_MAX)
        factor_suerte = jugador.suerte / self.SUERTE_DIVISOR

        # Ajuste de probabilidades con constantes
        probs_ajustadas = {
            self.CENTRAL: probs[self.CENTRAL]
            * (1 + self.FACTOR_AUMENTO_SUERTE * factor_suerte),
            self.INTERMEDIA: probs[self.INTERMEDIA],
            self.EXTERIOR: probs[self.EXTERIOR],
            self.ERROR: probs[self.ERROR]
            * (1 - self.FACTOR_REDUCCION_EXPERIENCIA * factor_experiencia),
        }

        # Normalización
        total = sum(probs_ajustadas.values())
        probs_ajustadas = {k: v / total for k, v in probs_ajustadas.items()}

        # Generación de coordenadas
        zona_impacto, radio = self._generar_coordenadas(probs_ajustadas)
        x, y = radio * np.cos((angulo := random.uniform(0, 2 * np.pi))), radio * np.sin(
            angulo
        )

        self.tiros.append(
            Tiro(
                jugador_id=jugador.user_id,
                nombre=jugador.nombre,
                genero=jugador.genero,
                zona=zona_impacto,
                puntaje=zona_impacto,
                coordenadas=[round(x, 2), round(y, 2)],  # Lista y redondeo para JSON
            )
        )

        return zona_impacto

    def _generar_coordenadas(self, probs_ajustadas: Dict[int, float]) -> tuple:
        zona_impacto = np.random.choice(
            list(probs_ajustadas.keys()), p=list(probs_ajustadas.values())
        )

        if zona_impacto == self.ERROR:
            radio = random.uniform(
                self.RADIO_EXTERIOR, self.RADIO_EXTERIOR * self.RADIO_ERROR_MULTIPLIER
            )
        elif zona_impacto == self.EXTERIOR:
            radio = random.uniform(self.RADIO_INTERMEDIA, self.RADIO_EXTERIOR)
        elif zona_impacto == self.INTERMEDIA:
            radio = random.uniform(self.RADIO_CENTRAL, self.RADIO_INTERMEDIA)
        else:  # CENTRAL
            radio = random.uniform(0, self.RADIO_CENTRAL)

        return zona_impacto, radio

    def obtener_tiros_serializables(self) -> List[dict]:
        """Devuelve los tiros en formato JSON-friendly"""
        return [asdict(tiro) for tiro in self.tiros]

    def reset(self):
        self.tiros = []
