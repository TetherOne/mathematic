"""
<module>
    <summary>
        Модуль реализации построителя графиков на основе Matplotlib.
        Создаёт объект Figure и возвращает его — отображение выполняет GUI.
    </summary>
</module>
"""

from typing import List

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from src.domain.entities.math_function import MathFunction
from src.domain.interfaces.i_plotter import IPlotter
from src.domain.value_objects.intersection_point import IntersectionPoint

_PLOT_POINTS_COUNT = 500
_FIGURE_SIZE = (7, 4)
_GRID_ALPHA = 0.3
_INTERSECTION_MARKER_SIZE = 10
_INTERSECTION_MARKER_COLOR = "#e74c3c"
_CLIP_VALUE = 1e6


class MatplotlibPlotter(IPlotter):
    """
    <summary>
        Реализация IPlotter на основе Matplotlib.
        Все методы создают и возвращают объект Figure без вызова plt.show() —
        слой представления (GUI) встраивает фигуру в нужный виджет.
    </summary>
    """

    def plot_single_function(self, function: MathFunction) -> Figure:
        """
        <summary>Строит график функции и возвращает Figure.</summary>
        <param name="function">Математическая функция для отображения.</param>
        <returns>Объект matplotlib.figure.Figure с готовым графиком.</returns>
        """
        figure, axes = plt.subplots(figsize=_FIGURE_SIZE)
        x_values, y_values = _compute_plot_data(function)

        axes.plot(x_values, y_values, color="#2980b9", linewidth=2,
                  label=f"f(x) = {function.expression}")
        _apply_common_style(axes, f"f(x) = {function.expression}")

        figure.tight_layout()
        return figure

    def plot_intersections(
        self,
        function_first: MathFunction,
        function_second: MathFunction,
        intersection_points: List[IntersectionPoint],
    ) -> Figure:
        """
        <summary>
            Строит совместный график двух функций с точками пересечения
            и возвращает Figure.
        </summary>
        <param name="function_first">Первая математическая функция.</param>
        <param name="function_second">Вторая математическая функция.</param>
        <param name="intersection_points">Список точек пересечения.</param>
        <returns>Объект matplotlib.figure.Figure с готовым графиком.</returns>
        """
        figure, axes = plt.subplots(figsize=_FIGURE_SIZE)

        x_values_first, y_values_first = _compute_plot_data(function_first)
        x_values_second, y_values_second = _compute_plot_data(function_second)

        axes.plot(x_values_first, y_values_first, color="#2980b9", linewidth=2,
                  label=f"f(x) = {function_first.expression}")
        axes.plot(x_values_second, y_values_second, color="#27ae60", linewidth=2,
                  label=f"g(x) = {function_second.expression}")

        _draw_intersection_points(axes, intersection_points)
        _apply_common_style(axes, "Точки пересечения функций")

        figure.tight_layout()
        return figure


def _compute_plot_data(function: MathFunction) -> tuple[np.ndarray, np.ndarray]:
    """
    <summary>
        Вычисляет массивы x и y, заменяя недопустимые значения на NaN
        для корректного отображения разрывов.
    </summary>
    <param name="function">Математическая функция.</param>
    <returns>Кортеж (x_values, y_values).</returns>
    """
    x_values = np.linspace(function.x_min, function.x_max, _PLOT_POINTS_COUNT)
    y_values = np.array(
        [_safe_evaluate(function, x) for x in x_values],
        dtype=float,
    )
    y_values = np.clip(y_values, -_CLIP_VALUE, _CLIP_VALUE)
    return x_values, y_values


def _draw_intersection_points(
    axes: plt.Axes,
    intersection_points: List[IntersectionPoint],
) -> None:
    """
    <summary>Наносит точки пересечения с аннотациями на оси.</summary>
    <param name="axes">Оси matplotlib.</param>
    <param name="intersection_points">Список точек пересечения.</param>
    """
    for point in intersection_points:
        axes.plot(
            point.x, point.y, "o",
            color=_INTERSECTION_MARKER_COLOR,
            markersize=_INTERSECTION_MARKER_SIZE,
            zorder=5,
        )
        axes.annotate(
            str(point),
            xy=(point.x, point.y),
            xytext=(point.x + 0.25, point.y + 0.25),
            fontsize=8,
            color=_INTERSECTION_MARKER_COLOR,
        )


def _apply_common_style(axes: plt.Axes, title: str) -> None:
    """
    <summary>Применяет единый стиль к осям: сетка, легенда, оси координат.</summary>
    <param name="axes">Оси matplotlib.</param>
    <param name="title">Заголовок графика.</param>
    """
    axes.set_title(title, fontsize=12, pad=10)
    axes.set_xlabel("x", fontsize=10)
    axes.set_ylabel("y", fontsize=10)
    axes.axhline(0, color="black", linewidth=0.8)
    axes.axvline(0, color="black", linewidth=0.8)
    axes.grid(True, alpha=_GRID_ALPHA)
    axes.legend(fontsize=9)


def _safe_evaluate(function: MathFunction, x: float) -> float:
    """
    <summary>
        Безопасно вычисляет функцию, возвращая NaN при любых ошибках.
    </summary>
    <param name="function">Математическая функция.</param>
    <param name="x">Значение аргумента.</param>
    <returns>Значение f(x) или float('nan').</returns>
    """
    try:
        result = function.evaluate(x)
        return result if np.isfinite(result) else float("nan")
    except (ValueError, ZeroDivisionError, OverflowError):
        return float("nan")
