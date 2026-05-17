"""
<module>
    <summary>
        Модуль варианта использования «Перевод числа между системами счисления».
        Поддерживает основания от 2 до 16 включительно.
        Цифры от 10 до 15 представляются буквами A–F.
    </summary>
</module>
"""

from src.domain.entities.number_conversion_task import NumberConversionTask

_DIGITS_ALPHABET = "0123456789ABCDEF"


class ConvertNumberUseCase:
    """
    <summary>
        Вариант использования для перевода целого числа из системы счисления
        с основанием P в систему с основанием Q.

        Алгоритм:
        1. Парсит строку number_string как целое число в системе счисления source_base.
        2. Переводит полученное десятичное целое в строку в системе target_base
           методом последовательного деления с остатком.
    </summary>
    """

    def execute(self, task: NumberConversionTask) -> str:
        """
        <summary>
            Выполняет перевод числа из одной системы счисления в другую.
        </summary>
        <param name="task">Задача перевода с исходным числом и основаниями.</param>
        <returns>
            Строковое представление числа в целевой системе счисления
            (буквы A–F используются для цифр 10–15).
        </returns>
        <raises cref="ValueError">
            Если number_string содержит цифры, недопустимые для source_base.
        </raises>
        """
        decimal_value = self._parse_to_decimal(
            task.number_string.upper(), task.source_base
        )
        return self._convert_from_decimal(decimal_value, task.target_base)

    @staticmethod
    def _parse_to_decimal(number_string: str, source_base: int) -> int:
        """
        <summary>
            Переводит строку в десятичное целое число.
            Использует встроенную функцию int() с параметром base.
        </summary>
        <param name="number_string">Строка числа в верхнем регистре.</param>
        <param name="source_base">Основание исходной системы счисления.</param>
        <returns>Десятичное значение числа.</returns>
        <raises cref="ValueError">Если строка содержит недопустимые символы.</raises>
        """
        try:
            return int(number_string, source_base)
        except ValueError as error:
            raise ValueError(
                f"Число '{number_string}' содержит символы, недопустимые "
                f"для системы с основанием {source_base}."
            ) from error

    @staticmethod
    def _convert_from_decimal(decimal_value: int, target_base: int) -> str:
        """
        <summary>
            Переводит десятичное целое число в строку в заданной системе счисления
            методом последовательного деления с остатком.
        </summary>
        <param name="decimal_value">Исходное десятичное значение (неотрицательное).</param>
        <param name="target_base">Основание целевой системы счисления.</param>
        <returns>Строковое представление числа в системе target_base.</returns>
        """
        if decimal_value == 0:
            return "0"

        is_negative = decimal_value < 0
        remaining = abs(decimal_value)
        digits: list[str] = []

        while remaining > 0:
            remainder = remaining % target_base
            digits.append(_DIGITS_ALPHABET[remainder])
            remaining //= target_base

        if is_negative:
            digits.append("-")

        return "".join(reversed(digits))
