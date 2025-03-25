import uuid
import matplotlib.pyplot as plt
from .equipo import Equipo
from .blanco_objetivo import Blanco
from .ronda import Ronda


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
        self.visualizar_resultados()
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

    def visualizar_resultados(self):
        self.blanco.visualizar_tiros()
        self._graficar_evolucion_puntajes()

    def _graficar_evolucion_puntajes(self):
        rondas = [r["ronda"] for r in self.historial_puntajes]
        puntajes1 = [r["equipo1"]["puntaje"] for r in self.historial_puntajes]
        puntajes2 = [r["equipo2"]["puntaje"] for r in self.historial_puntajes]

        plt.figure(figsize=(10, 6))
        plt.plot(rondas, puntajes1, "o-", label=self.equipo1.nombre)
        plt.plot(rondas, puntajes2, "o-", label=self.equipo2.nombre)
        plt.xlabel("Ronda")
        plt.ylabel("Puntos")
        plt.title("Evolución de puntajes por ronda")
        plt.legend()
        plt.grid(True)
        plt.show()
