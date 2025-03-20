class Ronda:
    def __init__(self, numero_ronda):
        self.numero = numero_ronda
        self.puntajes_equipos = {}
        self.finalizada = False

    def registrar_puntaje(self, equipo, puntaje):
        self.puntajes_equipos[equipo.nombre] = puntaje

    def obtener_ganador(self):
        if not self.puntajes_equipos:
            return None
        
        max_puntaje = max(self.puntajes_equipos.values())
        ganadores = [equipo for equipo, puntaje in self.puntajes_equipos.items() 
                    if puntaje == max_puntaje]
        
        return ganadores[0] if len(ganadores) == 1 else "Empate"

    def finalizar(self):
        self.finalizada = True

    def obtener_resumen(self):
        return {
            'numero_ronda': self.numero,
            'puntajes': self.puntajes_equipos,
            'ganador': self.obtener_ganador(),
            'finalizada': self.finalizada
        }