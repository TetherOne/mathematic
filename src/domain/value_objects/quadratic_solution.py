"""
<module>
    <summary>
        Модуль объекта-значения результата решения квадратного уравнения.
    </summary>
</module>
"""

from dataclasses import dataclass
from typing import Optional
import cmath


@dataclass(frozen=True)
class QuadraticSolution:
    """
    <summary>
        Неизменяемый объект-значение, хранящий результат решения
        квадратного уравнения ax² + bx + c = 0.
    </summary>
    <param name="discriminant">Дискриминант уравнения D = b² - 4ac.</param>
    <param name="root_first">Первый корень уравнения (вещественный или комплексный).</param>
    <param name="root_second">
        Второй корень уравнения (None, если дискриминант равен нулю).
    </param>
    """

    discriminant: float
    root_first: complex
    root_second: Optional[complex]

    @property
    def has_two_distinct_roots(self) -> bool:
        """
        <summary>Возвращает True, если уравнение имеет два различных корня.</summary>
        <returns>True при D ≠ 0, иначе False.</returns>
        """
        return self.discriminant != 0.0

    @property
    def has_real_roots(self) -> bool:
        """
        <summary>Возвращает True, если корни являются вещественными числами.</summary>
        <returns>True при D ≥ 0, иначе False.</returns>
        """
        return self.discriminant >= 0.0

    def format_root(self, root: complex) -> str:
        """
        <summary>
            Форматирует корень для отображения: вещественный — как float,
            комплексный — в виде a+bi.
        </summary>
        <param name="root">Корень уравнения.</param>
        <returns>Строковое представление корня.</returns>
        """
        if root.imag == 0.0:
            return f"{root.real:.6g}"
        return f"{root.real:.6g} {'+' if root.imag >= 0 else '-'} {abs(root.imag):.6g}i"
