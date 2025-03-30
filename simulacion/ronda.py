from modelos.random_wrapper import randint


class Ronda:
    """
    Representa una ronda del juego de arquería donde dos equipos compiten.
    Maneja la lógica de los turnos, puntajes y determina los ganadores de la ronda.
    """

    def __init__(self, numero_ronda, equipo1, equipo2, blanco):
        """
        Inicializa una nueva ronda del juego.

        Args:
            numero_ronda (int): Número identificador de la ronda actual
            equipo1 (Equipo): Primer equipo participante
            equipo2 (Equipo): Segundo equipo participante
            blanco (Blanco): El blanco objetivo donde se realizarán los tiros

        Atributos:
            jugador_ganador: El jugador que obtuvo el mayor puntaje en la ronda
            jugador_con_mas_suerte: El jugador que tuvo la mayor suerte en la ronda
            jugador_con_mas_experiencia: El jugador con mayor experiencia acumulada
            resultado (dict): Diccionario que almacena todos los resultados de la ronda
        """
        self.numero_ronda = numero_ronda
        self.equipo1 = equipo1
        self.equipo2 = equipo2
        self.blanco = blanco
        self.jugador_ganador = None
        self.jugador_con_mas_suerte = None
        self.jugador_con_mas_experiencia = None
        self.resultado = {
            "ronda actual": numero_ronda,
            "equipo 1": {
                "nombre": equipo1.nombre,
                "puntaje": 0,
                "tiros": 0,
                "puntaje_grupo": 0,
                "tiros_jugadores": {},
            },
            "equipo 2": {
                "nombre": equipo2.nombre,
                "puntaje": 0,
                "tiros": 0,
                "puntaje_grupo": 0,
                "tiros_jugadores": {},
            },
            "ganador_individual": None,
            "ganador_grupal": None,
            "jugador_con_mas_suerte": self.jugador_con_mas_suerte,
            "jugador_con_mas_experiencia": self.jugador_con_mas_experiencia,
            "ronda": numero_ronda,
        }

    def jugar(self):
        """
        Ejecuta la secuencia completa de una ronda de juego.
        
        Secuencia:
        1. Los equipos juegan sus turnos
        2. Se realiza el tiro extra para el jugador con más suerte
        3. Se determina el jugador ganador
        4. Se determina el equipo ganador
        5. Se actualiza la experiencia de los jugadores
        6. Se actualiza la resistencia de los jugadores

        Returns:
            dict: Resultados completos de la ronda, incluyendo puntajes, ganadores y estadísticas
        """
        self._jugar_turnos_equipos()
        self._jugar_tiro_extra()
        self._determinar_jugador_ganador()
        # self._manejar_lanzamientos_extra_consecutivos()
        self._determinar_equipo_ganador()
        self._actualizar_experiencia()
        self._recuperar_resistencia()

        if self.jugador_con_mas_suerte:
            self.resultado["jugador_con_mas_suerte"] = {
                "nombre": self.jugador_con_mas_suerte.nombre,
                "user_id": self.jugador_con_mas_suerte.user_id,
                "suerte": self.jugador_con_mas_suerte.suerte,
                "equipo": (
                    "equipo 1"
                    if self.jugador_con_mas_suerte in self.equipo1.jugadores
                    else "equipo 2"
                ),
            }
        else:
            self.resultado["jugador_con_mas_suerte"] = "No determinado"

        if self.jugador_con_mas_experiencia:
            self.resultado["jugador_con_mas_experiencia"] = {
                "nombre": self.jugador_con_mas_experiencia.nombre,
                "user_id": self.jugador_con_mas_experiencia.user_id,
                "experiencia": self.jugador_con_mas_experiencia.experiencia,
                "equipo": (
                    "equipo 1"
                    if self.jugador_con_mas_experiencia in self.equipo1.jugadores
                    else "equipo 2"
                ),
            }
        else:
            self.resultado["jugador_con_mas_experiencia"] = "No determinado"
        return self.resultado

    def _jugar_turnos_equipos(self):
        """
        Gestiona los turnos de tiro de ambos equipos.
        Cada equipo realiza sus tiros en orden.
        """
        self._jugar_turno_equipo(self.equipo1, "equipo 1")
        self._jugar_turno_equipo(self.equipo2, "equipo 2")

    def _jugar_turno_equipo(self, equipo, clave_equipo):
        """
        Ejecuta el turno de tiro para un equipo específico.

        Args:
            equipo (Equipo): El equipo que realizará los tiros
            clave_equipo (str): Identificador del equipo ("equipo 1" o "equipo 2")
            
        Efectos:
            - Cada jugador del equipo realiza tiros mientras tenga suficiente resistencia
            - Se actualizan los puntajes y estadísticas del equipo en el resultado
            - Se reinicia la suerte de cada jugador antes de sus tiros
        """
        for jugador in equipo.jugadores:
            jugador.reiniciar_suerte()
            puntaje, tiros = 0, 0
            while jugador.puede_tirar():
                puntaje += self.blanco.realizar_tiro(jugador)
                tiros += 1
            self.resultado[clave_equipo]["puntaje"] += puntaje
            self.resultado[clave_equipo]["tiros"] += tiros
            jugador.puntaje_total += puntaje
            jugador.puntaje_ronda_actual = puntaje

    def _jugar_tiro_extra(self):
        """
        Ejecuta los tiros extra para los jugadores con más suerte de cada equipo.
        
        Efectos:
            - Identifica al jugador con más suerte de cada equipo
            - Les permite realizar un tiro adicional
            - Actualiza el puntaje del equipo con el resultado del tiro extra
        """
        # el jugador con más suerte de cada equipo lanza un tiro extra
        for equipo, clave in [(self.equipo1, "equipo 1"), (self.equipo2, "equipo 2")]:
            jugador = max(equipo.jugadores, key=lambda j: j.suerte)
            self.jugador_con_mas_suerte = jugador
            tiro = self.blanco.realizar_tiro(jugador)
            self.resultado[clave]["puntaje"] += tiro

    def _registrar_tiros_jugadores(self):
        """
        Registra los tiros de cada jugador en el resultado, asociándolos al equipo correspondiente.
        Utiliza el método obtener_tiros_serializables del blanco para obtener datos detallados.
        """
        tiros_serializados = self.blanco.obtener_tiros_serializables()

        # Creamos conjuntos con los IDs de los jugadores de cada equipo para búsqueda eficiente
        ids_equipo1 = {jugador.user_id for jugador in self.equipo1.jugadores}
        ids_equipo2 = {jugador.user_id for jugador in self.equipo2.jugadores}

        # Asignamos los tiros al equipo correspondiente
        for jugador_tiros in tiros_serializados:
            jugador_id = jugador_tiros["jugador_id"]

            if jugador_id in ids_equipo1:
                self.resultado["equipo 1"]["tiros_jugadores"][
                    jugador_id
                ] = jugador_tiros
            elif jugador_id in ids_equipo2:
                self.resultado["equipo 2"]["tiros_jugadores"][
                    jugador_id
                ] = jugador_tiros

    def _manejar_lanzamientos_extra_consecutivos(self):
        for jugador in self.equipo1.jugadores + self.equipo2.jugadores:
            if jugador.consecutivo_extra_ganados >= 3:
                tiro = self.blanco.realizar_tiro(jugador)
                equipo = (
                    self.equipo1 if jugador in self.equipo1.jugadores else self.equipo2
                )
                equipo.puntaje_total += tiro

                clave_equipo = "equipo 1" if equipo == self.equipo1 else "equipo 2"
                self.resultado[clave_equipo]["puntaje_grupo"] += tiro

                jugador.consecutivo_extra_ganados = 0

    def _determinar_equipo_ganador(self):
        """
        Determina qué equipo ganó la ronda basado en el puntaje total.
        
        Efectos:
            - Compara los puntajes totales de ambos equipos
            - Asigna el ganador o declara empate
            - Actualiza el resultado de la ronda con el equipo ganador
        """
        puntaje1 = self.resultado["equipo 1"]["puntaje"]
        puntaje2 = self.resultado["equipo 2"]["puntaje"]

        if puntaje1 > puntaje2:
            self._asignar_ganador_ronda(self.equipo1)
        elif puntaje2 > puntaje1:
            self._asignar_ganador_ronda(self.equipo2)
        else:
            # se salta a la siguiente ronda
            self.resultado["ganador_individual"] = "EMPATE"

    def _determinar_jugador_ganador(self):
        """
        Determina el jugador ganador de la ronda actual.

        Proceso:
        1. Encuentra el puntaje máximo entre todos los jugadores
        2. Identifica a todos los jugadores que tienen ese puntaje máximo
        3. Si hay un solo jugador con el puntaje máximo, es declarado ganador
        4. Si hay múltiples jugadores con el mismo puntaje máximo, se inicia un desempate

        Efectos:
            - Actualiza el atributo jugador_ganador con el jugador que ganó la ronda
            - En caso de empate, inicia el proceso de desempate
        """
        maximo = 0
        for jugador in self.equipo1.jugadores + self.equipo2.jugadores:
            if jugador.puntaje_ronda_actual > maximo:
                maximo = jugador.puntaje_ronda_actual

        # Find all players with the maximum score
        jugadores_empatados = [
            jugador
            for jugador in self.equipo1.jugadores + self.equipo2.jugadores
            if jugador.puntaje_ronda_actual == maximo
        ]

        # If there's only one player with the maximum score, they're the winner
        if len(jugadores_empatados) == 1:
            self.jugador_ganador = jugadores_empatados[0]
        else:
            # Call the tiebreaker function to determine a winner
            self.jugador_ganador = self._desempate(jugadores_empatados)

    def _desempate(self, jugadores_empatados):
        """
        Realiza un proceso de desempate entre jugadores con el mismo puntaje máximo.

        Args:
            jugadores_empatados (list): Lista de jugadores que empataron con el puntaje más alto

        Returns:
            Jugador: El jugador que ganó el desempate

        Proceso:
            1. Todos los jugadores empatados realizan un tiro adicional
            2. Solo los que obtienen el puntaje más alto continúan
            3. El proceso se repite hasta que quede un solo ganador
        """
        contendientes = jugadores_empatados.copy()

        while len(contendientes) > 1:
            # Cada jugador realiza un tiro
            puntajes = {}
            for jugador in contendientes:
                puntaje = self.blanco.realizar_tiro_desempate(jugador)
                puntajes[jugador] = puntaje

            # Encontrar el puntaje máximo de esta ronda de desempate
            max_puntaje = max(puntajes.values())

            # Filtrar jugadores que obtuvieron el puntaje máximo
            contendientes = [
                jugador for jugador in contendientes if puntajes[jugador] == max_puntaje
            ]

        # Devolver el único jugador que queda en contendientes
        return contendientes[0]

    def _desempatar_ronda(self):
        while True:
            jugador1 = max(self.equipo1.jugadores, key=lambda j: j.punteria)
            jugador2 = max(self.equipo2.jugadores, key=lambda j: j.punteria)
            t1, t2 = self.blanco.realizar_tiro_desempate(
                jugador1
            ), self.blanco.realizar_tiro_desempate(jugador2)

            if t1 > t2:
                self._asignar_ganador_ronda(self.equipo1, jugador1)
                break
            elif t2 > t1:
                self._asignar_ganador_ronda(self.equipo2, jugador2)
                break

    def _asignar_ganador_ronda(self, equipo, jugador_extra=None):
        equipo.rondas_ganadas += 1
        self.resultado["ganador_individual"] = equipo.nombre
        if jugador_extra:
            jugador_extra.consecutivo_extra_ganados += 1

    def _actualizar_experiencia(self):
        """
        Actualiza la experiencia de los jugadores después de la ronda.
        
        Efectos:
            - El jugador ganador recibe 3 puntos de experiencia
            - Si un jugador alcanza 19 puntos de experiencia, obtiene beneficio de resistencia
            - Identifica y actualiza el jugador con más experiencia del juego
        """
        # Solo el jugador ganador obtiene 3 puntos de experiencia
        if self.jugador_ganador:
            self.jugador_ganador.experiencia += 3

            # Activar beneficio si alcanza los 19 puntos
            if self.jugador_ganador.experiencia >= 19:
                self.jugador_ganador.beneficio_resistencia = True
                self.jugador_ganador.rondas_con_beneficio = 2  # Beneficio por 2 rondas

        # Encontrar el jugador con más experiencia entre todos los jugadores
        todos_los_jugadores = self.equipo1.jugadores + self.equipo2.jugadores
        if todos_los_jugadores:
            self.jugador_con_mas_experiencia = max(
                todos_los_jugadores, key=lambda j: j.experiencia
            )
        else:
            self.jugador_con_mas_experiencia = None

    def _recuperar_resistencia(self):
        """
        Gestiona la recuperación de resistencia de todos los jugadores al final de la ronda.
        
        Efectos:
            - Incrementa el cansancio acumulado de cada jugador
            - Actualiza los beneficios de resistencia si están activos
            - Ajusta la resistencia actual según el cansancio y beneficios
        """
        for jugador in self.equipo1.jugadores + self.equipo2.jugadores:
            jugador.cansancio_acumulado += randint(1, 2)

            # Decrementar contador de rondas con beneficio si está activo
            if jugador.beneficio_resistencia and jugador.rondas_con_beneficio > 0:
                jugador.rondas_con_beneficio -= 1
                # Desactivar beneficio si se acabaron las rondas
                if jugador.rondas_con_beneficio <= 0:
                    jugador.beneficio_resistencia = False

            jugador.actualizar_resistencia()
