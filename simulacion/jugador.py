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

    def finalizar_juego(self):
        """Al final del juego, recupera su resistencia original"""
        self.reiniciar_habilidades()
        self.cansancio_acumulado = 0

    def finalizar_ronda(self):
        """
        Al filana de cada ronda:
        - El arquiero recupera su resistencia original
        - Se resta el cansancio acumulado más 1-2 unidades adicionales
        """
        perdida_adicional = random.randint(1, 2)
        self.cansancio_acumulado += perdida_adicional
        self.resistencia = self.resistencia_inicial - self.cansancio_acumulado
        self.experiencia += 1

    def realizar_tiro(self):
        if self.resistencia >= 5:
            self.resistencia -= 5
            # Calcula el puntaje basado en resistencia, experiencia y suerte
            puntaje = random.randint(1, 10)
            return puntaje
        else:
            raise ValueError("Resistencia insuficiente para realizar el tiro")
