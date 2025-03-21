import random
import uuid

class Jugador:
    def __init__(self, nombre, genero):
        self.user_id = str(uuid.uuid4())  # Genera un ID único
        self.nombre = nombre
        self.genero = genero  # 'M' o 'F'
        self._generar_habilidades()
        self.puntaje_total = 0
        self.tiros_realizados = []
        
    def _generar_habilidades(self):
        self.resistencia = random.randint(25, 45)  # 35 ± 10
        self.experiencia = 10
        self.suerte = round(random.uniform(1.0, 3.0), 2)
