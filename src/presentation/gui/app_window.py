"""
<module>
    <summary>
        Модуль главного окна графического приложения «Математика».
        Создаёт корневое окно tkinter с ttk.Notebook и четырьмя вкладками.
    </summary>
</module>
"""

import tkinter as tk
from tkinter import ttk

from src.application.services.math_application_service import MathApplicationService
from src.presentation.gui.tabs.conversion_tab import ConversionTab
from src.presentation.gui.tabs.intersection_tab import IntersectionTab
from src.presentation.gui.tabs.plot_tab import PlotTab
from src.presentation.gui.tabs.quadratic_tab import QuadraticTab

_WINDOW_TITLE = "Математика"
_WINDOW_MIN_WIDTH = 900
_WINDOW_MIN_HEIGHT = 620


class AppWindow:
    """
    <summary>
        Главное окно приложения на базе tkinter.
        Содержит ttk.Notebook с четырьмя вкладками, по одной на каждую
        математическую функцию приложения.
    </summary>
    <param name="service">Сервис приложения с бизнес-логикой.</param>
    """

    def __init__(self, service: MathApplicationService) -> None:
        """
        <summary>Инициализирует главное окно и собирает все вкладки.</summary>
        <param name="service">Сервис приложения.</param>
        """
        self._root = tk.Tk()
        self._root.title(_WINDOW_TITLE)
        self._root.minsize(_WINDOW_MIN_WIDTH, _WINDOW_MIN_HEIGHT)
        self._root.resizable(True, True)

        self._apply_theme()
        self._build_notebook(service)

    def _apply_theme(self) -> None:
        """<summary>Настраивает визуальную тему приложения через ttk.Style.</summary>"""
        style = ttk.Style(self._root)
        available_themes = style.theme_names()
        preferred_themes = ("clam", "alt", "default")
        for theme in preferred_themes:
            if theme in available_themes:
                style.theme_use(theme)
                break

        style.configure("TNotebook.Tab", padding=(14, 6), font=("Segoe UI", 10))
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TEntry", padding=4)
        style.configure("TLabelframe.Label", font=("Segoe UI", 10, "bold"))

    def _build_notebook(self, service: MathApplicationService) -> None:
        """
        <summary>Создаёт ttk.Notebook и добавляет все четыре вкладки.</summary>
        <param name="service">Сервис приложения, передаваемый каждой вкладке.</param>
        """
        notebook = ttk.Notebook(self._root)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        tabs = [
            (QuadraticTab(notebook, service), "📐 Квадратное уравнение"),
            (PlotTab(notebook, service),      "📈 График функции"),
            (IntersectionTab(notebook, service), "🔀 Пересечение функций"),
            (ConversionTab(notebook, service), "🔢 Системы счисления"),
        ]

        for tab_frame, tab_title in tabs:
            notebook.add(tab_frame, text=tab_title)

    def run(self) -> None:
        """
        <summary>Запускает главный цикл событий tkinter.</summary>
        """
        self._root.mainloop()
