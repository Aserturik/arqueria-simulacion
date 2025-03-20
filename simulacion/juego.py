from ..modelos.equipo import Equipo
from .ronda import Ronda

class Juego:
    def __init__(self, num_rondas=3):
        self.equipo1 = Equipo("Equipo 1")
        self.equipo2 = Equipo("Equipo 2")
        self.num_rondas = num_rondas
        self.rondas = []
        self.ganador = None

    def simular(self):
        for i in range(self.num_rondas):
            ronda = Ronda(i + 1)
            
            # Realizar tiros para ambos equipos
            puntaje_equipo1 = self.equipo1.realizar_ronda()
            puntaje_equipo2 = self.equipo2.realizar_ronda()
            
            # Registrar puntajes
            ronda.registrar_puntaje(self.equipo1, puntaje_equipo1)
            ronda.registrar_puntaje(self.equipo2, puntaje_equipo2)
            
            ronda.finalizar()
            self.rondas.append(ronda)

        self._determinar_ganador()
        return self.obtener_resultados()

    def _determinar_ganador(self):
        if self.equipo1.puntaje_total > self.equipo2.puntaje_total:
            self.ganador = self.equipo1.nombre
        elif self.equipo2.puntaje_total > self.equipo1.puntaje_total:
            self.ganador = self.equipo2.nombre
        else:
            self.ganador = "Empate"

    def obtener_resultados(self):
        return {
            'rondas': [ronda.obtener_resumen() for ronda in self.rondas],
            'equipo1': self.equipo1.obtener_estadisticas(),
            'equipo2': self.equipo2.obtener_estadisticas(),
            'ganador_final': self.ganador
        }