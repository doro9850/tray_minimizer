"""프로그램 자체를 제어하는 트레이 아이콘(설정 열기 / 종료)."""
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMenu, QSystemTrayIcon


class ControlTrayIcon(QObject):
    open_requested = Signal()
    quit_requested = Signal()

    def __init__(self, icon: QIcon, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._menu = QMenu()
        self._menu.addAction("설정 열기").triggered.connect(self.open_requested)
        self._menu.addAction("종료").triggered.connect(self.quit_requested)

        self._tray = QSystemTrayIcon(icon, self)
        self._tray.setToolTip("트레이 최소화")
        self._tray.setContextMenu(self._menu)
        self._tray.activated.connect(self._on_activated)

    def show(self) -> None:
        self._tray.show()

    def _on_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.open_requested.emit()
