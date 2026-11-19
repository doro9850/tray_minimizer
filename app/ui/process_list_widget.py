"""체크박스로 프로세스를 선택하는 목록 위젯."""

from collections.abc import Iterable

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QWidget

from app.icons.executable_icon_provider import ExecutableIconProvider
from app.process.process_info import ProcessInfo


class ProcessListWidget(QListWidget):
    """체크 상태가 바뀌면 target_toggled(key, checked) 를 발생시킨다."""

    target_toggled = Signal(str, bool)

    _KEY_ROLE = Qt.ItemDataRole.UserRole

    def __init__(
        self,
        icon_provider: ExecutableIconProvider,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._icon_provider = icon_provider
        self.itemChanged.connect(self._on_item_changed)
        # 체크박스 토글은 모두 이 핸들러가 담당한다(이름/아이콘/체크박스 어디를 눌러도 동일).
        self.itemClicked.connect(self._toggle_item)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        """더블클릭을 일반 클릭으로 처리한다.

        더블클릭 시간(Windows 기본 500ms) 안의 두 번째 클릭은 clicked 가 아니라
        doubleClicked 로 전달되어 토글이 누락되므로, 누름 이벤트로 넘겨 이후 release 에서
        itemClicked 가 발생하게 한다.
        """
        self.mousePressEvent(event)

    def show_processes(
        self,
        processes: Iterable[ProcessInfo],
        checked_keys: Iterable[str],
    ) -> None:
        checked = set(checked_keys)
        self.blockSignals(True)
        try:
            self.clear()
            for process in processes:
                self.addItem(
                    self._create_item(process, process.key in checked)
                )
        finally:
            self.blockSignals(False)

    def listed_keys(self) -> set[str]:
        return {
            self.item(i).data(self._KEY_ROLE)
            for i in range(self.count())
        }

    def _create_item(
        self, process: ProcessInfo, checked: bool
    ) -> QListWidgetItem:
        item = QListWidgetItem(
            self._icon_provider.icon_for(process.exe_path), process.name
        )
        item.setToolTip(process.exe_path)
        item.setData(self._KEY_ROLE, process.key)
        # QListWidgetItem 은 ItemIsUserCheckable 이 기본으로 켜져 있으므로 명시적으로 끈다.
        # 기본 체크박스 클릭과 항목 클릭(itemClicked)이 겹쳐 두 번 토글되는 것을 막고,
        # 토글을 _toggle_item 한 곳으로 모으기 위함.
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(
            Qt.CheckState.Checked
            if checked
            else Qt.CheckState.Unchecked
        )
        return item

    @staticmethod
    def _toggle_item(item: QListWidgetItem) -> None:
        is_checked = item.checkState() == Qt.CheckState.Checked
        item.setCheckState(
            Qt.CheckState.Unchecked
            if is_checked
            else Qt.CheckState.Checked
        )

    def _on_item_changed(self, item: QListWidgetItem) -> None:
        checked = item.checkState() == Qt.CheckState.Checked
        self.target_toggled.emit(item.data(self._KEY_ROLE), checked)
