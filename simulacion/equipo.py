from .jugador import Jugador
import names
import uuid
from modelos.random_wrapper import choice, shuffle

class Equipo:
    """
    Representa un equipo en el juego de arquería.
    Gestiona un grupo de jugadores y mantiene las estadísticas del equipo.
    """

    def __init__(self, nombre, num_jugadores=5):
        """
        Inicializa un nuevo equipo con sus jugadores.

        Args:
            nombre (str): Nombre identificador del equipo
            num_jugadores (int): Número de jugadores en el equipo (mínimo 2)

        Atributos:
            equipo_id (str): Identificador único del equipo
            jugadores (List[Jugador]): Lista de jugadores del equipo
            rondas_ganadas (int): Contador de rondas ganadas
            puntaje_total (int): Suma total de puntos del equipo
            puntaje_juego (int): Puntos acumulados en el juego actual
            juegos_ganados (int): Número total de juegos ganados
        """
        self.equipo_id = str(uuid.uuid4())
        self.nombre = nombre
        self.jugadores = self._generar_jugadores(num_jugadores)
        self.rondas_ganadas = 0
        self.puntaje_total = 0
        self.puntaje_juego = 0
        self.juegos_ganados = 0
        self.jugadores_por_id = {jugador.user_id: jugador for jugador in self.jugadores}

    def _generar_jugadores(self, num_jugadores):
        """
        Genera la lista inicial de jugadores del equipo.

        Args:
            num_jugadores (int): Cantidad de jugadores a generar

        Returns:
            List[Jugador]: Lista de jugadores generados

        Raises:
            ValueError: Si num_jugadores es menor a 2

        Proceso:
            1. Asegura al menos un jugador de cada género
            2. Genera el resto de jugadores con género aleatorio
            3. Aleatoriza el orden final de los jugadores
        """
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
            genero = choice(["M", "F"])
            nombre = names.get_full_name(gender="male" if genero == "M" else "female")
            jugadores.append(Jugador(nombre, genero))

        # Mezclar la lista para que el orden sea aleatorio
        shuffle(jugadores)
        return jugadores

    def realizar_ronda(self):
        """
        Ejecuta una ronda de tiros para todo el equipo.

        Returns:
            int: Puntaje total obtenido por el equipo en la ronda

        Efectos:
            - Cada jugador realiza sus tiros
            - Se actualiza el puntaje total del equipo
        """
        puntaje_ronda = 0
        for jugador in self.jugadores:
            puntaje_ronda += jugador.realizar_tiro()
        self.puntaje_total += puntaje_ronda
        return puntaje_ronda

    def obtener_jugador_por_id(self, user_id):
        """
        Obtiene un jugador específico por su ID.

        Args:
            user_id (str): Identificador único del jugador

        Returns:
            Jugador: El jugador encontrado o None si no existe
        """
        return self.jugadores_por_id.get(user_id)
