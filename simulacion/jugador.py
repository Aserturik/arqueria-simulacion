import random
import uuid


class Jugador:
    def __init__(self, nombre, genero):
        self.user_id = str(uuid.uuid4())
        self.nombre = nombre
        self.genero = genero  # 'M' o 'F'
        self._generar_habilidades()
        self.rondas_ganadas = 0
        self.puntaje_total = 0
        self.cansancio_acumulado = 0
        self.tiros_realizados = 0

        # Relaciones requeridas por la lógica de Ronda
        self.resistencia_actual = self.resistencia          # Valor actual de resistencia
        self.resistencia_previa = self.resistencia          # Para almacenar la resistencia antes del turno
        self.consecutivo_extra_ganados = 0                  # Conteo de tiros extra consecutivos ganados
        self.punteria = random.randint(50, 100)             # Valor de puntería para desempates
        self.beneficio_resistencia = False                  # Beneficio que puede mejorar la recuperación

    def _generar_habilidades(self):
        # Generamos y guardamos los valores iniciales
        self.resistencia_inicial = random.randint(25, 45)  # 35 ± 10
        self.experiencia_inicial = 10
        self.suerte_inicial = round(random.uniform(1.0, 3.0), 2)

        # Asignamos los valores actuales
        self.resistencia = self.resistencia_inicial
        self.experiencia = self.experiencia_inicial
        self.suerte = self.suerte_inicial

    def reiniciar_habilidades(self):
        """Restaura las habilidades a sus valores iniciales"""
        self.resistencia = self.resistencia_inicial
        self.experiencia = self.experiencia_inicial
        self.suerte = self.suerte_inicial

        # También se actualizan las propiedades relacionadas con la ronda
        self.resistencia_actual = self.resistencia
        self.resistencia_previa = self.resistencia
        self.consecutivo_extra_ganados = 0
        self.beneficio_resistencia = False

    def finalizar_juego(self):
        """Al final del juego, recupera su resistencia original"""
        self.reiniciar_habilidades()
        self.cansancio_acumulado = 0

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
        self.experiencia += 1

    def realizar_tiro(self):
        if self.resistencia_actual >= 5:
            self.resistencia_actual -= 5
            self.tiros_realizados += 1
            # Calcula el puntaje basado en resistencia, experiencia y suerte
            return True
        else:
            return False
