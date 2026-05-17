"""
<module>
    <summary>
        Модуль варианта использования «Построение графика функции».
        Возвращает объект фигуры — слой представления сам решает, как его показать.
    </summary>
</module>
"""

from typing import Any

from src.domain.entities.math_function import MathFunction
from src.domain.interfaces.i_plotter import IPlotter


class PlotFunctionUseCase:
    """
    <summary>
        Вариант использования для построения графика одной математической функции.
        Делегирует построение реализации IPlotter и возвращает объект фигуры
        слою представления (паттерн «Стратегия»).
    </summary>
    <param name="plotter">Реализация интерфейса IPlotter.</param>
    """

    def __init__(self, plotter: IPlotter) -> None:
        """
        <summary>Инициализирует вариант использования с конкретным построителем.</summary>
        <param name="plotter">Объект, реализующий интерфейс IPlotter.</param>
        """
        self._plotter = plotter

    def execute(self, function: MathFunction) -> Any:
        """
        <summary>
            Строит график заданной функции и возвращает объект фигуры.
        </summary>
        <param name="function">Математическая функция для построения графика.</param>
        <returns>Объект фигуры для отображения в слое представления.</returns>
        """
        return self._plotter.plot_single_function(function)
