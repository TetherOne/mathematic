"""
<module>
    <summary>
        Модуль абстрактного интерфейса построителя графиков.
        Методы возвращают объект фигуры (matplotlib.figure.Figure или аналог),
        не отображая её — за отображение отвечает слой представления.
    </summary>
</module>
"""

from abc import ABC, abstractmethod
from typing import Any, List

from src.domain.entities.math_function import MathFunction
from src.domain.value_objects.intersection_point import IntersectionPoint


class IPlotter(ABC):
    """
    <summary>
        Абстрактный интерфейс (Strategy) для построения графиков функций.
        Конкретные реализации создают графическое представление и возвращают
        объект фигуры — слой представления самостоятельно решает, как его отобразить
        (встроить в GUI, сохранить в файл, показать в окне и т.д.).
    </summary>
    """

    @abstractmethod
    def plot_single_function(self, function: MathFunction) -> Any:
        """
        <summary>Строит график одной функции и возвращает объект фигуры.</summary>
        <param name="function">Математическая функция для отображения.</param>
        <returns>Объект фигуры (например, matplotlib.figure.Figure).</returns>
        """

    @abstractmethod
    def plot_intersections(
        self,
        function_first: MathFunction,
        function_second: MathFunction,
        intersection_points: List[IntersectionPoint],
    ) -> Any:
        """
        <summary>
            Строит графики двух функций с отмеченными точками пересечения
            и возвращает объект фигуры.
        </summary>
        <param name="function_first">Первая математическая функция.</param>
        <param name="function_second">Вторая математическая функция.</param>
        <param name="intersection_points">Список точек пересечения.</param>
        <returns>Объект фигуры (например, matplotlib.figure.Figure).</returns>
        """
