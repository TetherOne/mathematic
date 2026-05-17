"""
<module>
    <summary>
        Модуль безопасного парсера математических функций на основе eval().
        Предоставляет ограниченное пространство имён с математическими функциями
        из модуля math, исключая доступ к произвольному коду Python.
    </summary>
</module>
"""

import math
from typing import Callable

from src.domain.entities.math_function import MathFunction
from src.domain.interfaces.i_function_parser import IFunctionParser

_SAFE_MATH_NAMESPACE: dict = {
    "__builtins__": {},
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "atan2": math.atan2,
    "sinh": math.sinh,
    "cosh": math.cosh,
    "tanh": math.tanh,
    "exp": math.exp,
    "log": math.log,
    "log2": math.log2,
    "log10": math.log10,
    "sqrt": math.sqrt,
    "pow": math.pow,
    "ceil": math.ceil,
    "floor": math.floor,
    "pi": math.pi,
    "e": math.e,
    "inf": math.inf,
}


class SafeFunctionParser(IFunctionParser):
    """
    <summary>
        Реализация IFunctionParser, использующая Python eval() с ограниченным
        пространством имён для безопасного вычисления математических выражений.

        Поддерживаемые функции: sin, cos, tan, asin, acos, atan, sinh, cosh, tanh,
        exp, log, log2, log10, sqrt, pow, abs, round, min, max, ceil, floor.
        Поддерживаемые константы: pi, e, inf.
    </summary>
    """

    def parse(
        self,
        expression: str,
        x_min: float = -10.0,
        x_max: float = 10.0,
    ) -> MathFunction:
        """
        <summary>
            Компилирует строковое выражение и возвращает объект MathFunction.
        </summary>
        <param name="expression">
            Математическое выражение с переменной 'x'.
            Примеры: 'x**2 - 4', 'sin(x) + 1', '2*x + 3'.
        </param>
        <param name="x_min">Левая граница диапазона аргумента.</param>
        <param name="x_max">Правая граница диапазона аргумента.</param>
        <returns>Объект MathFunction с вычислимым evaluator.</returns>
        <raises cref="ValueError">
            Если выражение содержит синтаксические ошибки или недопустимые имена.
        </raises>
        """
        compiled_expression = self._compile_expression(expression)
        evaluator = self._build_evaluator(compiled_expression)

        self._validate_evaluator(evaluator, expression)

        return MathFunction(
            expression=expression,
            evaluator=evaluator,
            x_min=x_min,
            x_max=x_max,
        )

    @staticmethod
    def _compile_expression(expression: str):
        """
        <summary>Компилирует строковое выражение в байт-код Python.</summary>
        <param name="expression">Строковое математическое выражение.</param>
        <returns>Скомпилированный объект кода.</returns>
        <raises cref="ValueError">При синтаксической ошибке.</raises>
        """
        try:
            return compile(expression, "<string>", "eval")
        except SyntaxError as error:
            raise ValueError(
                f"Синтаксическая ошибка в выражении '{expression}': {error}"
            ) from error

    @staticmethod
    def _build_evaluator(compiled_expression) -> Callable[[float], float]:
        """
        <summary>
            Строит вызываемый объект на основе скомпилированного выражения
            и безопасного пространства имён.
        </summary>
        <param name="compiled_expression">Скомпилированное выражение.</param>
        <returns>Функция f(x) → float.</returns>
        """
        def evaluator(x: float) -> float:
            local_namespace = {"x": x}
            return float(eval(compiled_expression, _SAFE_MATH_NAMESPACE, local_namespace))  # noqa: S307

        return evaluator

    @staticmethod
    def _validate_evaluator(
        evaluator: Callable[[float], float],
        expression: str,
    ) -> None:
        """
        <summary>
            Проверяет корректность вычислителя на тестовом значении x=0.
        </summary>
        <param name="evaluator">Функция для проверки.</param>
        <param name="expression">Исходное выражение (для сообщения об ошибке).</param>
        <raises cref="ValueError">Если вычисление в x=0 вызывает исключение.</raises>
        """
        try:
            evaluator(0.0)
        except (NameError, TypeError) as error:
            raise ValueError(
                f"Выражение '{expression}' содержит недопустимые имена или операции: {error}"
            ) from error
        except ZeroDivisionError:
            pass
        except (ValueError, OverflowError):
            pass
