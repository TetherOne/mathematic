"""
<module>
    <summary>
        Модуль вкладки «График функции» графического интерфейса.
        Позволяет ввести математическое выражение и диапазон,
        после чего отображает встроенный график Matplotlib.
    </summary>
</module>
"""

import tkinter as tk
from tkinter import ttk, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from src.application.services.math_application_service import MathApplicationService


class PlotTab(ttk.Frame):
    """
    <summary>
        Вкладка GUI для построения графика одной функции f(x).
        График встраивается в окно приложения через FigureCanvasTkAgg.
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
        self._canvas: FigureCanvasTkAgg | None = None
        self._build_widgets()

    def _build_widgets(self) -> None:
        """<summary>Создаёт и размещает все виджеты вкладки.</summary>"""
        title = ttk.Label(
            self,
            text="Построение графика функции",
            font=("Segoe UI", 13, "bold"),
        )
        title.pack(anchor="w", pady=(0, 15))

        input_frame = ttk.LabelFrame(self, text="Параметры", padding=12)
        input_frame.pack(fill="x", pady=(0, 10))

        row1 = ttk.Frame(input_frame)
        row1.pack(fill="x", pady=4)
        ttk.Label(row1, text="f(x) =", width=8).pack(side="left")
        self._entry_expression = ttk.Entry(row1, font=("Courier New", 11))
        self._entry_expression.pack(side="left", fill="x", expand=True, padx=5)
        self._entry_expression.insert(0, "x**2 - 4*x + 3")

        row2 = ttk.Frame(input_frame)
        row2.pack(fill="x", pady=4)
        ttk.Label(row2, text="x от:").pack(side="left")
        self._entry_x_min = ttk.Entry(row2, width=8)
        self._entry_x_min.pack(side="left", padx=5)
        self._entry_x_min.insert(0, "-10")
        ttk.Label(row2, text="до:").pack(side="left")
        self._entry_x_max = ttk.Entry(row2, width=8)
        self._entry_x_max.pack(side="left", padx=5)
        self._entry_x_max.insert(0, "10")

        ttk.Button(
            input_frame,
            text="Построить график",
            command=self._on_plot,
        ).pack(pady=(8, 0))

        self._plot_frame = ttk.Frame(self)
        self._plot_frame.pack(fill="both", expand=True)

        hint = ttk.Label(
            self,
            text="Доступно: sin, cos, tan, exp, log, sqrt, pi, e  |  Пример: sin(x) + x**2 / 4",
            foreground="grey",
            font=("Segoe UI", 9),
        )
        hint.pack(anchor="w", pady=(4, 0))

    def _on_plot(self) -> None:
        """<summary>Обрабатывает нажатие «Построить»: строит и встраивает график.</summary>"""
        expression = self._entry_expression.get().strip()
        if not expression:
            messagebox.showwarning("Пустое поле", "Введите выражение для f(x).")
            return

        try:
            x_min = float(self._entry_x_min.get())
            x_max = float(self._entry_x_max.get())
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Введите числовые значения диапазона x.")
            return

        if x_min >= x_max:
            messagebox.showerror("Ошибка диапазона", "Левая граница должна быть меньше правой.")
            return

        try:
            figure = self._service.plot_function(expression, x_min, x_max)
        except ValueError as error:
            messagebox.showerror("Ошибка выражения", str(error))
            return

        self._embed_figure(figure)

    def _embed_figure(self, figure) -> None:
        """
        <summary>
            Встраивает объект Figure в tkinter-фрейм.
            Удаляет предыдущий холст перед созданием нового.
        </summary>
        <param name="figure">Объект matplotlib.figure.Figure.</param>
        """
        for widget in self._plot_frame.winfo_children():
            widget.destroy()

        self._canvas = FigureCanvasTkAgg(figure, master=self._plot_frame)
        self._canvas.draw()
        self._canvas.get_tk_widget().pack(fill="both", expand=True)

        toolbar = NavigationToolbar2Tk(self._canvas, self._plot_frame)
        toolbar.update()
