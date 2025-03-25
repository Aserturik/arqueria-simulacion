import uuid
import matplotlib.pyplot as plt
from .equipo import Equipo
from .blanco_objetivo import Blanco
from .ronda import Ronda
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


class Juego:
    def __init__(self, nombre_equipo1, nombre_equipo2, num_jugadores=5, num_rondas=10):
        self.id_juego = str(uuid.uuid4())
        self.equipo1 = Equipo(nombre_equipo1, "M", num_jugadores)
        self.equipo2 = Equipo(nombre_equipo2, "F", num_jugadores)
        self.blanco = Blanco()
        self.num_rondas = num_rondas
        self.ronda_actual = 0
        self.historial_puntajes = []

    def jugar_ronda(self):
        self.ronda_actual += 1
        ronda = Ronda(self.ronda_actual, self.equipo1, self.equipo2, self.blanco)
        resultado = ronda.jugar()
        self.historial_puntajes.append(resultado)
        self._mostrar_resultados_ronda(resultado)
        return resultado

    def jugar_partida_completa(self):
        print("¡COMIENZA EL JUEGO DE ARQUERÍA!")
        print(f"Equipo 1: {self.equipo1.nombre} (M)")
        print(f"Equipo 2: {self.equipo2.nombre} (F)")

        for _ in range(self.num_rondas):
            self.jugar_ronda()

        self._finalizar_juego()

    def _mostrar_resultados_ronda(self, resultado):
        print(f"\n--- RESULTADOS RONDA {self.ronda_actual} ---")
        print(f"{self.equipo1.nombre}: {resultado['equipo1']['puntaje']} puntos")
        print(f"{self.equipo2.nombre}: {resultado['equipo2']['puntaje']} puntos")
        print(f"Ganador: {resultado['ganador_individual']}")

    def _finalizar_juego(self):
        self._determinar_ganador_final()
        self._reiniciar_jugadores()

    def _determinar_ganador_final(self):
        print("\n--- RESULTADO FINAL ---")
        print(f"{self.equipo1.nombre}: {self.equipo1.rondas_ganadas} rondas")
        print(f"{self.equipo2.nombre}: {self.equipo2.rondas_ganadas} rondas")

        if self.equipo1.rondas_ganadas > self.equipo2.rondas_ganadas:
            print(f"¡{self.equipo1.nombre} gana el juego!")
        elif self.equipo2.rondas_ganadas > self.equipo1.rondas_ganadas:
            print(f"¡{self.equipo2.nombre} gana el juego!")
        else:
            print("¡Empate!")

    def _reiniciar_jugadores(self):
        for jugador in self.equipo1.jugadores + self.equipo2.jugadores:
            jugador.resistencia_actual = jugador.resistencia_inicial
            jugador.consecutivo_extra_ganados = 0

    def generar_imagen_resultados(self):
        import io
        import base64
        import matplotlib.pyplot as plt
        from matplotlib.patches import Circle

        # 1. Evolución de puntajes por ronda (line plot)
        rondas = [r["ronda"] for r in self.historial_puntajes]
        puntajes1 = [r["equipo1"]["puntaje"] for r in self.historial_puntajes]
        puntajes2 = [r["equipo2"]["puntaje"] for r in self.historial_puntajes]

        fig1, ax1 = plt.subplots(figsize=(10, 6))
        ax1.plot(rondas, puntajes1, "o-", label=self.equipo1.nombre)
        ax1.plot(rondas, puntajes2, "o-", label=self.equipo2.nombre)
        ax1.set_xlabel("Ronda")
        ax1.set_ylabel("Puntos")
        ax1.set_title("Evolución de puntajes por ronda")
        ax1.legend()
        ax1.grid(True)

        buf1 = io.BytesIO()
        fig1.savefig(buf1, format="png")
        buf1.seek(0)
        imagen_evolucion = base64.b64encode(buf1.read()).decode("utf-8")
        plt.close(fig1)

        # 2. Puntaje Total Final (bar chart)
        final_puntaje1 = sum(puntajes1)
        final_puntaje2 = sum(puntajes2)

        fig2, ax2 = plt.subplots(figsize=(6, 6))
        equipos = [self.equipo1.nombre, self.equipo2.nombre]
        final_puntajes = [final_puntaje1, final_puntaje2]
        ax2.bar(equipos, final_puntajes, color=["blue", "orange"])
        ax2.set_xlabel("Equipo")
        ax2.set_ylabel("Puntaje Total")
        ax2.set_title("Puntaje Total Final")
        ax2.grid(axis="y")

        buf2 = io.BytesIO()
        fig2.savefig(buf2, format="png")
        buf2.seek(0)
        imagen_final = base64.b64encode(buf2.read()).decode("utf-8")
        plt.close(fig2)

        # 3. Visualización del Blanco con disparos
        # Se usa la información de la instancia self.blanco.
        # Se dibujan los anillos del blanco y cada disparo, coloreado según el género.
        fig3, ax3 = plt.subplots(figsize=(8, 8))

        # Dibujar anillos del blanco (se puede ajustar los colores para diferenciarlos)
        ax3.add_patch(
            Circle((0, 0), self.blanco.RADIO_EXTERIOR, fill=False, color="black", lw=2)
        )
        ax3.add_patch(
            Circle(
                (0, 0), self.blanco.RADIO_INTERMEDIA, fill=False, color="black", lw=2
            )
        )
        ax3.add_patch(
            Circle((0, 0), self.blanco.RADIO_CENTRAL, fill=False, color="black", lw=2)
        )

        # Límites y aspecto
        lim = self.blanco.RADIO_EXTERIOR * 1.5
        ax3.set_xlim(-lim, lim)
        ax3.set_ylim(-lim, lim)
        ax3.set_aspect("equal")
        ax3.grid(True)

        # Dibujar cada tiro
        for tiro in self.blanco.tiros:
            x, y = tiro["coordenadas"]
            color = "blue" if tiro["genero"] == "M" else "red"
            ax3.plot(x, y, "o", color=color, markersize=5)
        ax3.set_title("Disparos en el Blanco")

        buf3 = io.BytesIO()
        fig3.savefig(buf3, format="png")
        buf3.seek(0)
        imagen_blanco = base64.b64encode(buf3.read()).decode("utf-8")
        plt.close(fig3)

        return {
            "evolucion": imagen_evolucion,
            "final": imagen_final,
            "blanco": imagen_blanco,
        }
