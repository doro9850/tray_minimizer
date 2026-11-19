"""숨겨진 창 하나에 대응하는 트레이 아이콘."""
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMenu, QSystemTrayIcon


class TrayEntry(QObject):
    """클릭 또는 메뉴의 '복원' 선택 시 restore_requested(hwnd),
    메뉴의 '종료' 선택 시 close_requested(hwnd) 를 발생시킨다."""

    restore_requested = Signal(int)
    close_requested = Signal(int)

    _RESTORE_REASONS = (
        QSystemTrayIcon.ActivationReason.Trigger,
        QSystemTrayIcon.ActivationReason.DoubleClick,
    )

    def __init__(self, hwnd: int, title: str, icon: QIcon, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._hwnd = hwnd

        self._menu = QMenu()
        self._menu.addAction("복원").triggered.connect(self._request_restore)
        self._menu.addAction("종료").triggered.connect(self._request_close)

        self._tray = QSystemTrayIcon(icon, self)
        self._tray.setToolTip(title)
        self._tray.setContextMenu(self._menu)
        self._tray.activated.connect(self._on_activated)
        self._tray.show()

    def dispose(self) -> None:
        self._tray.hide()
        self._tray.deleteLater()
        self._menu.deleteLater()
        self.deleteLater()

    def _on_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason in self._RESTORE_REASONS:
            self._request_restore()

    def _request_restore(self, *_args) -> None:
        self.restore_requested.emit(self._hwnd)

    def _request_close(self, *_args) -> None:
        self.close_requested.emit(self._hwnd)
