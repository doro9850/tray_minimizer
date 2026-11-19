"""대상 프로세스의 창이 최소화되면 트레이로 보내는 핵심 서비스."""
from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import QObject, QTimer

from app.config.target_store import TargetStore
from app.process.process_info import make_process_key
from app.process.process_path_resolver import ProcessPathResolver
from app.tray.tray_icon_manager import TrayIconManager
from app.window.minimize_event_hook import MinimizeEventHook
from app.window.window_controller import WindowController
from app.window.window_enumerator import WindowEnumerator


@dataclass(frozen=True)
class HiddenWindow:
    hwnd: int
    pid: int
    exe_path: str

    @property
    def key(self) -> str:
        return make_process_key(self.exe_path)


class TrayMinimizeService(QObject):
    _CLEANUP_INTERVAL_MS = 2000

    def __init__(
        self,
        target_store: TargetStore,
        hook: MinimizeEventHook,
        window_enumerator: WindowEnumerator,
        window_controller: WindowController,
        path_resolver: ProcessPathResolver,
        tray_manager: TrayIconManager,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._targets = target_store
        self._hook = hook
        self._enumerator = window_enumerator
        self._controller = window_controller
        self._resolver = path_resolver
        self._tray = tray_manager
        self._hidden: dict[int, HiddenWindow] = {}

        self._hook.window_minimized.connect(self._on_window_minimized)
        self._tray.restore_requested.connect(self.restore_window)
        self._targets.changed.connect(self._on_targets_changed)

        self._cleanup_timer = QTimer(self)
        self._cleanup_timer.setInterval(self._CLEANUP_INTERVAL_MS)
        self._cleanup_timer.timeout.connect(self._remove_dead_windows)

    def start(self) -> None:
        self._hook.start()
        self._cleanup_timer.start()

    def shutdown(self) -> None:
        """종료 시 트레이에 숨겨진 창을 모두 복원해 유실되지 않게 한다."""
        self._cleanup_timer.stop()
        self._hook.stop()
        for hwnd in list(self._hidden):
            self.restore_window(hwnd)

    def hidden_pids(self) -> set[int]:
        return {hidden.pid for hidden in self._hidden.values()}

    def restore_window(self, hwnd: int) -> None:
        if self._hidden.pop(hwnd, None) is None:
            return
        self._tray.remove(hwnd)
        if self._controller.is_alive(hwnd):
            self._controller.restore(hwnd)

    def _on_window_minimized(self, hwnd: int) -> None:
        if hwnd in self._hidden or not self._enumerator.is_app_window(hwnd):
            return

        pid = self._controller.pid_of(hwnd)
        exe_path = self._resolver.resolve(pid)
        if exe_path is None or not self._targets.is_target(make_process_key(exe_path)):
            return

        title = self._controller.title_of(hwnd) or Path(exe_path).name
        self._controller.hide(hwnd)
        self._hidden[hwnd] = HiddenWindow(hwnd, pid, exe_path)
        self._tray.add(hwnd, title, exe_path)

    def _on_targets_changed(self) -> None:
        """대상에서 해제된 프로세스의 숨겨진 창은 복원한다."""
        for hwnd, hidden in list(self._hidden.items()):
            if not self._targets.is_target(hidden.key):
                self.restore_window(hwnd)

    def _remove_dead_windows(self) -> None:
        for hwnd in list(self._hidden):
            if not self._controller.is_alive(hwnd):
                del self._hidden[hwnd]
                self._tray.remove(hwnd)
