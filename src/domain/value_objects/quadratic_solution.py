"""
<module>
    <summary>
        Модуль объекта-значения результата решения квадратного уравнения.
    </summary>
</module>
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict


class QuadraticSolution(BaseModel):
    """
    <summary>
        Неизменяемый объект-значение с результатом решения уравнения ax² + bx + c = 0.
        arbitrary_types_allowed=True необходим для хранения complex-чисел.
    </summary>
    <param name="discriminant">Дискриминант D = b² - 4ac.</param>
    <param name="root_first">Первый корень (вещественный или комплексный).</param>
    <param name="root_second">Второй корень (None при D = 0).</param>
    """

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    discriminant: float
    root_first: complex
    root_second: Optional[complex] = None

    @property
    def has_two_distinct_roots(self) -> bool:
        """
        <summary>Возвращает True, если уравнение имеет два различных корня (D ≠ 0).</summary>
        <returns>True при D ≠ 0.</returns>
        """
        return self.discriminant != 0.0

    @property
    def has_real_roots(self) -> bool:
        """
        <summary>Возвращает True, если корни вещественные (D ≥ 0).</summary>
        <returns>True при D ≥ 0.</returns>
        """
        return self.discriminant >= 0.0

    def format_root(self, root: complex) -> str:
        """
        <summary>
            Форматирует корень для отображения:
            вещественный — как float, комплексный — в виде a ± bi.
        </summary>
        <param name="root">Корень уравнения.</param>
        <returns>Строковое представление корня.</returns>
        """
        if root.imag == 0.0:
            return f"{root.real:.6g}"
        sign = "+" if root.imag >= 0 else "-"
        return f"{root.real:.6g} {sign} {abs(root.imag):.6g}i"
