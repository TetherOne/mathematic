"""
<module>
    <summary>
        Модуль абстрактного интерфейса парсера математических функций.
        Определяет контракт для безопасного разбора строковых выражений.
    </summary>
</module>
"""

from abc import ABC, abstractmethod

from src.domain.entities.math_function import MathFunction


class IFunctionParser(ABC):
    """
    <summary>
        Абстрактный интерфейс для разбора строкового выражения математической
        функции и создания объекта MathFunction.
    </summary>
    """

    @abstractmethod
    def parse(
        self,
        expression: str,
        x_min: float = -10.0,
        x_max: float = 10.0,
    ) -> MathFunction:
        """
        <summary>
            Разбирает строковое выражение и возвращает объект MathFunction.
        </summary>
        <param name="expression">
            Математическое выражение в виде строки (переменная — 'x').
            Примеры: 'x**2 - 4', 'sin(x) + cos(x)', '2*x + 1'.
        </param>
        <param name="x_min">Левая граница диапазона аргумента.</param>
        <param name="x_max">Правая граница диапазона аргумента.</param>
        <returns>Объект MathFunction с заполненными полями expression и evaluator.</returns>
        <raises cref="ValueError">Если выражение содержит недопустимые конструкции.</raises>
        """
