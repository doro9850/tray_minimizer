"""창 핸들별 트레이 아이콘 생성/제거 관리."""
from PySide6.QtCore import QObject, Signal

from app.icons.executable_icon_provider import ExecutableIconProvider
from app.tray.tray_entry import TrayEntry


class TrayIconManager(QObject):
    restore_requested = Signal(int)

    def __init__(self, icon_provider: ExecutableIconProvider, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._icon_provider = icon_provider
        self._entries: dict[int, TrayEntry] = {}

    def add(self, hwnd: int, title: str, exe_path: str) -> None:
        if hwnd in self._entries:
            return
        entry = TrayEntry(hwnd, title, self._icon_provider.icon_for(exe_path), self)
        entry.restore_requested.connect(self.restore_requested)
        self._entries[hwnd] = entry

    def remove(self, hwnd: int) -> None:
        entry = self._entries.pop(hwnd, None)
        if entry is not None:
            entry.dispose()
