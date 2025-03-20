from .jugador import Jugador
import random
import names

class Equipo:
    def __init__(self, nombre, num_jugadores=5):
        self.nombre = nombre
        self.jugadores = self._generar_jugadores(num_jugadores)
        self.puntaje_total = 0

    def _generar_jugadores(self, num_jugadores):
        jugadores = []
        # Asegurar que haya una mezcla de géneros
        generos = ['M', 'F'] * (num_jugadores // 2 + 1)
        random.shuffle(generos)
        
        for i in range(num_jugadores):
            genero = generos[i]
            nombre = names.get_full_name(gender='male' if genero == 'M' else 'female')
            jugadores.append(Jugador(nombre, genero))
        
        return jugadores

    def realizar_ronda(self):
        puntaje_ronda = 0
        for jugador in self.jugadores:
            puntaje_ronda += jugador.realizar_tiro()
        self.puntaje_total += puntaje_ronda
        return puntaje_ronda

    def obtener_estadisticas(self):
        return {
            'nombre_equipo': self.nombre,
            'puntaje_total': self.puntaje_total,
            'jugadores': [{
                'nombre': j.nombre,
                'genero': j.genero,
                'puntaje': j.puntaje_total,
                'tiros': j.tiros_realizados
            } for j in self.jugadores]
        }