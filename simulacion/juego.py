import uuid
from .blanco_objetivo import Blanco
from .ronda import Ronda


class Juego:
    def __init__(self, equipo1, equipo2, num_rondas=10, juego_actual=0):
        self.id_juego = str(uuid.uuid4())
        self.equipo1 = equipo1
        self.equipo2 = equipo2
        self.blanco = Blanco()
        self.num_rondas = num_rondas
        self.ronda_actual = 0
        self.historial_rondas = []
        self.juego_actual = juego_actual
        # Requisitos solicitados:
        self.jugador_con_mas_suerte = None
        self.jugador_con_mas_experiencia = None
        self.equipo_con_mas_rondas_ganadas = None
        self.genero_con_mas_victorias = None

    def jugar_ronda(self):
        self.ronda_actual += 1
        ronda = Ronda(self.ronda_actual, self.equipo1, self.equipo2, self.blanco)
        resultado = ronda.jugar()
        self.historial_rondas.append(resultado)
        # self._mostrar_resultados_ronda(resultado)
        return resultado

    def jugar_partida_completa(self):
        for jugador in self.equipo1.jugadores + self.equipo2.jugadores:
            jugador.guardar_puntaje_total()

        for _ in range(self.num_rondas):
            self.jugar_ronda()

        self.resultado_puntos_por_jugador()
        self._finalizar_ronda()

    def _mostrar_resultados_ronda(self, resultado):
        print(f"\n--- RESULTADOS RONDA {self.ronda_actual} ---")
        print(f"Ganador: {resultado['ganador_individual']}")

    def _finalizar_ronda(self):
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

    def resultado_puntos_por_jugador(self):
        puntos_por_jugador = {}
        for jugador in self.equipo1.jugadores + self.equipo2.jugadores:
            jugador.puntaje_juego_actual = jugador.puntaje_total - jugador.puntaje_juego_anterior
            puntos_por_jugador[jugador.nombre] = (
                jugador.puntaje_juego_actual
            )

        print(puntos_por_jugador)
        return puntos_por_jugador
