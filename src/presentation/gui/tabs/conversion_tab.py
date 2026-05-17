"""
<module>
    <summary>
        Модуль вкладки «Системы счисления» графического интерфейса.
        Позволяет ввести число и основания, отображает результат перевода.
    </summary>
</module>
"""

import tkinter as tk
from tkinter import ttk, messagebox

from src.application.services.math_application_service import MathApplicationService

_BASE_OPTIONS = [str(b) for b in range(2, 17)]


class ConversionTab(ttk.Frame):
    """
    <summary>
        Вкладка GUI для перевода числа из системы счисления с основанием P
        в систему с основанием Q (2 ≤ P, Q ≤ 16).
    </summary>
    <param name="parent">Родительский виджет (ttk.Notebook).</param>
    <param name="service">Сервис приложения с бизнес-логикой.</param>
    """

    def __init__(self, parent: ttk.Notebook, service: MathApplicationService) -> None:
        """
        <summary>Инициализирует вкладку и строит все виджеты.</summary>
        <param name="parent">Родительский виджет.</param>
        <param name="service">Сервис приложения.</param>
        """
        super().__init__(parent, padding=20)
        self._service = service
        self._build_widgets()

    def _build_widgets(self) -> None:
        """<summary>Создаёт и размещает все виджеты вкладки.</summary>"""
        title = ttk.Label(
            self,
            text="Перевод числа между системами счисления",
            font=("Segoe UI", 13, "bold"),
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        input_frame = ttk.LabelFrame(self, text="Параметры", padding=20)
        input_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 20))

        ttk.Label(input_frame, text="Число:").grid(row=0, column=0, sticky="w", pady=8)
        self._entry_number = ttk.Entry(input_frame, width=20, font=("Courier New", 12))
        self._entry_number.grid(row=0, column=1, padx=10, pady=8)
        self._entry_number.insert(0, "FF")

        ttk.Label(input_frame, text="Исходная система (P):").grid(row=1, column=0, sticky="w", pady=8)
        self._var_source = tk.StringVar(value="16")
        source_combo = ttk.Combobox(
            input_frame,
            textvariable=self._var_source,
            values=_BASE_OPTIONS,
            width=6,
            state="readonly",
        )
        source_combo.grid(row=1, column=1, sticky="w", padx=10, pady=8)

        ttk.Label(input_frame, text="Целевая система (Q):").grid(row=2, column=0, sticky="w", pady=8)
        self._var_target = tk.StringVar(value="10")
        target_combo = ttk.Combobox(
            input_frame,
            textvariable=self._var_target,
            values=_BASE_OPTIONS,
            width=6,
            state="readonly",
        )
        target_combo.grid(row=2, column=1, sticky="w", padx=10, pady=8)

        ttk.Button(
            input_frame,
            text="Перевести",
            command=self._on_convert,
        ).grid(row=3, column=0, columnspan=2, pady=(15, 0))

        result_frame = ttk.LabelFrame(self, text="Результат", padding=20)
        result_frame.grid(row=1, column=1, sticky="nsew")

        self._result_var = tk.StringVar(value="")
        result_label = ttk.Label(
            result_frame,
            textvariable=self._result_var,
            font=("Courier New", 14),
            foreground="#2980b9",
            wraplength=300,
            justify="left",
        )
        result_label.pack(anchor="nw")

        self._history_label = ttk.Label(
            result_frame,
            text="",
            font=("Segoe UI", 9),
            foreground="grey",
        )
        self._history_label.pack(anchor="nw", pady=(10, 0))

        self._history: list[str] = []

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def _on_convert(self) -> None:
        """<summary>Обрабатывает нажатие «Перевести»: выполняет перевод и отображает итог.</summary>"""
        number_string = self._entry_number.get().strip()
        if not number_string:
            messagebox.showwarning("Пустое поле", "Введите число для перевода.")
            return

        try:
            source_base = int(self._var_source.get())
            target_base = int(self._var_target.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Выберите корректные основания систем счисления.")
            return

        try:
            result = self._service.convert_number(number_string, source_base, target_base)
        except ValueError as error:
            messagebox.showerror("Ошибка перевода", str(error))
            return

        display = (
            f"{number_string.upper()}  (осн. {source_base})\n"
            f"=\n"
            f"{result}  (осн. {target_base})"
        )
        self._result_var.set(display)

        history_entry = f"{number_string.upper()}({source_base}) → {result}({target_base})"
        self._history.append(history_entry)
        self._history_label.config(
            text="История:\n" + "\n".join(self._history[-5:])
        )
