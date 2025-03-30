from .jugador import Jugador
import random
import names
import uuid


class Equipo:
    def __init__(self, nombre, num_jugadores=5):
        self.equipo_id = str(uuid.uuid4())
        self.nombre = nombre
        self.jugadores = self._generar_jugadores(num_jugadores)
        self.rondas_ganadas = 0
        self.puntaje_total = 0
        self.puntaje_juego = 0
        self.juegos_ganados = 0
        self.jugadores_por_id = {jugador.user_id: jugador for jugador in self.jugadores}

    def _generar_jugadores(self, num_jugadores):
        if num_jugadores < 2:
            raise ValueError(
                "El equipo debe tener al menos 2 jugadores para garantizar diversidad de género"
            )

        jugadores = []
        # Asegurar al menos un jugador de cada género
        nombre_m = names.get_full_name(gender="male")
        jugadores.append(Jugador(nombre_m, "M"))

        nombre_f = names.get_full_name(gender="female")
        jugadores.append(Jugador(nombre_f, "F"))

        # Para el resto de jugadores, asignar género aleatoriamente
        for _ in range(num_jugadores - 2):
            genero = random.choice(["M", "F"])
            nombre = names.get_full_name(gender="male" if genero == "M" else "female")
            jugadores.append(Jugador(nombre, genero))

        # Mezclar la lista para que el orden sea aleatorio
        random.shuffle(jugadores)
        return jugadores

    def realizar_ronda(self):
        puntaje_ronda = 0
        for jugador in self.jugadores:
            puntaje_ronda += jugador.realizar_tiro()
        self.puntaje_total += puntaje_ronda
        return puntaje_ronda

    def obtener_jugador_por_id(self, user_id):
        """Obtiene un jugador específico por su ID"""
        return self.jugadores_por_id.get(user_id)
