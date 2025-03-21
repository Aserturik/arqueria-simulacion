from .jugador import Jugador
import random
import names


class Equipo:
    def __init__(self, nombre, genero, num_jugadores=5):
        self.nombre = nombre
        self.genero = genero.upper()  # 'M' o 'F'
        if self.genero not in ["M", "F"]:
            raise ValueError("El género debe ser 'M' o 'F'")
        self.jugadores = self._generar_jugadores(num_jugadores)
        self.puntaje_total = 0
        self.jugadores_por_id = {jugador.user_id: jugador for jugador in self.jugadores}

    def _generar_jugadores(self, num_jugadores):
        jugadores = []
        for _ in range(num_jugadores):
            nombre = names.get_full_name(
                gender="male" if self.genero == "M" else "female"
            )
            jugadores.append(Jugador(nombre, self.genero))
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

    def obtener_estadisticas(self):
        return {
            "nombre_equipo": self.nombre,
            "puntaje_total": self.puntaje_total,
            "jugadores": [
                {
                    "id": j.user_id,  # Agregamos el ID en las estadísticas
                    "nombre": j.nombre,
                    "genero": j.genero,
                    "puntaje": j.puntaje_total,
                    "tiros": j.tiros_realizados,
                }
                for j in self.jugadores
            ],
        }


# ...existing code...

if __name__ == "__main__":
    # Crear equipo masculino
    equipo_m = Equipo("Arqueros del Norte", "M", 5)
    print(f"\nEquipo Masculino: {equipo_m.nombre}")
    for jugador in equipo_m.jugadores:
        print(f"- {jugador.nombre} (ID: {jugador.user_id})")

    # Crear equipo femenino
    equipo_f = Equipo("Arqueras del Sur", "F", 5)
    print(f"\nEquipo Femenino: {equipo_f.nombre}")
    for jugador in equipo_f.jugadores:
        print(f"- {jugador.nombre} (ID: {jugador.user_id})")

    # Probar búsqueda por ID
    id_ejemplo = equipo_m.jugadores[0].user_id
    jugador = equipo_m.obtener_jugador_por_id(id_ejemplo)
    print(f"\nBúsqueda por ID {id_ejemplo}: {jugador.nombre}")
