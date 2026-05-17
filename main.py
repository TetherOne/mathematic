"""
<module>
    <summary>
        Точка входа в приложение «Математика».
        Выполняет сборку зависимостей (Composition Root) и запускает GUI.

        Архитектура:
        ┌──────────────────────────────────────────────────────────┐
        │  Presentation  →  src/presentation/gui/                  │
        │    AppWindow · QuadraticTab · PlotTab                    │
        │    IntersectionTab · ConversionTab                       │
        ├──────────────────────────────────────────────────────────┤
        │  Application   →  src/application/services/              │
        │    MathApplicationService  (Façade + DI)                 │
        ├──────────────────────────────────────────────────────────┤
        │  Domain        →  src/domain/                            │
        │    Entities · Value Objects · Use Cases · Interfaces     │
        ├──────────────────────────────────────────────────────────┤
        │  Infrastructure →  src/infrastructure/                   │
        │    MatplotlibPlotter · SafeFunctionParser                │
        └──────────────────────────────────────────────────────────┘
    </summary>
</module>
"""

from src.application.services.math_application_service import MathApplicationService
from src.infrastructure.parsing.safe_function_parser import SafeFunctionParser
from src.infrastructure.plotting.matplotlib_plotter import MatplotlibPlotter
from src.presentation.gui.app_window import AppWindow


def main() -> None:
    """
    <summary>
        Собирает граф зависимостей и запускает графическое приложение.
    </summary>
    """
    plotter = MatplotlibPlotter()
    function_parser = SafeFunctionParser()

    service = MathApplicationService(
        plotter=plotter,
        function_parser=function_parser,
    )

    window = AppWindow(service)
    window.run()


if __name__ == "__main__":
    main()
