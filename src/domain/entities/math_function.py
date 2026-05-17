"""
<module>
    <summary>
        Модуль сущности математической функции.
        Представляет функцию одной переменной с диапазоном отображения.
    </summary>
</module>
"""

from dataclasses import dataclass, field
from typing import Callable


@dataclass
class MathFunction:
    """
    <summary>
        Сущность математической функции f(x), заданной строковым выражением
        и вычислимым объектом-функцией.
    </summary>
    <param name="expression">Строковое представление функции (например, 'x**2 + 2*x - 3').</param>
    <param name="evaluator">Вызываемый объект, вычисляющий f(x) по значению x.</param>
    <param name="x_min">Левая граница диапазона отображения (по умолчанию -10).</param>
    <param name="x_max">Правая граница диапазона отображения (по умолчанию 10).</param>
    """

    expression: str
    evaluator: Callable[[float], float]
    x_min: float = field(default=-10.0)
    x_max: float = field(default=10.0)

    def evaluate(self, x: float) -> float:
        """
        <summary>Вычисляет значение функции в точке x.</summary>
        <param name="x">Значение аргумента функции.</param>
        <returns>Значение f(x).</returns>
        """
        return self.evaluator(x)
