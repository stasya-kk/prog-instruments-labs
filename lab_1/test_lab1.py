"""Тесты для лабораторной работы №1."""

import math
import unittest

import numpy as np

from lab1 import f, machine_epsilon, my_sin_taylor


class Lab1Test(unittest.TestCase):
    """Тесты для функций f, machine_epsilon, my_sin_taylor."""

    def test_f_at_zero_returns_one(self) -> None:
        """f(0) должно быть 1.0 — защита от деления на ноль."""
        self.assertEqual(f(0.0), 1.0)

    def test_machine_epsilon_float64(self) -> None:
        """Машинный эпсилон для float64 примерно 2.22e-16."""
        eps = machine_epsilon(np.float64)
        self.assertGreater(eps, 2.0e-16)
        self.assertLess(eps, 2.5e-16)

    def test_my_sin_taylor_small_x(self) -> None:
        """Ряд Тейлора для x=0.5 близок к math.sin(0.5)."""
        approx, _ = my_sin_taylor(0.5)
        self.assertAlmostEqual(approx, math.sin(0.5), places=9)

    def test_my_sin_taylor_negative(self) -> None:
        """Ряд Тейлора для x=-1 близок к math.sin(-1)."""
        approx, _ = my_sin_taylor(-1.0)
        self.assertAlmostEqual(approx, math.sin(-1.0), places=9)


if __name__ == "__main__":
    unittest.main()
