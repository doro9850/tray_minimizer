"""프로세스 선택 메인 창."""
from collections.abc import Iterable

from PySide6.QtCore import Signal
from PySide6.QtGui import QCloseEvent, QShowEvent
from PySide6.QtWidgets import QHBoxLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget

from app.icons.executable_icon_provider import ExecutableIconProvider
from app.process.process_info import ProcessInfo
from app.ui.process_list_widget import ProcessListWidget


class MainWindow(QMainWindow):
    """뷰 역할만 수행하며 동작은 시그널로 외부에 위임한다."""

    refresh_requested = Signal()
    clear_inactive_requested = Signal()
    target_toggled = Signal(str, bool)

    def __init__(self, icon_provider: ExecutableIconProvider) -> None:
        super().__init__()
        self.setWindowTitle("트레이 최소화")
        self.resize(420, 520)

        self._list = ProcessListWidget(icon_provider)
        self._list.target_toggled.connect(self.target_toggled)

        self._inactive_label = QLabel()
        self._clear_button = QPushButton("미실행 항목 해제")
        self._clear_button.clicked.connect(self.clear_inactive_requested)
        refresh_button = QPushButton("새로고침")
        refresh_button.clicked.connect(self.refresh_requested)

        self.setCentralWidget(self._build_layout(refresh_button))
        self.set_inactive_count(0)

    def show_processes(self, processes: Iterable[ProcessInfo], checked_keys: Iterable[str]) -> None:
        self._list.show_processes(processes, checked_keys)

    def listed_keys(self) -> set[str]:
        return self._list.listed_keys()

    def set_inactive_count(self, count: int) -> None:
        """실행 중이 아니지만 등록되어 있는 항목 수를 표시한다."""
        self._inactive_label.setText(f"실행 중이 아닌 등록 항목: {count}개 (실행 시 자동 적용)")
        self._clear_button.setEnabled(count > 0)

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        self.refresh_requested.emit()

    def closeEvent(self, event: QCloseEvent) -> None:
        """창을 닫아도 프로그램은 종료하지 않고 숨기기만 한다."""
        event.ignore()
        self.hide()

    def _build_layout(self, refresh_button: QPushButton) -> QWidget:
        guide = QLabel("트레이로 최소화할 프로세스를 체크하세요.\n(Windows 기본 프로세스는 표시되지 않습니다)")

        footer = QHBoxLayout()
        footer.addWidget(self._inactive_label, stretch=1)
        footer.addWidget(self._clear_button)

        layout = QVBoxLayout()
        layout.addWidget(guide)
        layout.addWidget(self._list, stretch=1)
        layout.addLayout(footer)
        layout.addWidget(refresh_button)

        container = QWidget()
        container.setLayout(layout)
        return container
