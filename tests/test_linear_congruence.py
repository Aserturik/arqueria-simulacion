import unittest
from modelos.linear_congruence import LinearCongruenceRandom
from modelos.pruebas.chi2_test import ChiTest
from modelos.pruebas.ks_test import KsTest
from modelos.pruebas.variance_test import VarianceTest
from modelos.pruebas.poker_test import PokerTest

class TestLinearCongruenceRandom(unittest.TestCase):
    def setUp(self):
        self.rng = LinearCongruenceRandom(seed_value=12345)
        self.n_samples = 10000

    def test_range(self):
        """Verifica que los números generados estén en el rango [0,1)."""
        for _ in range(1000):
            num = self.rng.random()
            self.assertGreaterEqual(num, 0.0)
            self.assertLess(num, 1.0)

    def test_chi_squared(self):
        """Prueba chi-cuadrado para uniformidad."""
        numbers = [self.rng.random() for _ in range(self.n_samples)]
        test = ChiTest(ri_values=numbers)
        test.checkTest()
        self.assertTrue(test.passed)

    def test_ks(self):
        """Prueba Kolmogorov-Smirnov para uniformidad."""
        numbers = [self.rng.random() for _ in range(self.n_samples)]
        test = KsTest(ri_nums=numbers)
        test.checkTest()
        self.assertTrue(test.passed)

    def test_variance(self):
        """Prueba de varianza."""
        numbers = [self.rng.random() for _ in range(self.n_samples)]
        test = VarianceTest(numbers)
        test.checkTest()
        self.assertTrue(test.passed)

    def test_poker(self):
        """Prueba de poker para independencia."""
        numbers = [self.rng.random() for _ in range(self.n_samples)]
        test = PokerTest(numbers)
        test.check_poker()
        self.assertTrue(test.passed)

    def test_seed_reproducibility(self):
        """Verifica que la misma semilla produzca la misma secuencia."""
        rng1 = LinearCongruenceRandom(seed_value=12345)
        rng2 = LinearCongruenceRandom(seed_value=12345)
        
        for _ in range(1000):
            self.assertEqual(rng1.random(), rng2.random())

if __name__ == '__main__':
    unittest.main()
