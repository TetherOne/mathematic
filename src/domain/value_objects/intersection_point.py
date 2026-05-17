"""
<module>
    <summary>
        Модуль объекта-значения точки пересечения двух функций.
    </summary>
</module>
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class IntersectionPoint:
    """
    <summary>
        Неизменяемый объект-значение, хранящий координаты точки
        пересечения двух математических функций.
    </summary>
    <param name="x">Координата по оси x.</param>
    <param name="y">Координата по оси y (вычисляется как f1(x) = f2(x)).</param>
    """

    x: float
    y: float

    def __str__(self) -> str:
        """
        <summary>Возвращает строковое представление точки в формате (x; y).</summary>
        <returns>Строка вида '(x; y)' с точностью до 6 значащих цифр.</returns>
        """
        return f"({self.x:.6g}; {self.y:.6g})"
