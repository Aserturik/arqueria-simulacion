from statistics import mean
from math import sqrt
from scipy.stats import norm
import matplotlib.pyplot as plt

# Clase que implementa la prueba de promedio para una secuencia de números
class AverageTest:
    # Inicializa la instancia con una lista de números
    def __init__(self, numbers):
        self.numbers = numbers  # Lista de números ingresados
        self.average = 0
        self.alpha = 0.05
        self.acceptation = 0.95
        self.passed = False
        self.n = len(numbers)
        self.z = 0.0
        self.upper_limit = 0.0
        self.lower_limit = 0.0

    # Calcula el promedio de la lista de números
    def compute_average(self):
        if self.n:
            self.average = mean(self.numbers)

    # Calcula el valor Z a partir de alpha
    def compute_z(self):
        self.z = norm.ppf(1 - (self.alpha / 2))

    # Calcula el límite superior de la prueba
    def compute_upper_limit(self):
        if self.n > 0:
            self.upper_limit = 0.5 + (self.z * (1 / sqrt(12 * self.n)))

    # Calcula el límite inferior de la prueba
    def compute_lower_limit(self):
        if self.n > 0:
            self.lower_limit = 0.5 - (self.z * (1 / sqrt(12 * self.n)))

    # Realiza todos los cálculos y determina si la prueba se pasa
    def evaluate_test(self):
        self.compute_average()
        self.compute_z()
        self.compute_upper_limit()
        self.compute_lower_limit()
        self.passed = self.lower_limit <= self.average <= self.upper_limit

    # Reinicia los valores de la prueba a sus valores iniciales
    def reset(self):
        self.average = 0
        self.alpha = 0.05
        self.acceptation = 0.95
        self.passed = False
        self.z = 0.0
        self.upper_limit = 0.0
        self.lower_limit = 0.0

    # Genera un gráfico de barras que muestra el límite inferior, el promedio y el límite superior
    def plot_graph(self):
        categories = ["Límite Inferior", "Promedio", "Límite Superior"]
        values = [self.lower_limit, self.average, self.upper_limit]
        fig, ax = plt.subplots()
        bars = plt.bar(categories, values, color=['red', 'blue', 'green'])
        plt.title("Comparación de Límite Inferior, Promedio y Límite Superior")
        plt.xlabel("Categoría")
        plt.ylabel("Valor")
        # Agrega etiquetas con los valores redondeados sobre cada barra
        for bar, value in zip(bars, values):
            ax.annotate(str(round(value, 4)), xy=(bar.get_x() + bar.get_width() / 2, value),
                        xytext=(0, 1), textcoords="offset points", ha="center", va="bottom")
        plt.show()

if __name__ == "__main__":
    # Solicita al usuario ingresar los números Ri separados por comas
    user_input = input("Ingresa los números Ri separados por comas: ")
    try:
        ri_numbers = [float(x.strip()) for x in user_input.split(",")]
    except ValueError:
        print("Error: asegúrate de ingresar únicamente números separados por comas.")
        exit(1)

    # Crea una instancia de AverageTest con la lista ingresada y evalúa la prueba
    test = AverageTest(ri_numbers)
    test.evaluate_test()

    # Muestra los resultados en consola
    print("Promedio:", test.average)
    print("Límite Inferior:", test.lower_limit)
    print("Límite Superior:", test.upper_limit)
    print("¿Prueba superada?:", test.passed)

    # Muestra el gráfico con los límites y el promedio
    test.plot_graph()
