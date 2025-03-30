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
        self.equipo1.puntaje_juego = 0
        self.equipo2.puntaje_juego = 0
        self.puntaje_ganador = 0
        self.experiencia_maxima = 0
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

    def jugar_juego_completo(self):
        for jugador in self.equipo1.jugadores + self.equipo2.jugadores:
            jugador.resetear_jugador()
            jugador.guardar_puntaje_total()

        for _ in range(self.num_rondas):
            self.jugar_ronda()

        self.resultado_puntos_por_jugador()
        self.determinar_jugador_con_mas_suerte()
        self.determinar_jugador_con_mas_experiencia()
        self._finalizar_juego()

    def _finalizar_juego(self):
        self.equipo_ganador_del_juego()
        self.puntaje_equipo1_final = self.equipo1.puntaje_juego
        self.puntaje_equipo2_final = self.equipo2.puntaje_juego
        self.guardar_estadisticas()
        self.reiniciar_equipos()

    def guardar_estadisticas(self):
        if self.equipo_ganador_del_juego:
            self.equipo_ganador_juego.puntaje_juego += self.puntaje_ganador

    def equipo_ganador_del_juego(self):
        # Calcular puntajes totales del juego
        self.equipo1.puntaje_juego = sum(
            ronda["equipo 1"]["puntaje"] for ronda in self.historial_rondas
        )
        self.equipo2.puntaje_juego = sum(
            ronda["equipo 2"]["puntaje"] for ronda in self.historial_rondas
        )

        # Asignar puntajes a los equipos
        self.equipo1.puntaje_juego = self.equipo1.puntaje_juego
        self.equipo2.puntaje_juego = self.equipo2.puntaje_juego

        # Guardar el puntaje más alto
        self.puntaje_ganador = max(
            self.equipo1.puntaje_juego, self.equipo2.puntaje_juego
        )

        # Determinar ganador
        if self.equipo1.puntaje_juego > self.equipo2.puntaje_juego:
            self.equipo1.juegos_ganados += 1
            self.equipo_ganador_juego = self.equipo1
        elif self.equipo2.puntaje_juego > self.equipo1.puntaje_juego:
            self.equipo2.juegos_ganados += 1
            self.equipo_ganador_juego = self.equipo2
        else:
            # Empate
            self.equipo_ganador_juego = None

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
        """Determina el jugador con mayor experiencia acumulada."""
        todos_jugadores = self.equipo1.jugadores + self.equipo2.jugadores

        if todos_jugadores:
            # Encuentra el jugador con mayor experiencia
            self.jugador_con_mas_experiencia = max(
                todos_jugadores, key=lambda j: j.experiencia
            )
            # Guarda la experiencia actual antes de que se reinicie
            self.experiencia_maxima = self.jugador_con_mas_experiencia.experiencia
        else:
            self.jugador_con_mas_experiencia = "No determinado"
            self.experiencia_maxima = 10
