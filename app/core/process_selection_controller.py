"""메인 창, 프로세스 스캐너, 대상 저장소를 연결한다."""
from PySide6.QtCore import QObject

from app.config.target_store import TargetStore
from app.core.tray_minimize_service import TrayMinimizeService
from app.process.running_process_scanner import RunningProcessScanner
from app.ui.main_window import MainWindow


class ProcessSelectionController(QObject):
    def __init__(
        self,
        window: MainWindow,
        scanner: RunningProcessScanner,
        target_store: TargetStore,
        service: TrayMinimizeService,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._window = window
        self._scanner = scanner
        self._store = target_store
        self._service = service

        window.refresh_requested.connect(self.refresh)
        window.target_toggled.connect(self._on_target_toggled)
        window.clear_inactive_requested.connect(self._clear_inactive)

    def refresh(self) -> None:
        processes = self._scanner.scan(extra_pids=self._service.hidden_pids())
        self._window.show_processes(processes, self._store.targets)
        self._update_inactive_count()

    def _on_target_toggled(self, key: str, enabled: bool) -> None:
        self._store.set_target(key, enabled)
        self._update_inactive_count()

    def _clear_inactive(self) -> None:
        self._store.keep_only(self._window.listed_keys())
        self._update_inactive_count()

    def _update_inactive_count(self) -> None:
        inactive = self._store.targets - self._window.listed_keys()
        self._window.set_inactive_count(len(inactive))
