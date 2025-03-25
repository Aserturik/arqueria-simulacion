from simulacion.juego import Juego

# Ejecutar la simulación
if __name__ == "__main__":
    juego = Juego(
        "Arqueros del Norte", "Arqueras del Sur", num_jugadores=5, num_rondas=10
    )
    juego.jugar_partida_completa()
