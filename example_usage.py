from abc import ABC, abstractmethod
from typing import List, Any, Sequence
import math
from time import time

class PRNG(ABC):
    @abstractmethod
    def seed(self, value: int) -> None:
        pass
    
    @abstractmethod
    def random(self) -> float:
        pass

    def randint(self, a: int, b: int) -> int:
        return a + int(self.random() * (b - a + 1))

    def uniform(self, a: float, b: float) -> float:
        return a + (b - a) * self.random()

    def choice(self, seq: Sequence[Any]) -> Any:
        if not seq:
            raise IndexError("No se puede elegir de una secuencia vacía")
        return seq[self.randint(0, len(seq) - 1)]

    def shuffle(self, x: List[Any]) -> None:
        for i in reversed(range(1, len(x))):
            j = self.randint(0, i)
            x[i], x[j] = x[j], x[i]

    def sample(self, population: Sequence[Any], k: int) -> List[Any]:
        if k < 0:
            raise ValueError("El tamaño de la muestra debe ser no negativo")
        n = len(population)
        if k > n:
            raise ValueError("El tamaño de la muestra no puede ser mayor que el de la población")
        result = list(population)
        for i in range(k):
            j = self.randint(i, n - 1)
            result[i], result[j] = result[j], result[i]
        return result[:k]

    def gauss(self, mu: float = 0.0, sigma: float = 1.0) -> float:
        u1 = self.random()
        u2 = self.random()
        z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
        return mu + z0 * sigma

class LinearCongruenceRandom(PRNG):
    DEFAULT_M = 2**31 - 1  # Número primo de Mersenne
    DEFAULT_A = 1597
    DEFAULT_C = 51749
    
    def __init__(self, seed_value=None):
        self.m = self.DEFAULT_M
        self.a = self.DEFAULT_A
        self.c = self.DEFAULT_C
        self._x = seed_value if seed_value is not None else int(time() * 1000)
    
    def seed(self, value):
        self._x = value % self.m
    
    def random(self):
        self._x = (self.a * self._x + self.c) % self.m
        return self._x / self.m

def main():
    # Crear una instancia del generador
    rng = LinearCongruenceRandom(seed_value=12345)

    # Ejecutar ejemplos de uso
    print("\nEjemplos de uso del Generador de Números Pseudoaleatorios:")
    print("-" * 60)
    
    # Generar número flotante entre 0 y 1
    print(f"Número aleatorio [0,1): {rng.random():.6f}")

    # Generar entero en rango específico
    print(f"Entero entre 1 y 10: {rng.randint(1, 10)}")

    # Generar número flotante en rango específico
    print(f"Flotante entre -5.0 y 5.0: {rng.uniform(-5.0, 5.0):.2f}")

    # Seleccionar elemento aleatorio de una lista
    items = ['manzana', 'naranja', 'banana', 'pera']
    print(f"Fruta aleatoria: {rng.choice(items)}")

    # Mezclar una lista
    numbers = list(range(10))
    rng.shuffle(numbers)
    print(f"Lista mezclada: {numbers}")

    # Obtener muestra aleatoria
    print(f"Muestra de 3 números del 1-10: {rng.sample(range(1, 11), 3)}")

    # Generar número con distribución normal
    print(f"Número con distribución normal (μ=0, σ=1): {rng.gauss():.6f}")

if __name__ == '__main__':
    main()

