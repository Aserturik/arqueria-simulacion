import random

class Jugador:
    def __init__(self, nombre, genero):
        self.nombre = nombre
        self.genero = genero  # 'M' o 'F'
        self._generar_habilidades()
        self.puntaje_total = 0
        self.tiros_realizados = []

    def _generar_habilidades(self):
        self.resistencia = random.randint(25, 45)  # 35 ± 10
        self.experiencia = 10
        self.suerte = round(random.uniform(1.0, 3.0), 2)

    def realizar_tiro(self):
        # Fórmula para calcular la puntuación del tiro
        factor_cansancio = max(0.7, 1 - (len(self.tiros_realizados) * 0.1))
        precision_base = (self.resistencia * 0.4 + 
                         self.experiencia * 0.4 + 
                         self.suerte * 0.2)
        
        # Añadir algo de aleatoriedad al tiro
        variacion = random.uniform(-5, 5)
        puntuacion = precision_base * factor_cansancio + variacion
        
        # Limitar la puntuación entre 0 y 10
        puntuacion = max(0, min(10, puntuacion))
        
        self.tiros_realizados.append(puntuacion)
        self.puntaje_total += puntuacion
        return puntuacion

    def __str__(self):
        return f"{self.nombre} ({self.genero}) - R:{self.resistencia} E:{self.experiencia} S:{self.suerte}"