"""
<module>
    <summary>
        Модуль сущности задачи перевода числа между системами счисления.
        Допустимые основания: от 2 до 16 включительно.
    </summary>
</module>
"""

from pydantic import BaseModel, ConfigDict, model_validator

_MIN_BASE = 2
_MAX_BASE = 16


class NumberConversionTask(BaseModel):
    """
    <summary>
        Неизменяемая сущность задачи перевода числа из системы счисления
        с основанием source_base в систему с основанием target_base.
        Pydantic валидирует типы, model_validator проверяет диапазоны оснований.
    </summary>
    <param name="number_string">Строковое представление числа в исходной системе.</param>
    <param name="source_base">Основание исходной системы счисления (2–16).</param>
    <param name="target_base">Основание целевой системы счисления (2–16).</param>
    <raises cref="ValidationError">
        Если основания вне диапазона [2, 16] или поля имеют неверные типы.
    </raises>
    """

    model_config = ConfigDict(frozen=True)

    number_string: str
    source_base: int
    target_base: int

    @model_validator(mode="after")
    def validate_bases_in_range(self) -> "NumberConversionTask":
        """
        <summary>
            Проверяет, что оба основания находятся в допустимом диапазоне [2, 16].
        </summary>
        <returns>Экземпляр сущности, если валидация прошла успешно.</returns>
        <raises cref="ValueError">Если хотя бы одно из оснований вне диапазона.</raises>
        """
        self._validate_base(self.source_base, "исходной")
        self._validate_base(self.target_base, "целевой")
        return self

    @staticmethod
    def _validate_base(base: int, system_label: str) -> None:
        """
        <summary>Проверяет допустимость основания системы счисления.</summary>
        <param name="base">Проверяемое основание.</param>
        <param name="system_label">Описание системы для сообщения об ошибке.</param>
        <raises cref="ValueError">Если основание вне диапазона [2, 16].</raises>
        """
        if not (_MIN_BASE <= base <= _MAX_BASE):
            raise ValueError(
                f"Основание {system_label} системы счисления должно быть "
                f"от {_MIN_BASE} до {_MAX_BASE}, получено: {base}."
            )
