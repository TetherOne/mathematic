"""
<module>
    <summary>
        Модуль сущности квадратного уравнения.
        Содержит доменную модель уравнения вида ax² + bx + c = 0.
    </summary>
</module>
"""

from pydantic import BaseModel, ConfigDict, model_validator


class QuadraticEquation(BaseModel):
    """
    <summary>
        Неизменяемая сущность квадратного уравнения вида ax² + bx + c = 0.
        Pydantic автоматически валидирует типы полей при создании объекта.
    </summary>
    <param name="coefficient_a">Коэффициент при x² (не может быть равен нулю).</param>
    <param name="coefficient_b">Коэффициент при x.</param>
    <param name="coefficient_c">Свободный член уравнения.</param>
    <raises cref="ValidationError">
        Если coefficient_a == 0 или поля не являются числами.
    </raises>
    """

    model_config = ConfigDict(frozen=True)

    coefficient_a: float
    coefficient_b: float
    coefficient_c: float

    @model_validator(mode="after")
    def validate_coefficient_a_not_zero(self) -> "QuadraticEquation":
        """
        <summary>
            Проверяет, что коэффициент 'a' не равен нулю.
            Выполняется после валидации типов Pydantic.
        </summary>
        <returns>Экземпляр сущности, если валидация прошла успешно.</returns>
        <raises cref="ValueError">Если coefficient_a == 0.</raises>
        """
        if self.coefficient_a == 0.0:
            raise ValueError(
                "Коэффициент 'a' не может быть равен нулю: "
                "уравнение перестаёт быть квадратным."
            )
        return self
