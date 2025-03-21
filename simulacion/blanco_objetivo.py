import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import random


class Blanco:
    # Definición de zonas y puntajes
    CENTRAL = 10
    INTERMEDIA = 9
    EXTERIOR = 8
    ERROR = 0

    # Radio de cada zona (unidades arbitrarias)
    RADIO_CENTRAL = 1.0
    RADIO_INTERMEDIA = 2.0
    RADIO_EXTERIOR = 3.0

    # Probabilidades por género (porcentajes)
    PROBABILIDADES = {
        "M": {
            CENTRAL: 0.20,  # 20%
            INTERMEDIA: 0.33,  # 33%
            EXTERIOR: 0.40,  # 40%
            ERROR: 0.07,  # 7%
        },
        "F": {
            CENTRAL: 0.30,  # 30%
            INTERMEDIA: 0.38,  # 38%
            EXTERIOR: 0.27,  # 27%
            ERROR: 0.05,  # 5%
        },
    }

    def __init__(self):
        self.tiros = []  # Lista para guardar todos los tiros realizados

    def realizar_tiro(self, jugador):
        """
        Realiza un tiro simulado basado en las habilidades del jugador y las probabilidades por género
        """
        # Verificar si el jugador puede realizar el tiro
        if jugador.resistencia < 5:
            return 0

        # Reducir resistencia y contabilizar tiro
        jugador.resistencia -= 5
        jugador.tiros_realizados += 1

        # Obtenemos probabilidades según género
        probs = self.PROBABILIDADES[jugador.genero]

        # Ajustamos probabilidades según habilidades del jugador
        # La experiencia mejora la precisión (reduce probabilidad de error)
        factor_experiencia = min(1.0, jugador.experiencia / 50)
        # La suerte puede ayudar a dar en zonas de mayor puntaje
        factor_suerte = jugador.suerte / 3.0

        # Ajustamos probabilidades
        probs_ajustadas = {
            self.CENTRAL: probs[self.CENTRAL] * (1 + 0.1 * factor_suerte),
            self.INTERMEDIA: probs[self.INTERMEDIA],
            self.EXTERIOR: probs[self.EXTERIOR],
            self.ERROR: probs[self.ERROR] * (1 - 0.2 * factor_experiencia),
        }

        # Normalizamos para que sumen 1
        total = sum(probs_ajustadas.values())
        probs_ajustadas = {k: v / total for k, v in probs_ajustadas.items()}

        # Simulamos el tiro usando distribución de probabilidad
        zonas = [self.CENTRAL, self.INTERMEDIA, self.EXTERIOR, self.ERROR]
        probabilidades = [probs_ajustadas[zona] for zona in zonas]
        zona_impacto = np.random.choice(zonas, p=probabilidades)

        # Generamos coordenadas para representar gráficamente
        if zona_impacto == self.ERROR:
            # Fuera del blanco (radio > RADIO_EXTERIOR)
            angulo = random.uniform(0, 2 * np.pi)
            radio = random.uniform(self.RADIO_EXTERIOR, self.RADIO_EXTERIOR * 1.5)
        elif zona_impacto == self.EXTERIOR:
            angulo = random.uniform(0, 2 * np.pi)
            radio = random.uniform(self.RADIO_INTERMEDIA, self.RADIO_EXTERIOR)
        elif zona_impacto == self.INTERMEDIA:
            angulo = random.uniform(0, 2 * np.pi)
            radio = random.uniform(self.RADIO_CENTRAL, self.RADIO_INTERMEDIA)
        else:  # CENTRAL
            angulo = random.uniform(0, 2 * np.pi)
            radio = random.uniform(0, self.RADIO_CENTRAL)

        x = radio * np.cos(angulo)
        y = radio * np.sin(angulo)

        # Guardamos el tiro
        tiro = {
            "jugador_id": jugador.user_id,
            "nombre": jugador.nombre,
            "genero": jugador.genero,
            "zona": zona_impacto,
            "puntaje": zona_impacto,
            "coordenadas": (x, y),
        }
        self.tiros.append(tiro)

        return zona_impacto  # Retornamos el puntaje

    def visualizar_tiros(self, ultimos_n=None):
        """
        Visualiza la diana y los últimos n tiros realizados
        Si ultimos_n es None, muestra todos los tiros
        """
        fig, ax = plt.subplots(figsize=(8, 8))

        # Dibujamos la diana
        ax.add_patch(Circle((0, 0), self.RADIO_EXTERIOR, fill=False, color="black"))
        ax.add_patch(Circle((0, 0), self.RADIO_INTERMEDIA, fill=False, color="black"))
        ax.add_patch(Circle((0, 0), self.RADIO_CENTRAL, fill=False, color="black"))

        # Límites del gráfico
        ax.set_xlim(-self.RADIO_EXTERIOR * 1.5, self.RADIO_EXTERIOR * 1.5)
        ax.set_ylim(-self.RADIO_EXTERIOR * 1.5, self.RADIO_EXTERIOR * 1.5)
        ax.set_aspect("equal")

        # Dibujamos los tiros
        tiros_mostrar = self.tiros
        if ultimos_n is not None:
            tiros_mostrar = self.tiros[-ultimos_n:]

        for tiro in tiros_mostrar:
            x, y = tiro["coordenadas"]
            color = "blue" if tiro["genero"] == "M" else "red"
            ax.plot(x, y, "o", color=color, markersize=5)

        plt.title("Simulación de Tiros en Diana")
        plt.grid(True)
        plt.show()

    def reset(self):
        """Reinicia el historial de tiros"""
        self.tiros = []
