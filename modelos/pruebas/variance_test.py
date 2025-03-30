from numpy import mean, var
import scipy.stats as st
import matplotlib.pyplot as plt

class VarianceTest:
    """
    Clase que implementa la Prueba de Varianza para una secuencia de números generados.
    """
    def __init__(self, ri_numbers):
        self.ri_numbers = ri_numbers        # Lista de números generados
        self.variance = 0.0                 # Varianza calculada de la secuencia (inicialmente 0.0)
        self.alpha = 0.05                   # Nivel de significancia
        self.average = 0.0                  # Promedio de la secuencia (inicialmente 0.0)
        self.acceptation = 0.95             # Tasa de aceptación (valor teórico, no usado en cálculos)
        self.passed = False                 # Resultado de la prueba (True si pasó, False de lo contrario)
        self.n = len(ri_numbers)            # Número total de elementos en la secuencia
        self.superior_limit = 0.0           # Límite superior para la varianza
        self.inferior_limit = 0.0           # Límite inferior para la varianza
        self.chi_square1 = 0.0              # Valor crítico de chi-cuadrado para el límite inferior
        self.chi_square2 = 0.0              # Valor crítico de chi-cuadrado para el límite superior

    def calculateVariance(self):
        self.variance = var(self.ri_numbers)

    def calculateAverage(self):
        self.average = mean(self.ri_numbers)

    def calculateChiSquare1(self):
        self.chi_square1 = st.chi2.ppf(self.alpha / 2, self.n - 1)

    def calculateChiSquare2(self):
        self.chi_square2 = st.chi2.ppf(1 - self.alpha / 2, self.n - 1)

    def calculateInferiorLimit(self):
        self.inferior_limit = self.chi_square1 / (12 * (self.n - 1))

    def calculateSuperiorLimit(self):
        self.superior_limit = self.chi_square2 / (12 * (self.n - 1))

    def checkTest(self):
        self.calculateAverage()
        self.calculateVariance()
        self.calculateChiSquare1()
        self.calculateChiSquare2()
        self.calculateSuperiorLimit()
        self.calculateInferiorLimit()
        if self.inferior_limit <= self.variance <= self.superior_limit:
            self.passed = True
        else:
            self.passed = False

    def plotLimitsAndVariance(self):
        x = ["Límite Inferior", "Varianza", "Límite Superior"]
        y = [self.inferior_limit, self.variance, self.superior_limit]
        fig, ax = plt.subplots()
        bars = ax.bar(x, y, color=['red', 'blue', 'green'])
        plt.title('Límite Inferior, Varianza y Límite Superior')
        plt.xlabel('Medidas')
        plt.ylabel('Valor')
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.4f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 1), textcoords="offset points", ha='center', va='bottom')
        plt.show()

    def clear(self):
        self.variance = 0.0
        self.alpha = 0.05
        self.average = 0.0
        self.acceptation = 0.95
        self.passed = False
        self.superior_limit = 0.0
        self.inferior_limit = 0.0
        self.chi_square1 = 0.0
        self.chi_square2 = 0.0

if __name__ == "__main__":
    # Solicita al usuario que ingrese los números separados por comas
    user_input = input("Ingresa los números separados por comas: ")
    try:
        ri_numbers = [float(x.strip()) for x in user_input.split(",")]
    except ValueError:
        print("Error: asegúrate de ingresar únicamente números separados por comas.")
        exit(1)

    # Crea la instancia de VarianceTest y ejecuta la prueba
    variance_test = VarianceTest(ri_numbers)
    variance_test.checkTest()

    # Muestra los resultados en consola
    print("\nNúmeros ingresados:", variance_test.ri_numbers)
    print("Promedio:", variance_test.average)
    print("Varianza:", variance_test.variance)
    print("Límite Inferior:", variance_test.inferior_limit)
    print("Límite Superior:", variance_test.superior_limit)
    print("¿Prueba de Varianza superada?:", variance_test.passed)

    # Muestra el gráfico
    variance_test.plotLimitsAndVariance()
