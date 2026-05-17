"""
<module>
    <summary>
        Модуль сервиса приложения «Математика».
        Координирует варианты использования и возвращает результаты GUI-слою.
    </summary>
</module>
"""

from typing import Any, List, Tuple

from src.domain.interfaces.i_function_parser import IFunctionParser
from src.domain.interfaces.i_plotter import IPlotter
from src.domain.entities.number_conversion_task import NumberConversionTask
from src.domain.entities.quadratic_equation import QuadraticEquation
from src.domain.use_cases.convert_number_use_case import ConvertNumberUseCase
from src.domain.use_cases.find_intersections_use_case import FindIntersectionsUseCase
from src.domain.use_cases.plot_function_use_case import PlotFunctionUseCase
from src.domain.use_cases.solve_quadratic_use_case import SolveQuadraticUseCase
from src.domain.value_objects.intersection_point import IntersectionPoint
from src.domain.value_objects.quadratic_solution import QuadraticSolution


class MathApplicationService:
    """
    <summary>
        Сервис приложения — фасад над всеми вариантами использования.
        Принимает примитивные данные от GUI, формирует доменные объекты,
        делегирует выполнение use cases и возвращает результаты.

        Паттерн: Façade + Dependency Injection.
    </summary>
    <param name="plotter">Реализация IPlotter для визуализации.</param>
    <param name="function_parser">Реализация IFunctionParser для разбора выражений.</param>
    """

    def __init__(self, plotter: IPlotter, function_parser: IFunctionParser) -> None:
        """
        <summary>Инициализирует сервис с внедрёнными зависимостями.</summary>
        <param name="plotter">Построитель графиков.</param>
        <param name="function_parser">Парсер математических функций.</param>
        """
        self._function_parser = function_parser

        self._solve_quadratic = SolveQuadraticUseCase()
        self._plot_function = PlotFunctionUseCase(plotter)
        self._find_intersections = FindIntersectionsUseCase(plotter)
        self._convert_number = ConvertNumberUseCase()

    def solve_quadratic_equation(
        self,
        coefficient_a: float,
        coefficient_b: float,
        coefficient_c: float,
    ) -> QuadraticSolution:
        """
        <summary>Решает квадратное уравнение ax² + bx + c = 0.</summary>
        <param name="coefficient_a">Коэффициент при x².</param>
        <param name="coefficient_b">Коэффициент при x.</param>
        <param name="coefficient_c">Свободный член.</param>
        <returns>Объект QuadraticSolution с дискриминантом и корнями.</returns>
        <raises cref="ValueError">Если coefficient_a == 0.</raises>
        """
        equation = QuadraticEquation(
            coefficient_a=coefficient_a,
            coefficient_b=coefficient_b,
            coefficient_c=coefficient_c,
        )
        return self._solve_quadratic.execute(equation)

    def plot_function(
        self,
        expression: str,
        x_min: float = -10.0,
        x_max: float = 10.0,
    ) -> Any:
        """
        <summary>Парсит выражение и строит график функции.</summary>
        <param name="expression">Математическое выражение (переменная — 'x').</param>
        <param name="x_min">Левая граница отображения.</param>
        <param name="x_max">Правая граница отображения.</param>
        <returns>Объект фигуры (matplotlib.figure.Figure) для встраивания в GUI.</returns>
        <raises cref="ValueError">Если выражение содержит недопустимые конструкции.</raises>
        """
        function = self._function_parser.parse(expression, x_min, x_max)
        return self._plot_function.execute(function)

    def find_intersections(
        self,
        expression_first: str,
        expression_second: str,
        x_min: float = -10.0,
        x_max: float = 10.0,
    ) -> Tuple[List[IntersectionPoint], Any]:
        """
        <summary>
            Парсит два выражения, находит точки пересечения и строит график.
        </summary>
        <param name="expression_first">Первое математическое выражение.</param>
        <param name="expression_second">Второе математическое выражение.</param>
        <param name="x_min">Левая граница поиска.</param>
        <param name="x_max">Правая граница поиска.</param>
        <returns>
            Кортеж (points, figure):
            - points: список IntersectionPoint.
            - figure: объект фигуры для встраивания в GUI.
        </returns>
        """
        function_first = self._function_parser.parse(expression_first, x_min, x_max)
        function_second = self._function_parser.parse(expression_second, x_min, x_max)
        return self._find_intersections.execute(function_first, function_second)

    def convert_number(
        self,
        number_string: str,
        source_base: int,
        target_base: int,
    ) -> str:
        """
        <summary>Переводит число из одной системы счисления в другую.</summary>
        <param name="number_string">Строка числа в исходной системе счисления.</param>
        <param name="source_base">Основание исходной системы (2–16).</param>
        <param name="target_base">Основание целевой системы (2–16).</param>
        <returns>Строка числа в целевой системе счисления.</returns>
        <raises cref="ValueError">Если данные некорректны.</raises>
        """
        task = NumberConversionTask(
            number_string=number_string,
            source_base=source_base,
            target_base=target_base,
        )
        return self._convert_number.execute(task)
