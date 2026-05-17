"""
<module>
    <summary>
        Модуль варианта использования «Решение квадратного уравнения».
        Содержит доменную логику нахождения корней уравнения ax² + bx + c = 0.
    </summary>
</module>
"""

import cmath

from src.domain.entities.quadratic_equation import QuadraticEquation
from src.domain.value_objects.quadratic_solution import QuadraticSolution


class SolveQuadraticUseCase:
    """
    <summary>
        Вариант использования для решения квадратного уравнения ax² + bx + c = 0.
        Применяет стандартный метод дискриминанта и возвращает объект-значение
        с результатами решения (включая комплексные корни при D < 0).
    </summary>
    """

    def execute(self, equation: QuadraticEquation) -> QuadraticSolution:
        """
        <summary>
            Решает квадратное уравнение и возвращает результат.
        </summary>
        <param name="equation">Сущность квадратного уравнения с коэффициентами a, b, c.</param>
        <returns>
            Объект QuadraticSolution с дискриминантом и корнями уравнения.
        </returns>
        """
        discriminant = self._compute_discriminant(
            equation.coefficient_a,
            equation.coefficient_b,
            equation.coefficient_c,
        )
        return self._compute_roots(
            equation.coefficient_a,
            equation.coefficient_b,
            discriminant,
        )

    @staticmethod
    def _compute_discriminant(
        coefficient_a: float,
        coefficient_b: float,
        coefficient_c: float,
    ) -> float:
        """
        <summary>Вычисляет дискриминант квадратного уравнения D = b² - 4ac.</summary>
        <param name="coefficient_a">Коэффициент при x².</param>
        <param name="coefficient_b">Коэффициент при x.</param>
        <param name="coefficient_c">Свободный член.</param>
        <returns>Значение дискриминанта.</returns>
        """
        return coefficient_b ** 2 - 4 * coefficient_a * coefficient_c

    @staticmethod
    def _compute_roots(
        coefficient_a: float,
        coefficient_b: float,
        discriminant: float,
    ) -> QuadraticSolution:
        """
        <summary>
            Вычисляет корни уравнения по значению дискриминанта.
            Использует модуль cmath для корректной работы с комплексными числами.
        </summary>
        <param name="coefficient_a">Коэффициент при x².</param>
        <param name="coefficient_b">Коэффициент при x.</param>
        <param name="discriminant">Дискриминант уравнения.</param>
        <returns>Объект QuadraticSolution с корнями.</returns>
        """
        sqrt_discriminant = cmath.sqrt(discriminant)
        root_first = (-coefficient_b + sqrt_discriminant) / (2 * coefficient_a)
        root_second = (-coefficient_b - sqrt_discriminant) / (2 * coefficient_a)

        if discriminant == 0.0:
            return QuadraticSolution(
                discriminant=discriminant,
                root_first=root_first,
                root_second=None,
            )

        return QuadraticSolution(
            discriminant=discriminant,
            root_first=root_first,
            root_second=root_second,
        )
