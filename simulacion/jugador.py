import random
import uuid


class Jugador:
    def __init__(self, nombre, genero):
        self.user_id = str(uuid.uuid4())
        self.nombre = nombre
        self.genero = genero  # 'M' o 'F'
        self._generar_habilidades()
        self.rondas_ganadas = 0
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
        # Generamos y guardamos los valores iniciales
        # resistencia: 35 ± 10
        self.resistencia_inicial = random.randint(25, 45)  # 35 ± 10
        self.experiencia_inicial = 10

        # Asignamos los valores actuales
        self.resistencia = self.resistencia_inicial
        self.experiencia = self.experiencia_inicial

    def reiniciar_habilidades(self):
        """Restaura las habilidades a sus valores iniciales"""
        self.resistencia = self.resistencia_inicial - self.cansancio_acumulado
        self.experiencia = self.experiencia_inicial

        # También se actualizan las propiedades relacionadas con la ronda
        self.resistencia_actual = self.resistencia
        self.consecutivo_extra_ganados = 0
        self.beneficio_resistencia = False

    def resetear_jugador(self):
        self.resistencia = self.resistencia_inicial
        self.experiencia = self.experiencia_inicial
        self.cansancio_acumulado = 0

    def finalizar_juego(self):
        """Al final del juego, recupera su resistencia original"""
        self.reiniciar_habilidades()
        self.cansancio_acumulado = 0
        self.tiros_realizados = 0
        self.consecutivo_extra_ganados = 0

    def puede_tirar(self):
        """Verifica si el jugador tiene suficiente resistencia para realizar un tiro"""
        return (
            self.resistencia_actual >= 5
        )  # Mismo valor que Blanco.TIRO_RESISTENCIA_COST

    def actualizar_resistencia(self):
        """Actualiza la resistencia actual del jugador al final de cada tiro"""
        self.resistencia_actual = self.resistencia_inicial - self.cansancio_acumulado

    def finalizar_ronda(self):
        """
        Al final de cada ronda:
        - Se resta el cansancio acumulado más 1-2 unidades adicionales
        - Se actualiza la resistencia actual partiendo de la inicial
        """
        perdida_adicional = random.randint(1, 2)
        self.cansancio_acumulado += perdida_adicional
        self.resistencia = self.resistencia_inicial - self.cansancio_acumulado

        # Actualizamos la resistencia actual para la lógica de la ronda
        self.resistencia_actual = self.resistencia
        print("resistencia al final de la ronda: " + self.resistencia)
        self.experiencia += 1

    def realizar_tiro(self):
        if self.resistencia_actual >= 5:
            self.resistencia_actual -= 5
            self.tiros_realizados += 1
            print("lancé y tengo resistencia " + self.resistencia_actual)
            # Calcula el puntaje basado en resistencia, experiencia y suerte
            return True
        else:
            return False

    def reiniciar_suerte(self):
        """Reinicia la suerte del jugador para cada ronda"""
        self.suerte = round(random.uniform(1.0, 3.0), 2)

    def guardar_puntaje_total(self):
        """Guarda el puntaje total acumulado del jugador"""
        self.puntaje_juego_anterior = self.puntaje_total
