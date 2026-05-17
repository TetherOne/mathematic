"""
<module>
    <summary>
        Модуль сущности задачи перевода числа между системами счисления.
        Допустимые основания: от 2 до 16 включительно.
    </summary>
</module>
"""

from dataclasses import dataclass

_MIN_BASE = 2
_MAX_BASE = 16


@dataclass(frozen=True)
class NumberConversionTask:
    """
    <summary>
        Неизменяемая сущность задачи перевода числа из системы счисления
        с основанием source_base в систему с основанием target_base.
    </summary>
    <param name="number_string">
        Строковое представление числа в исходной системе счисления.
        Допустимы цифры 0–9 и буквы A–F (регистр не важен).
    </param>
    <param name="source_base">Основание исходной системы счисления (2–16).</param>
    <param name="target_base">Основание целевой системы счисления (2–16).</param>
    <raises cref="ValueError">
        Если основания выходят за пределы допустимого диапазона [2, 16].
    </raises>
    """

    number_string: str
    source_base: int
    target_base: int

    def __post_init__(self) -> None:
        """
        <summary>Валидирует основания систем счисления после инициализации.</summary>
        <raises cref="ValueError">Если source_base или target_base вне диапазона [2, 16].</raises>
        """
        self._validate_base(self.source_base, "исходной")
        self._validate_base(self.target_base, "целевой")

    @staticmethod
    def _validate_base(base: int, system_label: str) -> None:
        """
        <summary>Проверяет, что основание системы счисления находится в допустимом диапазоне.</summary>
        <param name="base">Проверяемое основание.</param>
        <param name="system_label">Человекочитаемое описание системы (для сообщения об ошибке).</param>
        <raises cref="ValueError">Если основание вне диапазона [2, 16].</raises>
        """
        if not (_MIN_BASE <= base <= _MAX_BASE):
            raise ValueError(
                f"Основание {system_label} системы счисления должно быть "
                f"от {_MIN_BASE} до {_MAX_BASE}, получено: {base}."
            )
