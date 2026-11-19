"""시스템 전역 창 최소화 이벤트를 Qt 시그널로 전달한다."""
from PySide6.QtCore import QObject, Signal

from app.winapi import win_event_api
from app.winapi.user32 import OBJID_WINDOW, WinEventProc


class MinimizeEventHook(QObject):
    """창이 최소화되기 시작할 때 window_minimized(hwnd) 를 발생시킨다."""

    window_minimized = Signal(int)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        # ctypes 콜백은 참조를 유지해야 GC 되지 않는다.
        self._callback = WinEventProc(self._on_event)
        self._handle: int | None = None

    def start(self) -> None:
        if self._handle is None:
            self._handle = win_event_api.install_minimize_hook(self._callback)

    def stop(self) -> None:
        if self._handle is not None:
            win_event_api.uninstall_hook(self._handle)
            self._handle = None

    def _on_event(self, _hook, _event, hwnd, id_object, _id_child, _thread, _time) -> None:
        if hwnd and id_object == OBJID_WINDOW:
            self.window_minimized.emit(int(hwnd))
