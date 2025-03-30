from uuid import uuid4  # Más específico que importar todo uuid
from modelos.random_wrapper import randint, uniform


class Jugador:
    """
    Representa un jugador en el juego de arquería con sus habilidades y estadísticas.
    Maneja la lógica de tiros, resistencia, experiencia y suerte del jugador.
    """

    def __init__(self, nombre, genero):
        """
        Inicializa un nuevo jugador con sus atributos base.

        Args:
            nombre (str): Nombre del jugador
            genero (str): Género del jugador ('M' o 'F')

        Atributos:
            user_id (str): Identificador único del jugador
            resistencia (int): Capacidad física del jugador (25-45)
            experiencia (int): Puntos de experiencia acumulados
            suerte (float): Factor de suerte que afecta la precisión (1.0-3.0)
            cansancio_acumulado (int): Pérdida de resistencia acumulada
            beneficio_resistencia (bool): Indica si el jugador tiene beneficio de resistencia
        """
        self.user_id = str(uuid4())
        self.nombre = nombre
        self.genero = genero  # 'M' o 'F'
        self._generar_habilidades()
        self.suerte = 0
        self.puntaje_total = 0
        self.puntaje_juego_anterior = 0
        self.puntaje_juego_actual = 0
        self.puntje_ronda_actual = 0
        self.cansancio_acumulado = 0
        self.tiros_realizados = 0

        # Relaciones requeridas por la lógica de Ronda
        self.resistencia_actual = self.resistencia  # Valor actual de resistencia
        self.consecutivo_extra_ganados = 0  # Conteo de tiros extra consecutivos ganados
        self.beneficio_resistencia = (
            False  # Beneficio que puede mejorar la recuperación
        )

    def _generar_habilidades(self):
        """
        Genera las habilidades iniciales del jugador.
        
        Efectos:
            - Establece la resistencia inicial (35 ± 10)
            - Establece la experiencia inicial (10)
            - Inicializa el contador de rondas con beneficio
        """
        # Generamos y guardamos los valores iniciales
        # resistencia: 35 ± 10
        self.resistencia_inicial = randint(25, 45)  # 35 ± 10
        self.experiencia_inicial = 10
        self.rondas_con_beneficio = 0

        # Asignamos los valores actuales
        self.resistencia = self.resistencia_inicial
        self.experiencia = self.experiencia_inicial

    def reiniciar_habilidades(self):
        """
        Restaura las habilidades a sus valores iniciales, considerando el cansancio acumulado.
        
        Efectos:
            - Restaura la resistencia considerando el cansancio acumulado
            - Restaura la experiencia a su valor inicial
            - Reinicia los contadores de beneficios y tiros extra
        """
        self.resistencia = self.resistencia_inicial - self.cansancio_acumulado
        self.experiencia = self.experiencia_inicial

        # También se actualizan las propiedades relacionadas con la ronda
        self.resistencia_actual = self.resistencia
        self.consecutivo_extra_ganados = 0
        self.beneficio_resistencia = False

    def resetear_jugador(self):
        """
        Reinicia completamente el estado del jugador.
        
        Efectos:
            - Restaura la resistencia a su valor inicial
            - Restaura la experiencia a su valor inicial
            - Elimina todo el cansancio acumulado
        """
        self.resistencia = self.resistencia_inicial
        self.experiencia = self.experiencia_inicial
        self.cansancio_acumulado = 0

    def finalizar_juego(self):
        """
        Reinicia el estado del jugador al finalizar un juego completo.
        
        Efectos:
            - Reinicia todas las habilidades
            - Elimina el cansancio acumulado
            - Reinicia contadores de tiros y beneficios
            - Restaura la experiencia al valor base
        """
        self.reiniciar_habilidades()
        self.cansancio_acumulado = 0
        self.tiros_realizados = 0
        self.consecutivo_extra_ganados = 0
        self.beneficio_resistencia = False
        self.experiencia = 10

    def puede_tirar(self):
        """
        Verifica si el jugador tiene suficiente resistencia para realizar un tiro.
        
        Returns:
            bool: True si el jugador tiene al menos 5 puntos de resistencia, False en caso contrario
        """
        return (
            self.resistencia_actual >= 5
        )  # Mismo valor que Blanco.TIRO_RESISTENCIA_COST

    def actualizar_resistencia(self):
        """
        Actualiza la resistencia actual del jugador después de cada tiro.
        
        Lógica:
            - Si tiene beneficio de resistencia y 19+ puntos de experiencia:
                Solo pierde 1 punto de resistencia
            - En caso contrario:
                Pierde resistencia normal según el cansancio acumulado
        """
        # Si el jugador tiene 19+ puntos de experiencia, pierde menos resistencia
        if self.experiencia >= 19 and self.beneficio_resistencia:
            # Solo pierde 1 punto en lugar de la pérdida normal
            self.resistencia_actual = self.resistencia_inicial - max(
                1, self.cansancio_acumulado - 1
            )
        else:
            self.resistencia_actual = (
                self.resistencia_inicial - self.cansancio_acumulado
            )

    def finalizar_ronda(self):
        """
        Actualiza el estado del jugador al final de una ronda.
        
        Efectos:
            - Incrementa el cansancio acumulado en 1-2 unidades
            - Actualiza la resistencia según el cansancio
            - Incrementa la experiencia en 1 punto
        """
        perdida_adicional = randint(1, 2)  # Usar nuestro generador en lugar de random
        self.cansancio_acumulado += perdida_adicional
        self.resistencia = self.resistencia_inicial - self.cansancio_acumulado

        # Actualizamos la resistencia actual para la lógica de la ronda
        self.resistencia_actual = self.resistencia
        self.experiencia += 1

    def realizar_tiro(self):
        """
        Ejecuta un tiro si el jugador tiene suficiente resistencia.
        
        Returns:
            bool: True si el tiro fue realizado, False si no había suficiente resistencia
            
        Efectos:
            - Reduce la resistencia en 5 puntos
            - Incrementa el contador de tiros realizados
        """
        if self.resistencia_actual >= 5:
            self.resistencia_actual -= 5
            self.tiros_realizados += 1
            # Calcula el puntaje basado en resistencia, experiencia y suerte
            return True
        else:
            return False

    def reiniciar_suerte(self):
        """
        Genera un nuevo valor de suerte para el jugador en cada ronda.
        
        Efectos:
            - Asigna un valor aleatorio de suerte entre 1.0 y 3.0
        """
        self.suerte = round(uniform(1.0, 3.0), 2)

    def guardar_puntaje_total(self):
        """
        Almacena el puntaje total actual como puntaje del juego anterior.
        
        Efectos:
            - Guarda el puntaje total actual antes de comenzar un nuevo juego
        """
        self.puntaje_juego_anterior = self.puntaje_total
