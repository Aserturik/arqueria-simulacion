import uuid
from .blanco_objetivo import Blanco
from .ronda import Ronda


class Juego:
    """
    Clase principal que coordina un juego completo de arquería.
    Gestiona la interacción entre equipos, rondas y mantiene estadísticas globales.
    """

    generos_victorias_totales = {"M": 0, "F": 0}  # Contador de victorias por género

    def __init__(self, equipo1, equipo2, num_rondas=10, juego_actual=0):
        """
        Inicializa un nuevo juego de arquería.

        Args:
            equipo1 (Equipo): Primer equipo participante
            equipo2 (Equipo): Segundo equipo participante
            num_rondas (int): Número de rondas a jugar (default: 10)
            juego_actual (int): Número identificador del juego actual

        Atributos:
            id_juego (str): Identificador único del juego
            historial_rondas (List[dict]): Registro de resultados de cada ronda
            puntaje_ganador (int): Puntaje más alto obtenido en el juego
            experiencia_maxima (int): Máxima experiencia alcanzada por un jugador
            jugador_con_mas_suerte (Jugador): Jugador que tuvo más suerte en el juego
            jugador_con_mas_experiencia (Jugador): Jugador con mayor experiencia acumulada
            equipo_ganador_juego (Equipo): Equipo que ganó el juego
            genero_con_mas_victorias (str): Género que acumuló más victorias
        """
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
        self.victorias_por_genero = {"M": 0, "F": 0}

    def jugar_ronda(self):
        """
        Ejecuta una ronda individual del juego.
        
        Efectos:
            - Incrementa el contador de ronda actual
            - Crea y ejecuta una nueva instancia de Ronda
            - Almacena el resultado en el historial
        """
        self.ronda_actual += 1
        ronda = Ronda(self.ronda_actual, self.equipo1, self.equipo2, self.blanco)
        resultado = ronda.jugar()
        self.historial_rondas.append(resultado)

    def jugar_juego_completo(self):
        """
        Ejecuta la secuencia completa de un juego.
        
        Secuencia:
        1. Reinicia el estado de todos los jugadores
        2. Ejecuta todas las rondas programadas
        3. Calcula y actualiza estadísticas finales
        4. Determina ganadores y récords

        Efectos:
            - Actualiza todas las estadísticas del juego
            - Determina y registra ganadores
            - Actualiza contadores globales
        """
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
        """
        Realiza las operaciones de finalización del juego.
        
        Efectos:
            - Determina el equipo ganador
            - Guarda los puntajes finales
            - Actualiza estadísticas de género
            - Reinicia los equipos para el siguiente juego
        """
        self.equipo_ganador_del_juego()
        self.puntaje_equipo1_final = self.equipo1.puntaje_juego
        self.puntaje_equipo2_final = self.equipo2.puntaje_juego
        self.determinar_genero_con_mas_victorias()
        self.guardar_estadisticas()
        self.reiniciar_equipos()

    def guardar_estadisticas(self):
        """
        Actualiza las estadísticas del equipo ganador.
        
        Efectos:
            - Incrementa el puntaje del equipo ganador
        """
        if self.equipo_ganador_juego is not None:
            self.equipo_ganador_juego.puntaje_juego += self.puntaje_ganador

    def equipo_ganador_del_juego(self):
        """
        Determina y registra el equipo ganador del juego.
        
        Proceso:
        1. Calcula los puntajes totales de ambos equipos
        2. Compara los puntajes y determina el ganador
        3. Actualiza los contadores de juegos ganados
        4. Registra el equipo ganador y el puntaje más alto

        Efectos:
            - Actualiza puntajes de los equipos
            - Incrementa contador de juegos ganados
            - Establece el equipo_ganador_juego
        """
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
        """
        Prepara los equipos para un nuevo juego.
        
        Efectos:
            - Reinicia los puntajes de ambos equipos
            - Finaliza el juego para todos los jugadores
        """
        # se reinician las estadísticas de los equipos
        self.equipo1.puntaje_juego = 0
        self.equipo2.puntaje_juego = 0

        for jugador in self.equipo1.jugadores + self.equipo2.jugadores:
            jugador.finalizar_juego()

    def resultado_puntos_por_jugador(self):
        """
        Calcula y registra los puntos individuales de cada jugador.
        
        Efectos:
            - Actualiza puntaje_juego_actual de cada jugador
            - Mantiene registro de puntos por jugador
        """
        puntos_por_jugador = {}
        for jugador in self.equipo1.jugadores + self.equipo2.jugadores:
            jugador.puntaje_juego_actual = (
                jugador.puntaje_total - jugador.puntaje_juego_anterior
            )
            puntos_por_jugador[jugador.nombre] = jugador.puntaje_juego_actual

    def determinar_jugador_con_mas_suerte(self):
        """
        Identifica al jugador que tuvo más suerte durante el juego.
        
        Proceso:
        1. Analiza cada ronda del historial
        2. Cuenta las veces que cada jugador fue el más afortunado
        3. Determina el jugador con más apariciones como "más suerte"

        Efectos:
            - Actualiza el atributo jugador_con_mas_suerte
        """
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
        """
        Identifica y registra el jugador con mayor experiencia acumulada.
        
        Proceso:
        1. Compara la experiencia de todos los jugadores
        2. Registra al jugador con mayor experiencia
        3. Guarda el valor máximo de experiencia alcanzado

        Efectos:
            - Actualiza jugador_con_mas_experiencia
            - Actualiza experiencia_maxima
        """
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

    def determinar_genero_con_mas_victorias(self):
        """
        Analiza y registra las victorias por género en el juego actual.
        
        Proceso:
        1. Analiza cada ronda y determina el género del ganador
        2. Acumula victorias por género
        3. Determina el género con más victorias
        4. Actualiza el contador global si no hubo empate

        Efectos:
            - Actualiza victorias_por_genero
            - Actualiza genero_con_mas_victorias
            - Actualiza el contador global generos_victorias_totales
        """
        # Analizamos cada ronda para contar victorias por género
        for ronda in self.historial_rondas:
            if ronda["ganador_individual"] != "EMPATE" and ronda["ganador_individual"]:
                # Identificar el equipo ganador
                equipo_ganador = (
                    self.equipo1
                    if ronda["ganador_individual"] == self.equipo1.nombre
                    else self.equipo2
                )

                # Encontrar al jugador con mayor puntaje de ese equipo en esa ronda
                mejor_jugador = None
                mejor_puntaje = -1

                for jugador in equipo_ganador.jugadores:
                    for j in self.equipo1.jugadores + self.equipo2.jugadores:
                        if (
                            j.nombre == jugador.nombre
                            and j.puntaje_ronda_actual > mejor_puntaje
                        ):
                            mejor_puntaje = j.puntaje_ronda_actual
                            mejor_jugador = j

                # Sumar victoria al género correspondiente
                if mejor_jugador:
                    self.victorias_por_genero[mejor_jugador.genero] += 1

        # Determinar el género con más victorias en este juego
        if self.victorias_por_genero["M"] > self.victorias_por_genero["F"]:
            self.genero_con_mas_victorias = "M"
        elif self.victorias_por_genero["F"] > self.victorias_por_genero["M"]:
            self.genero_con_mas_victorias = "F"
        else:
            self.genero_con_mas_victorias = "Empate"

        # Actualizar el contador global si no fue empate
        if self.genero_con_mas_victorias != "Empate":
            Juego.generos_victorias_totales[self.genero_con_mas_victorias] += 1
