"""
<module>
    <summary>
        Модуль вкладки «Пересечение функций» графического интерфейса.
        Отображает координаты точек пересечения и встроенный график двух функций.
    </summary>
</module>
"""

import tkinter as tk
from tkinter import ttk, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from src.application.services.math_application_service import MathApplicationService


class IntersectionTab(ttk.Frame):
    """
    <summary>
        Вкладка GUI для поиска точек пересечения двух функций f(x) и g(x).
        Выводит список координат и встраивает совместный график.
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
            text="Точки пересечения двух функций",
            font=("Segoe UI", 13, "bold"),
        )
        title.pack(anchor="w", pady=(0, 15))

        input_frame = ttk.LabelFrame(self, text="Функции и диапазон", padding=12)
        input_frame.pack(fill="x", pady=(0, 10))

        row1 = ttk.Frame(input_frame)
        row1.pack(fill="x", pady=4)
        ttk.Label(row1, text="f(x) =", width=8).pack(side="left")
        self._entry_f = ttk.Entry(row1, font=("Courier New", 11))
        self._entry_f.pack(side="left", fill="x", expand=True, padx=5)
        self._entry_f.insert(0, "x**2")

        row2 = ttk.Frame(input_frame)
        row2.pack(fill="x", pady=4)
        ttk.Label(row2, text="g(x) =", width=8).pack(side="left")
        self._entry_g = ttk.Entry(row2, font=("Courier New", 11))
        self._entry_g.pack(side="left", fill="x", expand=True, padx=5)
        self._entry_g.insert(0, "x + 2")

        row3 = ttk.Frame(input_frame)
        row3.pack(fill="x", pady=4)
        ttk.Label(row3, text="x от:").pack(side="left")
        self._entry_x_min = ttk.Entry(row3, width=8)
        self._entry_x_min.pack(side="left", padx=5)
        self._entry_x_min.insert(0, "-10")
        ttk.Label(row3, text="до:").pack(side="left")
        self._entry_x_max = ttk.Entry(row3, width=8)
        self._entry_x_max.pack(side="left", padx=5)
        self._entry_x_max.insert(0, "10")

        ttk.Button(
            input_frame,
            text="Найти пересечения",
            command=self._on_find,
        ).pack(pady=(8, 0))

        content_frame = ttk.Frame(self)
        content_frame.pack(fill="both", expand=True)

        result_frame = ttk.LabelFrame(content_frame, text="Координаты точек", padding=10)
        result_frame.pack(side="left", fill="y", padx=(0, 10))

        self._result_listbox = tk.Listbox(
            result_frame,
            width=26,
            font=("Courier New", 11),
            selectmode="browse",
            relief="flat",
            bg="#f8f9fa",
        )
        self._result_listbox.pack(fill="both", expand=True)

        self._plot_frame = ttk.Frame(content_frame)
        self._plot_frame.pack(side="left", fill="both", expand=True)

    def _on_find(self) -> None:
        """<summary>Обрабатывает нажатие «Найти пересечения».</summary>"""
        expression_f = self._entry_f.get().strip()
        expression_g = self._entry_g.get().strip()
        if not expression_f or not expression_g:
            messagebox.showwarning("Пустое поле", "Введите выражения для f(x) и g(x).")
            return

        try:
            x_min = float(self._entry_x_min.get())
            x_max = float(self._entry_x_max.get())
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Введите числовые значения диапазона x.")
            return

        try:
            points, figure = self._service.find_intersections(
                expression_f, expression_g, x_min, x_max
            )
        except ValueError as error:
            messagebox.showerror("Ошибка выражения", str(error))
            return

        self._result_listbox.delete(0, "end")
        if not points:
            self._result_listbox.insert("end", "Пересечений не найдено")
        else:
            self._result_listbox.insert("end", f"Найдено: {len(points)}")
            self._result_listbox.insert("end", "─" * 22)
            for index, point in enumerate(points, start=1):
                self._result_listbox.insert("end", f"  {index}. {point}")

        self._embed_figure(figure)

    def _embed_figure(self, figure) -> None:
        """
        <summary>Встраивает Figure в tkinter-фрейм, заменяя предыдущий.</summary>
        <param name="figure">Объект matplotlib.figure.Figure.</param>
        """
        for widget in self._plot_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(figure, master=self._plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self._plot_frame)
        toolbar.update()
