from simulacion.equipo import Equipo
from simulacion.jugador import Jugador
from simulacion.blanco_objetivo import Blanco
import matplotlib.pyplot as plt
import uuid


class Juego:
    def __init__(self, nombre_equipo1, nombre_equipo2, num_jugadores=5, num_rondas=3):
        self.id_juego = str(uuid.uuid4())
        self.equipo1 = Equipo(nombre_equipo1, "M", num_jugadores)
        self.equipo2 = Equipo(nombre_equipo2, "F", num_jugadores)
        self.blanco = Blanco()
        self.num_rondas = num_rondas
        self.ronda_actual = 0
        self.historial_puntajes = []

    def jugar_ronda(self):
        """Simula una ronda completa del juego"""
        self.ronda_actual += 1
        print(f"\n--- RONDA {self.ronda_actual} ---")

        # Resultados de la ronda
        resultado_ronda = {
            "ronda": self.ronda_actual,
            "equipo1": {"puntaje": 0, "tiros": 0},
            "equipo2": {"puntaje": 0, "tiros": 0},
        }

        # Equipo 1 juega
        print(f"\nEquipo {self.equipo1.nombre} (Masculino):")
        for i, jugador in enumerate(self.equipo1.jugadores):
            print(f"  Debug - Procesando jugador: {jugador.nombre}")
            print(f"  Debug - Resistencia inicial: {jugador.resistencia}")
            puntaje_jugador = 0
            tiros_realizados = 0

            print(f"  {jugador.nombre} - ", end="")
            while jugador.resistencia >= 5:
                try:
                    print(f"Debug - Intento tiro, resistencia: {jugador.resistencia}")
                    puntaje = self.blanco.realizar_tiro(jugador)
                    print(f"Debug - Puntaje obtenido: {puntaje}")
                    puntaje_jugador += puntaje
                    tiros_realizados += 1
                    print(f"Debug - Resistencia después: {jugador.resistencia}")
                except Exception as e:
                    print(f"ERROR: {str(e)}")
                    break

        # Equipo 2 juega
        print(f"\nEquipo {self.equipo2.nombre} (Femenino):")
        for i, jugador in enumerate(self.equipo2.jugadores):
            puntaje_jugador = 0
            tiros_realizados = 0

            print(f"  {jugador.nombre} - ", end="")
            while jugador.resistencia >= 5:
                puntaje = self.blanco.realizar_tiro(jugador)
                puntaje_jugador += puntaje
                tiros_realizados += 1

            print(f"Puntaje: {puntaje_jugador} ({tiros_realizados} tiros)")
            jugador.puntaje_total += puntaje_jugador
            resultado_ronda["equipo2"]["puntaje"] += puntaje_jugador
            resultado_ronda["equipo2"]["tiros"] += tiros_realizados
            jugador.finalizar_ronda()

        # Determinar ganador de la ronda
        if (
            resultado_ronda["equipo1"]["puntaje"]
            > resultado_ronda["equipo2"]["puntaje"]
        ):
            ganador = self.equipo1.nombre
            self.equipo1.rondas_ganadas += 1
        elif (
            resultado_ronda["equipo2"]["puntaje"]
            > resultado_ronda["equipo1"]["puntaje"]
        ):
            ganador = self.equipo2.nombre
            self.equipo2.rondas_ganadas += 1
        else:
            ganador = "Empate"

        resultado_ronda["ganador"] = ganador
        self.historial_puntajes.append(resultado_ronda)

        print(f"\nResultado Ronda {self.ronda_actual}:")
        print(
            f"  {self.equipo1.nombre}: {resultado_ronda['equipo1']['puntaje']} puntos"
        )
        print(
            f"  {self.equipo2.nombre}: {resultado_ronda['equipo2']['puntaje']} puntos"
        )
        print(f"  Ganador: {ganador}")

        return resultado_ronda

    def jugar_partida_completa(self):
        """Juega una partida completa con todas las rondas"""
        print(f"¡COMIENZA EL JUEGO DE ARQUERÍA!")
        print(f"Equipo 1: {self.equipo1.nombre} (M)")
        print(f"Equipo 2: {self.equipo2.nombre} (F)")
        print(f"Rondas: {self.num_rondas}")

        for _ in range(self.num_rondas):
            self.jugar_ronda()

        # Determinar ganador final
        if self.equipo1.rondas_ganadas > self.equipo2.rondas_ganadas:
            ganador_final = self.equipo1.nombre
            self.equipo1.juegos_ganados += 1
        elif self.equipo2.rondas_ganadas > self.equipo1.rondas_ganadas:
            ganador_final = self.equipo2.nombre
            self.equipo2.juegos_ganados += 1
        else:
            ganador_final = "Empate"

        print("\n--- RESULTADO FINAL ---")
        print(f"  {self.equipo1.nombre}: {self.equipo1.rondas_ganadas} rondas ganadas")
        print(f"  {self.equipo2.nombre}: {self.equipo2.rondas_ganadas} rondas ganadas")
        print(f"  ¡{ganador_final} gana el juego!")

        # Visualizar el resultado
        self.visualizar_resultados()

        # Reiniciar jugadores para próximo juego
        for jugador in self.equipo1.jugadores + self.equipo2.jugadores:
            jugador.finalizar_juego()

    def visualizar_resultados(self):
        """Muestra gráficos con los resultados del juego"""
        # Visualizar el blanco con todos los tiros
        self.blanco.visualizar_tiros()

        # Gráfico de puntajes por ronda
        rondas = [r["ronda"] for r in self.historial_puntajes]
        puntajes_eq1 = [r["equipo1"]["puntaje"] for r in self.historial_puntajes]
        puntajes_eq2 = [r["equipo2"]["puntaje"] for r in self.historial_puntajes]

        plt.figure(figsize=(10, 6))
        plt.plot(rondas, puntajes_eq1, "o-", label=self.equipo1.nombre)
        plt.plot(rondas, puntajes_eq2, "o-", label=self.equipo2.nombre)
        plt.xlabel("Ronda")
        plt.ylabel("Puntaje")
        plt.title("Evolución de puntajes por ronda")
        plt.legend()
        plt.grid(True)
        plt.show()


# Ejecutar la simulación
if __name__ == "__main__":
    juego = Juego(
        "Arqueros del Norte", "Arqueras del Sur", num_jugadores=5, num_rondas=1
    )
    juego.jugar_partida_completa()
