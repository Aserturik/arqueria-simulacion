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
        self.equipo_ganador_juego = None
        self.genero_con_mas_victorias = None

    def jugar_ronda(self):
        self.ronda_actual += 1
        ronda = Ronda(self.ronda_actual, self.equipo1, self.equipo2, self.blanco)
        resultado = ronda.jugar()
        self.historial_rondas.append(resultado)
        # self._mostrar_resultados_ronda(resultado)

    def jugar_juego_completo(self):
        for jugador in self.equipo1.jugadores + self.equipo2.jugadores:
            jugador.resetear_jugador()
            jugador.guardar_puntaje_total()

        for _ in range(self.num_rondas):
            self.jugar_ronda()

        self.resultado_puntos_por_jugador()
        self.determinar_jugador_con_mas_suerte()
        #self.determinar_jugador_con_mas_experiencia()
        self._finalizar_juego()

    def _mostrar_resultados_ronda(self, resultado):
        print(f"\n--- RESULTADOS RONDA {self.ronda_actual} ---")
        print(f"Ganador: {resultado['ganador_individual']}")

    def _finalizar_juego(self):
        self.equipo_ganador_del_juego()
        self.reiniciar_equipos()

    def equipo_ganador_del_juego(self):
        for ronda in self.historial_rondas:
            self.equipo1.puntaje_juego += ronda["equipo 1"]["puntaje"]
            self.equipo2.puntaje_juego += ronda["equipo 2"]["puntaje"]

        print("\n--- RESULTADO DEL JUEGO ---")
        if self.equipo1.puntaje_juego > self.equipo2.puntaje_juego:
            self.equipo1.juegos_ganados += 1
            self.equipo_ganador_juego = self.equipo1
            print(
                f"¡{self.equipo1.nombre} gana el juego! con un puntaje de {self.equipo1.puntaje_juego} puntos."
            )
            print(
                f"¡{self.equipo2.nombre} pierde el juego! con un puntaje de {self.equipo2.puntaje_juego} puntos."
            )
        elif self.equipo2.puntaje_juego > self.equipo1.puntaje_juego:
            self.equipo2.juegos_ganados += 1
            self.equipo_ganador_juego = self.equipo2
            print(
                f"¡{self.equipo2.nombre} gana el juego! con un puntaje de {self.equipo2.puntaje_juego} puntos."
            )
            print(
                f"¡{self.equipo1.nombre} pierde el juego! con un puntaje de {self.equipo1.puntaje_juego} puntos."
            )
        else:
            # Empate en el juego
            self.equipo1.juegos_ganados += 0
            self.equipo2.juegos_ganados += 0
            self.equipo_ganador_juego = None
            print("¡Empate en el juego!")

    def reiniciar_equipos(self):
        # se reinician las estadísticas de los equipos
        self.equipo1.puntaje_juego = 0
        self.equipo2.puntaje_juego = 0

        for jugador in self.equipo1.jugadores + self.equipo2.jugadores:
            jugador.finalizar_juego()

    def resultado_puntos_por_jugador(self):
        puntos_por_jugador = {}
        for jugador in self.equipo1.jugadores + self.equipo2.jugadores:
            jugador.puntaje_juego_actual = (
                jugador.puntaje_total - jugador.puntaje_juego_anterior
            )
            puntos_por_jugador[jugador.nombre] = jugador.puntaje_juego_actual

        print(puntos_por_jugador)

    def determinar_jugador_con_mas_suerte(self):
        # se busca en cada ronda el jugador con más suerte
        # el atributo "jugador_con_mas_suerte" de la ronda
        # el jugador que más veces aparezca como jugador con más suerte
        # es el jugador con más suerte del juego
        jugadores_suerte = {}
        for ronda in self.historial_rondas:
            jugador_id = ronda["jugador_con_mas_suerte"]["user_id"]

            if jugador_id not in jugadores_suerte:
                jugadores_suerte[jugador_id] = 1
            else:
                jugadores_suerte[jugador_id] += 1
        # se busca el jugador con más suerte
        if jugadores_suerte:
            jugador_id_mas_suerte = max(jugadores_suerte, key=jugadores_suerte.get)

            # se busca el jugador con más suerte
            for jugador in self.equipo1.jugadores + self.equipo2.jugadores:
                if jugador.user_id == jugador_id_mas_suerte:
                    self.jugador_con_mas_suerte = jugador
                    break
            else:
                self.jugador_con_mas_suerte = "No determinado"
        else:
            self.jugador_con_mas_suerte = "No determinado"

    def determinar_jugador_con_mas_experiencia(self):
        # se busca en cada ronda el jugador con más experiencia
        # el atributo "jugador_con_mas_experiencia" de la ronda
        # el jugador que más veces aparezca como jugador con más experiencia
        # es el jugador con más experiencia del juego
        jugadores_experiencia = {}
        for ronda in self.historial_rondas:
            jugador_id = ronda["jugador_con_mas_experiencia"]["user_id"]

            if jugador_id not in jugadores_experiencia:
                jugadores_experiencia[jugador_id] = 1
            else:
                jugadores_experiencia[jugador_id] += 1
        # se busca el jugador con más experiencia
        if jugadores_experiencia:
            jugador_id_mas_experiencia = max(
                jugadores_experiencia, key=jugadores_experiencia.get
            )

            # se busca el jugador con más experiencia
            for jugador in self.equipo1.jugadores + self.equipo2.jugadores:
                if jugador.user_id == jugador_id_mas_experiencia:
                    self.jugador_con_mas_experiencia = jugador
                    break
            else:
                self.jugador_con_mas_experiencia = "No determinado"
        else:
            self.jugador_con_mas_experiencia = "No determinado"
