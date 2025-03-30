"""
Módulo que implementa la prueba de Chi Cuadrado para validar secuencias de números aleatorios.

La prueba Chi Cuadrado evalúa la uniformidad de la distribución de números
comparando las frecuencias observadas con las esperadas.

Descripción detallada:
- Propósito: Validar la hipótesis de uniformidad en una secuencia de números aleatorios
- Funcionamiento: Divide el rango de números en intervalos y compara frecuencias
- Hipótesis nula (H0): Los números siguen una distribución uniforme
- Hipótesis alternativa (H1): Los números no siguen una distribución uniforme
- Nivel de significancia predeterminado: 0.05 (5%)

Parámetros de entrada:
- Lista de números a evaluar
- Número de intervalos (opcional, default=10)

Resultados:
- Estadístico chi cuadrado calculado
- Valor crítico para el nivel de significancia
- Decisión de la prueba (passed)
- Gráficos comparativos

Relaciones:
- Consume números generados por implementaciones de PRNG
- Complementa otras pruebas de uniformidad como KsTest
"""

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from typing import List, Optional

class ChiSquareTest:
    """
    Implementa la prueba estadística Chi Cuadrado para evaluar uniformidad.

    Atributos:
        numbers (List[float]): Secuencia de números a evaluar
        n_intervals (int): Número de intervalos para la prueba
        n (int): Cantidad total de números
        intervals (List[tuple]): Lista de tuplas con los límites de cada intervalo
        observed_freq (List[int]): Frecuencias observadas en cada intervalo
        expected_freq (float): Frecuencia esperada para cada intervalo
        chi_square (float): Estadístico chi cuadrado calculado
        critical_value (float): Valor crítico de la distribución chi cuadrado
        alpha (float): Nivel de significancia de la prueba
        passed (bool): Resultado de la prueba
    """
    def __init__(self, numbers: List[float], n_intervals: int = 10):
        self.numbers = numbers
        self.n = len(numbers)
        self.n_intervals = n_intervals
        self.intervals = []
        self.observed_freq = []
        self.expected_freq = self.n / self.n_intervals
        self.chi_square = 0.0
        self.critical_value = 0.0
        self.alpha = 0.05
        self.passed = False

    def calculate_intervals(self):
        """
        Calcula los intervalos para la prueba.

        Divide el rango de números en n_intervals intervalos de igual tamaño.
        Cada intervalo se almacena como una tupla (límite_inferior, límite_superior).
        """
        min_val = min(self.numbers)
        max_val = max(self.numbers)
        interval_size = (max_val - min_val) / self.n_intervals
        for i in range(self.n_intervals):
            lower = min_val + i * interval_size
            upper = lower + interval_size
            self.intervals.append((lower, upper))

    def calculate_frequencies(self):
        """
        Calcula las frecuencias observadas en cada intervalo.

        Recorre la lista de números y cuenta cuántos caen en cada intervalo.
        El último intervalo incluye su límite superior para incluir el valor máximo.
        """
        self.observed_freq = [0] * self.n_intervals
        for num in self.numbers:
            for i, (lower, upper) in enumerate(self.intervals):
                if lower <= num < upper or (i == self.n_intervals - 1 and num == upper):
                    self.observed_freq[i] += 1
                    break

    def calculate_chi_square(self):
        """
        Calcula el estadístico chi cuadrado.

        Utiliza la fórmula: Σ((O - E)²/E) donde:
        O: Frecuencia observada
        E: Frecuencia esperada
        """
        self.chi_square = sum(
            ((observed - self.expected_freq) ** 2) / self.expected_freq
            for observed in self.observed_freq
        )

    def calculate_critical_value(self):
        """
        Calcula el valor crítico de chi cuadrado.

        Utiliza la distribución chi cuadrado con (n_intervals - 1) grados de libertad
        y el nivel de significancia alpha para determinar el valor crítico.
        """
        df = self.n_intervals - 1
        self.critical_value = stats.chi2.ppf(1 - self.alpha, df)

    def evaluate_test(self):
        """
        Ejecuta la prueba completa de Chi Cuadrado.

        Proceso:
        1. Calcula los intervalos
        2. Determina las frecuencias observadas
        3. Calcula el estadístico chi cuadrado
        4. Obtiene el valor crítico
        5. Compara y determina si la prueba es exitosa
        """
        self.calculate_intervals()
        self.calculate_frequencies()
        self.calculate_chi_square()
        self.calculate_critical_value()
        self.passed = self.chi_square <= self.critical_value

    def plot_results(self):
        """
        Genera un gráfico comparando chi cuadrado calculado vs crítico.

        Visualización:
        - Gráfico de barras
        - Barra azul: Chi cuadrado calculado
        - Barra roja: Valor crítico
        - Valores numéricos sobre cada barra
        """
        labels = ['Chi Cuadrado\nCalculado', 'Valor Crítico']
        values = [self.chi_square, self.critical_value]
        colors = ['blue', 'red']
        
        fig, ax = plt.subplots()
        bars = plt.bar(labels, values, color=colors)
        plt.title('Comparación Chi Cuadrado vs Valor Crítico')
        plt.ylabel('Valor')
        
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:.4f}', ha='center', va='bottom')
        
        plt.show()

    def plot_frequencies(self):
        """
        Genera un gráfico de frecuencias observadas vs esperadas.

        Visualización:
        - Gráfico de barras agrupadas
        - Frecuencias observadas en un color
        - Frecuencias esperadas en otro color
        - Leyenda para identificar cada tipo
        """
        x = range(self.n_intervals)
        observed = self.observed_freq
        expected = [self.expected_freq] * self.n_intervals

        fig, ax = plt.subplots()
        width = 0.35
        ax.bar([i - width/2 for i in x], observed, width, label='Observada')
        ax.bar([i + width/2 for i in x], expected, width, label='Esperada')

        plt.xlabel('Intervalo')
        plt.ylabel('Frecuencia')
        plt.title('Frecuencias Observadas vs Esperadas')
        plt.legend()
        plt.show()

if __name__ == "__main__":
    # Ejemplo de uso
    numbers_input = input("Ingresa los números Ri separados por comas: ")
    try:
        numbers = [float(x.strip()) for x in numbers_input.split(",")]
        test = ChiSquareTest(numbers)
        test.evaluate_test()
        
        print(f"\nEstadístico Chi Cuadrado: {test.chi_square:.4f}")
        print(f"Valor Crítico: {test.critical_value:.4f}")
        print(f"¿Prueba superada?: {test.passed}")
        
        test.plot_results()
        test.plot_frequencies()
    except ValueError:
        print("Error: Asegúrate de ingresar solo números separados por comas.")
