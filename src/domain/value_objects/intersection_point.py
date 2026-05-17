"""
<module>
    <summary>
        Модуль объекта-значения точки пересечения двух функций.
    </summary>
</module>
"""

from pydantic import BaseModel, ConfigDict


class IntersectionPoint(BaseModel):
    """
    <summary>
        Неизменяемый объект-значение с координатами точки пересечения двух функций.
    </summary>
    <param name="x">Координата по оси x.</param>
    <param name="y">Координата по оси y.</param>
    """

    model_config = ConfigDict(frozen=True)

    x: float
    y: float

    def __str__(self) -> str:
        """
        <summary>Возвращает строковое представление точки в формате (x; y).</summary>
        <returns>Строка вида '(x; y)' с точностью до 6 значащих цифр.</returns>
        """
        return f"({self.x:.6g}; {self.y:.6g})"
