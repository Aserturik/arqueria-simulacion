from typing import Optional
import time
from .prng import PRNG

class LinearCongruenceRandom(PRNG):
    """
    Implementación del Generador de Números Pseudoaleatorios por Congruencia Lineal.
    
    Utiliza la fórmula: X_(n+1) = (a * X_n + c) mod m
    donde:
        m = módulo (debe ser un número primo grande)
        a = multiplicador (debe cumplir ciertas condiciones)
        c = incremento
        X_0 = semilla inicial
    """
    
    # Valores por defecto optimizados para máximo período
    DEFAULT_M = 2**31 - 1  # Número primo de Mersenne
    DEFAULT_A = 1597
    DEFAULT_C = 51749
    
    def __init__(self, seed_value: Optional[int] = None):
        """
        Inicializa el generador con parámetros optimizados.
        
        Args:
            seed_value: Semilla inicial. Si es None, usa el timestamp actual.
        """
        self.m = self.DEFAULT_M
        self.a = self.DEFAULT_A
        self.c = self.DEFAULT_C
        self._x = seed_value if seed_value is not None else int(time.time() * 1000)
        self._validate_parameters()

    def _validate_parameters(self) -> None:
        """Valida que los parámetros cumplan las condiciones necesarias."""
        if self.m <= 0:
            raise ValueError("El módulo m debe ser positivo")
        if self.a <= 0:
            raise ValueError("El multiplicador a debe ser positivo")
        if self.c < 0:
            raise ValueError("El incremento c debe ser no negativo")
        if self.a >= self.m:
            raise ValueError("El multiplicador a debe ser menor que m")
        if self.c >= self.m:
            raise ValueError("El incremento c debe ser menor que m")

    def seed(self, value: int) -> None:
        """Establece una nueva semilla para el generador."""
        self._x = value % self.m

    def random(self) -> float:
        """
        Genera un número pseudoaleatorio en el rango [0.0, 1.0).
        
        Returns:
            float: Número pseudoaleatorio normalizado.
        """
        self._x = (self.a * self._x + self.c) % self.m
        return self._x / self.m
