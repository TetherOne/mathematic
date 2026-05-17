"""
<module>
    <summary>
        Модуль варианта использования «Поиск точек пересечения двух функций».
        Возвращает кортеж: список точек пересечения и объект фигуры для GUI.
    </summary>
</module>
"""

from typing import Any, List, Tuple

import numpy as np
from scipy import optimize

from src.domain.entities.math_function import MathFunction
from src.domain.interfaces.i_plotter import IPlotter
from src.domain.value_objects.intersection_point import IntersectionPoint

_SAMPLE_POINTS_COUNT = 1000
_ROOT_FINDING_TOLERANCE = 1e-9


class FindIntersectionsUseCase:
    """
    <summary>
        Вариант использования для нахождения точек пересечения двух функций.

        Алгоритм:
        1. Вычисляет разность g(x) = f1(x) - f2(x) на равномерной сетке.
        2. Находит интервалы со сменой знака (потенциальные пересечения).
        3. Применяет метод Брента для точного нахождения корней.
        4. Передаёт результаты построителю и возвращает фигуру.
    </summary>
    <param name="plotter">Реализация IPlotter для визуализации результата.</param>
    """

    def __init__(self, plotter: IPlotter) -> None:
        """
        <summary>Инициализирует вариант использования с конкретным построителем.</summary>
        <param name="plotter">Объект, реализующий интерфейс IPlotter.</param>
        """
        self._plotter = plotter

    def execute(
        self,
        function_first: MathFunction,
        function_second: MathFunction,
    ) -> Tuple[List[IntersectionPoint], Any]:
        """
        <summary>
            Находит точки пересечения, строит график и возвращает результаты.
        </summary>
        <param name="function_first">Первая математическая функция.</param>
        <param name="function_second">Вторая математическая функция.</param>
        <returns>
            Кортеж (intersection_points, figure):
            - intersection_points: список объектов IntersectionPoint.
            - figure: объект фигуры для встраивания в GUI.
        </returns>
        """
        x_min = min(function_first.x_min, function_second.x_min)
        x_max = max(function_first.x_max, function_second.x_max)

        intersection_points = self._find_intersection_points(
            function_first, function_second, x_min, x_max
        )
        figure = self._plotter.plot_intersections(
            function_first, function_second, intersection_points
        )
        return intersection_points, figure

    @staticmethod
    def _find_intersection_points(
        function_first: MathFunction,
        function_second: MathFunction,
        x_min: float,
        x_max: float,
    ) -> List[IntersectionPoint]:
        """
        <summary>
            Численно находит все точки пересечения на заданном отрезке.
        </summary>
        <param name="function_first">Первая функция.</param>
        <param name="function_second">Вторая функция.</param>
        <param name="x_min">Левая граница поиска.</param>
        <param name="x_max">Правая граница поиска.</param>
        <returns>Список найденных точек пересечения.</returns>
        """
        x_values = np.linspace(x_min, x_max, _SAMPLE_POINTS_COUNT)

        def difference(x: float) -> float:
            return function_first.evaluate(x) - function_second.evaluate(x)

        difference_values = np.array([difference(x) for x in x_values])

        intersection_points: List[IntersectionPoint] = []
        seen_x_values: List[float] = []

        for index in range(len(x_values) - 1):
            left_value = difference_values[index]
            right_value = difference_values[index + 1]

            if not (np.isfinite(left_value) and np.isfinite(right_value)):
                continue

            if left_value * right_value < 0:
                root_x = optimize.brentq(
                    difference,
                    x_values[index],
                    x_values[index + 1],
                    xtol=_ROOT_FINDING_TOLERANCE,
                )
                if not _is_duplicate(root_x, seen_x_values):
                    seen_x_values.append(root_x)
                    root_y = function_first.evaluate(root_x)
                    intersection_points.append(IntersectionPoint(x=root_x, y=root_y))

            elif left_value == 0.0:
                x_candidate = x_values[index]
                if not _is_duplicate(x_candidate, seen_x_values):
                    seen_x_values.append(x_candidate)
                    y_candidate = function_first.evaluate(x_candidate)
                    intersection_points.append(
                        IntersectionPoint(x=x_candidate, y=y_candidate)
                    )

        return intersection_points


def _is_duplicate(candidate_x: float, seen_x_values: List[float]) -> bool:
    """
    <summary>
        Проверяет, не является ли кандидат дубликатом уже найденной точки.
    </summary>
    <param name="candidate_x">Кандидат на новую точку пересечения.</param>
    <param name="seen_x_values">Список уже найденных значений x.</param>
    <returns>True, если кандидат слишком близок к одному из найденных.</returns>
    """
    return any(abs(candidate_x - existing_x) < 1e-6 for existing_x in seen_x_values)
