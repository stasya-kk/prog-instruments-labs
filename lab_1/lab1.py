"""Лабораторная работа №1.

Вариант 7. Функция f(x) = sin(x)/x.
Ряд Тейлора: sin(x) = sum((-1)^n * x^(2n+1) / (2n+1)!).
"""

from __future__ import annotations

import math
from typing import Any

import matplotlib

matplotlib.use("Agg")  # backend без GUI — важно для CI
import matplotlib.pyplot as plt
import numpy as np


def f(x: float | np.floating[Any]) -> float | np.floating[Any]:
    """Исследуемая функция sin(x)/x с защитой от деления на ноль."""
    if abs(x) < 1e-300:
        return 1.0
    return np.sin(x) / x


def machine_epsilon(dtype: type[np.floating[Any]]) -> float:
    """Экспериментальное определение машинного эпсилон для типа dtype."""
    eps = 1.0
    while dtype(1.0 + eps) != dtype(1.0):
        eps /= 2.0
    return eps * 2.0


def my_sin_taylor(x: float, eps: float = 1e-10) -> tuple[float, int]:
    """Вычисление sin(x) через ряд Тейлора с заданной точностью."""
    term = x
    s = term
    n = 0
    while abs(term) > eps:
        n += 1
        term *= -x * x / ((2 * n) * (2 * n + 1))
        s += term
    return s, n


def task1_float_comparison() -> None:
    """Задание 1. Сравнение точности float64 и float32."""
    print("=" * 60)
    print("ЗАДАНИЕ 1: Сравнение float64 и float32")
    print("=" * 60)

    x_vals = np.logspace(-1, -15, 15)

    header = f"{'x':<12} | {'float64':<20} | {'float32':<20} | {'Отн. ошибка':<15}"
    print(header)
    print("-" * 65)

    for x in x_vals:
        res64 = f(np.float64(x))
        res32 = f(np.float32(x))
        rel_err = abs(res64 - res32) / abs(res64) if res64 != 0 else 0.0
        print(f"{x:<12.1e} | {res64:<20.10f} | {res32:<20.10f} | {rel_err:<15.2e}")


def task2_machine_epsilon() -> None:
    """Задание 2. Машинный эпсилон для float64 и float32."""
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 2: Машинный эпсилон")
    print("=" * 60)

    eps_float64 = machine_epsilon(np.float64)
    eps_float32 = machine_epsilon(np.float32)

    print(f"Машинный эпсилон для float64: {eps_float64:.5e}")
    print(f"Машинный эпсилон для float32: {eps_float32:.5e}")


def task3_taylor() -> None:
    """Задание 3. Ряд Тейлора для sin(x)."""
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 3: Ряд Тейлора для sin(x)")
    print("=" * 60)

    for x in (1, -1):
        for eps_val in (1e-6, 1e-10):
            approx, n_terms = my_sin_taylor(x, eps=eps_val)
            exact = math.sin(x)
            error = abs(approx - exact)
            print(
                f"x={x:<3} eps={eps_val:.0e}: approx={approx:.10f}, "
                f"terms={n_terms}, error={error:.2e}"
            )


def task4_error_plot(save_path: str = "lab1_error_plot.png") -> None:
    """Задание 4. График погрешности (x = 2.5)."""
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 4: График погрешности (x = 2.5)")
    print("=" * 60)

    x_fixed = 2.5
    exact_val = math.sin(x_fixed)

    n_terms_list: list[int] = []
    errors_list: list[float] = []

    current_sum = 0.0
    term = x_fixed

    for i in range(1, 20):
        if i == 1:
            term = x_fixed
        else:
            n = i - 1
            term *= -x_fixed * x_fixed / ((2 * n) * (2 * n + 1))
        current_sum += term
        n_terms_list.append(i)
        errors_list.append(abs(exact_val - current_sum))

    plt.figure(figsize=(10, 6))
    plt.semilogy(
        n_terms_list,
        errors_list,
        "o-",
        color="blue",
        label="Абсолютная погрешность",
    )
    plt.title(f"Зависимость погрешности от числа членов ряда (x={x_fixed})")
    plt.xlabel("Количество членов ряда (n)")
    plt.ylabel("Абсолютная погрешность (лог. шкала)")
    plt.grid(True, which="both", linestyle="--")
    plt.legend()
    plt.savefig(save_path, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"График сохранён в {save_path}")


def main() -> None:
    """Точка входа."""
    task1_float_comparison()
    task2_machine_epsilon()
    task3_taylor()
    task4_error_plot()


if __name__ == "__main__":
    main()
