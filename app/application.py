"""객체 생성과 연결(조립)을 담당하는 애플리케이션 루트."""
import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QStyle

from app.config.settings_repository import SettingsRepository
from app.config.startup_options import StartupOptions
from app.config.target_store import TargetStore
from app.core.process_selection_controller import ProcessSelectionController
from app.core.tray_minimize_service import TrayMinimizeService
from app.icons.app_icon_provider import AppIconProvider
from app.icons.executable_icon_provider import ExecutableIconProvider
from app.process.process_path_resolver import ProcessPathResolver
from app.process.running_process_scanner import RunningProcessScanner
from app.process.windows_process_filter import WindowsProcessFilter
from app.tray.tray_icon_manager import TrayIconManager
from app.ui.control_tray_icon import ControlTrayIcon
from app.ui.main_window import MainWindow
from app.window.minimize_event_hook import MinimizeEventHook
from app.window.window_controller import WindowController
from app.window.window_enumerator import WindowEnumerator


class Application:
    def __init__(self) -> None:
        self._qt_app = QApplication(sys.argv)
        self._qt_app.setQuitOnLastWindowClosed(False)

        # 모든 창의 타이틀 아이콘과 제어 트레이 아이콘에 공통 적용된다.
        self._app_icon = self._load_app_icon()
        self._qt_app.setWindowIcon(self._app_icon)

        # 설정은 생성 시점에 파일에서 로드되므로 재시작 후에도 유지된다.
        repository = SettingsRepository.default()
        settings = repository.load()
        self._store = TargetStore(repository, settings)
        self._startup = StartupOptions(repository, settings)
        icon_provider = ExecutableIconProvider()
        window_enumerator = WindowEnumerator()
        path_resolver = ProcessPathResolver()

        self._service = TrayMinimizeService(
            target_store=self._store,
            hook=MinimizeEventHook(),
            window_enumerator=window_enumerator,
            window_controller=WindowController(),
            path_resolver=path_resolver,
            tray_manager=TrayIconManager(icon_provider),
        )
        scanner = RunningProcessScanner(
            window_enumerator, path_resolver, WindowsProcessFilter(), own_pid=os.getpid()
        )

        self._window = MainWindow(icon_provider)
        self._window.set_start_minimized(self._startup.start_minimized)
        self._window.start_minimized_toggled.connect(self._startup.set_start_minimized)
        self._selection = ProcessSelectionController(
            self._window, scanner, self._store, self._service
        )
        self._control_tray = self._create_control_tray()

    def run(self) -> int:
        self._service.start()
        self._control_tray.show()
        if not self._startup.start_minimized:
            self._window.show()
        return self._qt_app.exec()

    def _load_app_icon(self) -> QIcon:
        fallback = self._qt_app.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
        return AppIconProvider().load(fallback)

    def _create_control_tray(self) -> ControlTrayIcon:
        tray = ControlTrayIcon(self._app_icon)
        tray.open_requested.connect(self._show_window)
        tray.quit_requested.connect(self._quit)
        return tray

    def _show_window(self) -> None:
        self._window.show()
        self._window.raise_()
        self._window.activateWindow()

    def _quit(self) -> None:
        self._service.shutdown()
        self._qt_app.quit()
