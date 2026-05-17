"""
<module>
    <summary>
        Модуль сущности квадратного уравнения.
        Содержит доменную модель уравнения вида ax² + bx + c = 0.
    </summary>
</module>
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class QuadraticEquation:
    """
    <summary>
        Неизменяемая сущность квадратного уравнения вида ax² + bx + c = 0.
    </summary>
    <param name="coefficient_a">Коэффициент при x² (не может быть равен нулю).</param>
    <param name="coefficient_b">Коэффициент при x.</param>
    <param name="coefficient_c">Свободный член уравнения.</param>
    <raises cref="ValueError">
        Если коэффициент 'a' равен нулю — уравнение не является квадратным.
    </raises>
    """

    coefficient_a: float
    coefficient_b: float
    coefficient_c: float

    def __post_init__(self) -> None:
        """
        <summary>Валидирует данные сущности после инициализации.</summary>
        <raises cref="ValueError">Если coefficient_a == 0.</raises>
        """
        if self.coefficient_a == 0.0:
            raise ValueError(
                "Коэффициент 'a' не может быть равен нулю: "
                "уравнение перестаёт быть квадратным."
            )
