import random
from .blanco_objetivo import Blanco


class Ronda:
    def __init__(self, numero_ronda, equipo1, equipo2, blanco):
        self.numero_ronda = numero_ronda
        self.equipo1 = equipo1
        self.equipo2 = equipo2
        self.blanco = blanco
        self.resultado = {
            "ronda": numero_ronda,
            "equipo1": {"puntaje": 0, "tiros": 0, "puntaje_grupo": 0},
            "equipo2": {"puntaje": 0, "tiros": 0, "puntaje_grupo": 0},
            "ganador_individual": None,
            "ganador_grupal": None,
        }

    def jugar(self):
        self._preparar_jugadores()
        self._jugar_turnos_equipos()
        self._realizar_lanzamiento_grupo()
        self._manejar_lanzamientos_extra_consecutivos()
        self._determinar_ganador_individual()
        self._actualizar_experiencia()
        self._recuperar_resistencia()
        return self.resultado

    def _preparar_jugadores(self):
        for jugador in self.equipo1.jugadores + self.equipo2.jugadores:
            jugador.resistencia_previa = jugador.resistencia_actual
            jugador.resistencia_actual = jugador.resistencia_previa

    def _jugar_turnos_equipos(self):
        self._jugar_turno_equipo(self.equipo1, "equipo1")
        self._jugar_turno_equipo(self.equipo2, "equipo2")

    def _jugar_turno_equipo(self, equipo, clave_equipo):
        for jugador in equipo.jugadores:
            puntaje, tiros = 0, 0
            while jugador.puede_tirar():
                puntaje += self.blanco.realizar_tiro(jugador)
                tiros += 1
            self.resultado[clave_equipo]["puntaje"] += puntaje
            self.resultado[clave_equipo]["tiros"] += tiros
            jugador.puntaje_total += puntaje

    def _realizar_lanzamiento_grupo(self):
        for equipo, clave in [(self.equipo1, "equipo1"), (self.equipo2, "equipo2")]:
            jugador = max(equipo.jugadores, key=lambda j: j.suerte)
            tiro = self.blanco.realizar_tiro(jugador)
            self.resultado[clave]["puntaje_grupo"] += tiro
            equipo.puntaje_total += tiro

    def _manejar_lanzamientos_extra_consecutivos(self):
        for jugador in self.equipo1.jugadores + self.equipo2.jugadores:
            if jugador.consecutivo_extra_ganados >= 3:
                tiro = self.blanco.realizar_tiro(jugador)
                equipo = (
                    self.equipo1 if jugador in self.equipo1.jugadores else self.equipo2
                )
                equipo.puntaje_total += tiro
                self.resultado[equipo.nombre.lower()]["puntaje_grupo"] += tiro
                jugador.consecutivo_extra_ganados = 0

    def _determinar_ganador_individual(self):
        puntaje1 = self.resultado["equipo1"]["puntaje"]
        puntaje2 = self.resultado["equipo2"]["puntaje"]

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
            perdida = 1 if jugador.beneficio_resistencia else random.randint(1, 2)
            jugador.resistencia_actual = jugador.resistencia_previa - perdida
