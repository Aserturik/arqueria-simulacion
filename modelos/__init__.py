"""
Paquete de modelos para simulación de arquería.

Este paquete contiene:
- PRNG: Generador de números pseudoaleatorios base
- Pruebas estadísticas:
  - AverageTest: Prueba de promedios
  - KsTest: Prueba de Kolmogorov-Smirnov
  - PokerTest: Prueba de Poker
  - ChiSquareTest: Prueba de Chi Cuadrado
  - VarianceTest: Prueba de Varianza
"""

from .prng import PRNG
from .pruebas.average_test import AverageTest
from .pruebas.ks_test import KsTest
from .pruebas.poker_test import PokerTest
from .pruebas.chi_square_test import ChiSquareTest
from .pruebas.variance_test import VarianceTest

__all__ = ['PRNG', 'AverageTest', 'KsTest', 'PokerTest', 'ChiSquareTest', 'VarianceTest']