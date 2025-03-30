from numpy import mean, var
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt

class PokerTest:

    def __init__(self, ri_nums):
        self.ri_nums = ri_nums              # Lista de números pseudoaleatorios en el rango [0, 1)
        self.prob = [0.3024, 0.504, 0.108, 0.072, 0.009, 0.0045, 0.0001]  # Probabilidades teóricas de cada mano de poker
        self.oi = [0, 0, 0, 0, 0, 0, 0]      # Frecuencias observadas de cada mano
        self.ei = []                        # Frecuencias esperadas de cada mano (se calcularán según prob y n)
        self.eid = []                       # Valores (oi - ei)^2 / ei para cada mano
        self.passed = False                 # Resultado de la prueba (True si pasó, False si no)
        self.n = len(ri_nums)               # Número de elementos en la secuencia de números pseudoaleatorios
        self.total_sum = 0.0                # Suma total de los valores calculados (oi - ei)^2 / ei
        self.chi_reverse = st.chi2.ppf(1 - 0.05, 6)  # Valor crítico de chi-cuadrado para 6 grados de libertad y nivel 0.05

    # Realiza la prueba de poker y determina si ha pasado.
    def check_poker(self):
        self.calculate_oi()
        self.calculate_ei()
        self.calculate_eid()
        self.calculate_total_sum()
        if self.total_sum < self.chi_reverse:
            self.passed = True
        else:
            self.passed = False
        return self.passed

    # Calcula la suma total de (oi - ei)^2 / ei para cada mano.
    def calculate_total_sum(self):
        for num in self.eid:
            self.total_sum += num

    # Calcula las frecuencias observadas de cada mano de poker.
    def calculate_oi(self):
        for n in self.ri_nums:
            # Convertir el número a cadena y separar en la parte decimal.
            arr = str(n).split(".")
            if len(arr) < 2:
                continue
            num = arr[1]
            if self.all_diff(num):  # Todas diferentes
                self.oi[0] += 1
            elif self.all_same(num):  # Todas iguales
                self.oi[6] += 1
            elif self.four_of_a_kind(num):  # Cuatro del mismo valor
                self.oi[5] += 1
            elif self.one_three_of_a_kind_and_one_pair(num):  # Tercia y un par (Full house)
                self.oi[4] += 1
            elif self.only_three_of_a_kind(num):  # Solo una tercia
                self.oi[3] += 1
            elif self.two_pairs(num):  # Dos pares
                self.oi[2] += 1
            elif self.only_one_pair(num):  # Solo un par
                self.oi[1] += 1

    def all_diff(self, numstr):
        return len(numstr) == len(set(numstr))

    def all_same(self, numstr):
        return len(set(numstr)) == 1

    def four_of_a_kind(self, numstr):
        count = {}
        for char in numstr:
            count[char] = count.get(char, 0) + 1
        num_quads = sum(1 for freq in count.values() if freq == 4)
        return num_quads == 1

    def two_pairs(self, numstr):
        count = {}
        for char in numstr:
            count[char] = count.get(char, 0) + 1
        num_pairs = sum(1 for freq in count.values() if freq == 2)
        return num_pairs == 2

    def one_three_of_a_kind_and_one_pair(self, numstr):
        count = {}
        for char in numstr:
            count[char] = count.get(char, 0) + 1
        num_pairs = sum(1 for freq in count.values() if freq == 2)
        num_triples = sum(1 for freq in count.values() if freq == 3)
        return num_pairs == 1 and num_triples == 1

    def only_one_pair(self, numstr):
        count = {}
        for char in numstr:
            count[char] = count.get(char, 0) + 1
        num_pairs = sum(1 for freq in count.values() if freq == 2)
        return num_pairs == 1

    def only_three_of_a_kind(self, numstr):
        count = {}
        for char in numstr:
            count[char] = count.get(char, 0) + 1
        num_triples = sum(1 for freq in count.values() if freq == 3)
        return num_triples == 1

    # Calcula las frecuencias esperadas de cada mano de poker.
    def calculate_ei(self):
        for i in range(7):
            self.ei.append(self.prob[i] * self.n)

    # Calcula (oi - ei)^2 / ei para cada mano.
    def calculate_eid(self):
        for i in range(len(self.oi)):
            expected = self.prob[i] * self.n
            if expected != 0:
                self.eid.append(((self.oi[i] - expected) ** 2) / expected)

    # Genera un gráfico de barras que compara total_sum con el valor crítico chi_reverse.
    def plot_totalSum_vs_chiReverse(self):
        if self.n != 0:
            x = ['SUM ((Oi - Ei)^2/Ei)', 'Chi2 Crítico']
            y = [self.total_sum, self.chi_reverse]
            colors = ['purple', 'yellow']
            fig, ax = plt.subplots()
            bars = plt.bar(x, y, color=colors, edgecolor='black')
            plt.xlabel('Índices')
            plt.ylabel('Valores')
            plt.title('Comparación: Total Sum vs Chi2 Crítico')
            for bar, value in zip(bars, y):
                ax.annotate(str(round(value, 4)), xy=(bar.get_x() + bar.get_width() / 2, value),
                            xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
            plt.show()

    # Genera un gráfico de barras que compara las frecuencias observadas (oi) y las esperadas (ei).
    def plot_oi_vs_ei(self):
        if self.n != 0:
            hands = ['D', 'O', 'T', 'K', 'F', 'P', 'Q']  # D: Todas diferentes, O: Un par, T: Dos pares, K: Tercia, F: Full house, P: Poker, Q: Todas iguales
            indice = np.arange(len(hands))
            ancho = 0.35
            fig, ax = plt.subplots()
            bars_oi = ax.bar(indice - ancho/2, self.oi, ancho, label='Observadas')
            bars_ei = ax.bar(indice + ancho/2, self.ei, ancho, label='Esperadas', alpha=0.7)
            ax.set_xlabel('Manos de Poker')
            ax.set_ylabel('Frecuencia')
            ax.set_title('Frecuencias Observadas vs. Esperadas')
            ax.set_xticks(indice)
            ax.set_xticklabels(hands)
            ax.legend()
            plt.show()

if __name__ == "__main__":
    # Solicita al usuario que ingrese los números Ri separados por comas
    user_input = input("Ingresa los números Ri separados por comas: ")
    try:
        # Convertir la entrada a una lista de números float
        ri_nums = [float(x.strip()) for x in user_input.split(",")]
    except ValueError:
        print("Error: asegúrate de ingresar únicamente números separados por comas.")
        exit(1)

    # Crea la instancia de PokerTest y ejecuta la prueba
    poker_test = PokerTest(ri_nums)
    passed = poker_test.check_poker()

    # Muestra los resultados en consola
    print("\nNúmeros Ri ingresados:", poker_test.ri_nums)
    print("Frecuencias Observadas (oi):", poker_test.oi)
    print("Frecuencias Esperadas (ei):", poker_test.ei)
    print("Valores calculados ((Oi - Ei)^2/Ei):", poker_test.eid)
    print("Suma Total:", round(poker_test.total_sum, 4))
    print("Valor Crítico de Chi2:", round(poker_test.chi_reverse, 4))
    print("¿Prueba de Poker superada?:", passed)

    # Muestra los gráficos
    poker_test.plot_totalSum_vs_chiReverse()
    poker_test.plot_oi_vs_ei()
