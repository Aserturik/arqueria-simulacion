import sys
import os
import time
from abc import ABC, abstractmethod
import math
from typing import List, Any, Sequence
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2, norm

# Implementación del generador
class PRNG(ABC):
    @abstractmethod
    def seed(self, value: int) -> None:
        pass
    
    @abstractmethod
    def random(self) -> float:
        pass

class LinearCongruenceRandom(PRNG):
    DEFAULT_M = 2**31 - 1  # Número primo de Mersenne
    DEFAULT_A = 1597
    DEFAULT_C = 51749
    
    def __init__(self, seed_value=None):
        self.m = self.DEFAULT_M
        self.a = self.DEFAULT_A
        self.c = self.DEFAULT_C
        self._x = seed_value if seed_value is not None else int(time.time() * 1000)
    
    def seed(self, value):
        self._x = value % self.m
    
    def random(self):
        self._x = (self.a * self._x + self.c) % self.m
        return self._x / self.m

# Implementación de las pruebas estadísticas
class ChiSquareTest:
    def __init__(self, numbers, intervals=10):
        self.numbers = numbers
        self.intervals = intervals
        self.observed_freq = np.zeros(intervals)
        self.expected_freq = len(numbers) / intervals
        self.chi_square = 0
        self.critical_value = 0
        self.passed = False
        
    def run_test(self):
        # Calcular frecuencias observadas
        for num in self.numbers:
            interval = int(num * self.intervals)
            if interval == self.intervals:  # Maneja el caso del 1.0
                interval -= 1
            self.observed_freq[interval] += 1
            
        # Calcular estadístico chi-cuadrado
        self.chi_square = sum((self.observed_freq - self.expected_freq)**2 / self.expected_freq)
        
        # Calcular valor crítico
        alpha = 0.05  # nivel de significancia
        df = self.intervals - 1  # grados de libertad
        self.critical_value = chi2.ppf(1 - alpha, df)
        
        # Determinar si pasa la prueba
        self.passed = self.chi_square <= self.critical_value

class KolmogorovSmirnovTest:
    def __init__(self, numbers):
        self.numbers = sorted(numbers)
        self.n = len(numbers)
        self.d_max = 0
        self.critical_value = 0
        self.passed = False
        
    def run_test(self):
        for i, x in enumerate(self.numbers):
            # Calcular diferencia máxima entre distribución empírica y teórica
            d1 = (i + 1) / self.n - x
            d2 = x - i / self.n
            self.d_max = max(self.d_max, d1, d2)
            
        # Calcular valor crítico
        alpha = 0.05
        self.critical_value = np.sqrt(-np.log(alpha/2) / (2 * self.n))
        
        # Determinar si pasa la prueba
        self.passed = self.d_max <= self.critical_value

def ejecutar_validaciones(tamano_muestra=10000, semilla=12345):
    """
    Ejecuta pruebas estadísticas para validar la calidad del generador.
    """
    print(f"\nValidación del Generador de Números Pseudoaleatorios")
    print("=" * 50)
    print(f"Tamaño de muestra: {tamano_muestra}")
    print(f"Semilla: {semilla}")
    print("-" * 50)
    
    # Generar números
    rng = LinearCongruenceRandom(seed_value=semilla)
    numeros = [rng.random() for _ in range(tamano_muestra)]
    
    # Prueba Chi-Cuadrado
    print("\n1. Prueba Chi-Cuadrado para Uniformidad:")
    print("-" * 50)
    chi_test = ChiSquareTest(numeros)
    chi_test.run_test()
    print(f"Estadístico Chi-Cuadrado: {chi_test.chi_square:.4f}")
    print(f"Valor crítico: {chi_test.critical_value:.4f}")
    print(f"Resultado: {'APROBADO' if chi_test.passed else 'NO APROBADO'}")
    
    # Prueba Kolmogorov-Smirnov
    print("\n2. Prueba Kolmogorov-Smirnov:")
    print("-" * 50)
    ks_test = KolmogorovSmirnovTest(numeros)
    ks_test.run_test()
    print(f"Estadístico D: {ks_test.d_max:.4f}")
    print(f"Valor crítico: {ks_test.critical_value:.4f}")
    print(f"Resultado: {'APROBADO' if ks_test.passed else 'NO APROBADO'}")
    
    # Análisis de la distribución
    mean = np.mean(numeros)
    std = np.std(numeros)
    print("\n3. Análisis de la Distribución:")
    print("-" * 50)
    print(f"Media: {mean:.6f} (Esperado: 0.5)")
    print(f"Desviación estándar: {std:.6f} (Esperado: {1/math.sqrt(12):.6f})")
    
    # Visualización
    plt.figure(figsize=(12, 4))
    
    # Histograma
    plt.subplot(121)
    plt.hist(numeros, bins=50, density=True, alpha=0.7, color='blue')
    plt.title('Distribución de Números Generados')
    plt.xlabel('Valor')
    plt.ylabel('Densidad')
    plt.grid(True, alpha=0.3)
    
    # QQ Plot
    plt.subplot(122)
    stats = norm()
    osm = np.array([(i - 0.5)/len(numeros) for i in range(1, len(numeros) + 1)])
    theoretical_quantiles = stats.ppf(osm)
    plt.scatter(theoretical_quantiles, np.sort(numeros), alpha=0.5)
    plt.plot([-3, 3], [0, 1], 'r--')
    plt.title('Q-Q Plot')
    plt.xlabel('Cuantiles Teóricos')
    plt.ylabel('Cuantiles Observados')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    ejecutar_validaciones()