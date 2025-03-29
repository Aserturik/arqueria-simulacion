import random


class Ronda:
    def __init__(self, numero_ronda, equipo1, equipo2, blanco):
        self.numero_ronda = numero_ronda
        self.equipo1 = equipo1
        self.equipo2 = equipo2
        self.blanco = blanco
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
            "ronda": numero_ronda,
        }

    def jugar(self):
        #self._preparar_jugadores()
        self._jugar_turnos_equipos()
        self._jugar_tiro_extra()
        #self._realizar_lanzamiento_grupo()
        #self._manejar_lanzamientos_extra_consecutivos()
        self._determinar_ganador_individual()
        self._actualizar_experiencia()
        self._recuperar_resistencia()
        #self._registrar_tiros_jugadores()
        return self.resultado

    def _preparar_jugadores(self):
        """
        Prepara a los jugadores para la ronda, restaurando su resistencia original
        menos una o dos unidades para representar el cansancio acumulado.
        """
        for jugador in self.equipo1.jugadores + self.equipo2.jugadores:
            jugador.tiros_realizados = 0

    def _jugar_turnos_equipos(self):
        self._jugar_turno_equipo(self.equipo1, "equipo 1")
        self._jugar_turno_equipo(self.equipo2, "equipo 2")

    def _jugar_turno_equipo(self, equipo, clave_equipo):
        for jugador in equipo.jugadores:
            puntaje, tiros = 0, 0
            while jugador.puede_tirar():
                puntaje += self.blanco.realizar_tiro(jugador)
                tiros += 1
            self.resultado[clave_equipo]["puntaje"] += puntaje
            self.resultado[clave_equipo]["tiros"] += tiros
            jugador.puntaje_total += puntaje
    
    def _jugar_tiro_extra(self):
        # el jugador con más suerte de cada equipo lanza un tiro extra
        for equipo, clave in [(self.equipo1, "equipo 1"), (self.equipo2, "equipo 2")]:
            jugador = max(equipo.jugadores, key=lambda j: j.suerte)
            tiro = self.blanco.realizar_tiro(jugador)
            self.resultado[clave]["puntaje"] += tiro

    def _realizar_lanzamiento_grupo(self):
        for equipo, clave in [(self.equipo1, "equipo 1"), (self.equipo2, "equipo 2")]:
            jugador = max(equipo.jugadores, key=lambda j: j.suerte)
            tiro = self.blanco.realizar_tiro(jugador)
            self.resultado[clave]["puntaje_grupo"] += tiro
            equipo.puntaje_total += tiro

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

    def _determinar_ganador_individual(self):
        puntaje1 = self.resultado["equipo 1"]["puntaje"]
        puntaje2 = self.resultado["equipo 2"]["puntaje"]

        if puntaje1 > puntaje2:
            self._asignar_ganador_ronda(self.equipo1)
        elif puntaje2 > puntaje1:
            self._asignar_ganador_ronda(self.equipo2)
        else:
            self._desempatar_ronda()

    def _desempatar_ronda(self):
        while True:
            jugador1 = max(self.equipo1.jugadores, key=lambda j: j.punteria)
            jugador2 = max(self.equipo2.jugadores, key=lambda j: j.punteria)
            t1, t2 = self.blanco.realizar_tiro(jugador1), self.blanco.realizar_tiro(
                jugador2
            )

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
        if self.resultado["ganador_individual"] == self.equipo1.nombre:
            self._aumentar_experiencia(self.equipo1)
        elif self.resultado["ganador_individual"] == self.equipo2.nombre:
            self._aumentar_experiencia(self.equipo2)

    def _aumentar_experiencia(self, equipo):
        for jugador in equipo.jugadores:
            jugador.experiencia += 3
            if jugador.experiencia >= 9:
                jugador.beneficio_resistencia = True

    def _recuperar_resistencia(self):
        for jugador in self.equipo1.jugadores + self.equipo2.jugadores:
            jugador.cansancio_acumulado += random.randint(1, 2)
            jugador.actualizar_resistencia()
            #todo solo actualiza el cansancio acumulado. No actualiza la resistencia actual
