"""
<module>
    <summary>
        Модуль вкладки «Квадратное уравнение» графического интерфейса.
        Предоставляет форму ввода коэффициентов и отображает корни уравнения.
    </summary>
</module>
"""

import tkinter as tk
from tkinter import ttk, messagebox

from src.application.services.math_application_service import MathApplicationService


class QuadraticTab(ttk.Frame):
    """
    <summary>
        Вкладка GUI для решения квадратного уравнения ax² + bx + c = 0.
        Пользователь вводит коэффициенты a, b, c и нажимает «Решить» —
        отображаются дискриминант и корни уравнения.
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
            text="Решение квадратного уравнения  ax² + bx + c = 0",
            font=("Segoe UI", 13, "bold"),
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        coefficients_frame = ttk.LabelFrame(self, text="Коэффициенты", padding=15)
        coefficients_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 15))

        ttk.Label(coefficients_frame, text="a (при x²):").grid(row=0, column=0, sticky="w", pady=5)
        self._entry_a = ttk.Entry(coefficients_frame, width=15)
        self._entry_a.grid(row=0, column=1, padx=10, pady=5)
        self._entry_a.insert(0, "1")

        ttk.Label(coefficients_frame, text="b (при x):").grid(row=1, column=0, sticky="w", pady=5)
        self._entry_b = ttk.Entry(coefficients_frame, width=15)
        self._entry_b.grid(row=1, column=1, padx=10, pady=5)
        self._entry_b.insert(0, "-5")

        ttk.Label(coefficients_frame, text="c (свободный член):").grid(row=2, column=0, sticky="w", pady=5)
        self._entry_c = ttk.Entry(coefficients_frame, width=15)
        self._entry_c.grid(row=2, column=1, padx=10, pady=5)
        self._entry_c.insert(0, "6")

        solve_button = ttk.Button(
            coefficients_frame,
            text="Решить",
            command=self._on_solve,
        )
        solve_button.grid(row=3, column=0, columnspan=2, pady=(15, 0))

        result_frame = ttk.LabelFrame(self, text="Результат", padding=15)
        result_frame.grid(row=1, column=1, sticky="nsew")

        self._result_text = tk.Text(
            result_frame,
            width=38,
            height=10,
            state="disabled",
            font=("Courier New", 11),
            relief="flat",
            bg="#f8f9fa",
        )
        self._result_text.pack(fill="both", expand=True)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

    def _on_solve(self) -> None:
        """<summary>Обрабатывает нажатие кнопки «Решить»: читает ввод, вычисляет, отображает.</summary>"""
        try:
            coefficient_a = float(self._entry_a.get())
            coefficient_b = float(self._entry_b.get())
            coefficient_c = float(self._entry_c.get())
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Введите числовые значения для a, b и c.")
            return

        try:
            solution = self._service.solve_quadratic_equation(
                coefficient_a, coefficient_b, coefficient_c
            )
        except ValueError as error:
            messagebox.showerror("Ошибка", str(error))
            return

        lines = [
            f"Уравнение: {coefficient_a}x² + {coefficient_b}x + {coefficient_c} = 0\n",
            f"Дискриминант D = {solution.discriminant:.6g}\n",
            "─" * 34 + "\n",
        ]

        if solution.has_two_distinct_roots:
            lines.append(f"x₁ = {solution.format_root(solution.root_first)}\n")
            lines.append(f"x₂ = {solution.format_root(solution.root_second)}\n")
        else:
            lines.append(f"x  = {solution.format_root(solution.root_first)}\n")
            lines.append("(единственный корень, D = 0)\n")

        if not solution.has_real_roots:
            lines.append("\n⚠ D < 0 — корни комплексные\n")

        self._set_result_text("".join(lines))

    def _set_result_text(self, content: str) -> None:
        """
        <summary>Обновляет содержимое текстового виджета результатов.</summary>
        <param name="content">Текст для отображения.</param>
        """
        self._result_text.config(state="normal")
        self._result_text.delete("1.0", "end")
        self._result_text.insert("1.0", content)
        self._result_text.config(state="disabled")
