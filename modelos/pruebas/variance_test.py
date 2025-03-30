"""
Módulo que implementa la prueba de Varianza para validar secuencias de números aleatorios.

La prueba de Varianza verifica que la dispersión de los números generados
se ajuste a lo esperado para una distribución uniforme.

Relaciones:
- Consume números generados por implementaciones de PRNG
- Complementa la prueba de promedios (AverageTest)
"""

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from typing import List, Optional

class VarianceTest:
    def __init__(self, numbers: List[float]):
        self.numbers = numbers
        self.n = len(numbers)
        self.variance = 0.0
        self.theoretical_variance = 1/12  # Varianza teórica para distribución uniforme [0,1]
        self.lower_limit = 0.0
        self.upper_limit = 0.0
        self.alpha = 0.05
        self.passed = False

    def calculate_variance(self):
        """Calcula la varianza muestral."""
        self.variance = np.var(self.numbers)

    def calculate_limits(self):
        """Calcula los límites de aceptación usando chi cuadrado."""
        df = self.n - 1
        chi_lower = stats.chi2.ppf(self.alpha/2, df)
        chi_upper = stats.chi2.ppf(1 - self.alpha/2, df)
        
        self.lower_limit = (chi_lower / df) * self.theoretical_variance
        self.upper_limit = (chi_upper / df) * self.theoretical_variance

    def evaluate_test(self):
        """Ejecuta la prueba completa."""
        self.calculate_variance()
        self.calculate_limits()
        self.passed = self.lower_limit <= self.variance <= self.upper_limit

    def plot_results(self):
        """Genera un gráfico comparando la varianza con sus límites."""
        labels = ['Límite\nInferior', 'Varianza\nCalculada', 'Límite\nSuperior']
        values = [self.lower_limit, self.variance, self.upper_limit]
        colors = ['red', 'blue', 'red']
        
        fig, ax = plt.subplots()
        bars = plt.bar(labels, values, color=colors)
        plt.title('Comparación de Varianza con Límites de Aceptación')
        plt.ylabel('Valor')
        
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:.6f}', ha='center', va='bottom')
        
        plt.show()

    def plot_distribution(self):
        """Genera un histograma de los números con la distribución teórica."""
        plt.figure(figsize=(10, 6))
        plt.hist(self.numbers, bins=30, density=True, alpha=0.7, color='blue',
                label='Distribución Observada')
        
        # Agregar línea de distribución uniforme teórica
        plt.axhline(y=1, color='r', linestyle='--', label='Distribución Teórica')
        
        plt.title('Distribución de Números Generados')
        plt.xlabel('Valor')
        plt.ylabel('Densidad')
        plt.legend()
        plt.show()

if __name__ == "__main__":
    # Ejemplo de uso
    numbers_input = input("Ingresa los números Ri separados por comas: ")
    try:
        numbers = [float(x.strip()) for x in numbers_input.split(",")]
        test = VarianceTest(numbers)
        test.evaluate_test()
        
        print(f"\nVarianza calculada: {test.variance:.6f}")
        print(f"Límite inferior: {test.lower_limit:.6f}")
        print(f"Límite superior: {test.upper_limit:.6f}")
        print(f"¿Prueba superada?: {test.passed}")
        
        test.plot_results()
        test.plot_distribution()
    except ValueError:
        print("Error: Asegúrate de ingresar solo números separados por comas.")
