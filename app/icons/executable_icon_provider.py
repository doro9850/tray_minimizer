"""실행 파일의 아이콘을 가져온다(트레이 아이콘 자동 지정에 사용)."""
from PySide6.QtCore import QFileInfo
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileIconProvider


class ExecutableIconProvider:
    def __init__(self) -> None:
        self._provider = QFileIconProvider()
        self._cache: dict[str, QIcon] = {}

    def icon_for(self, exe_path: str) -> QIcon:
        if exe_path not in self._cache:
            self._cache[exe_path] = self._provider.icon(QFileInfo(exe_path))
        return self._cache[exe_path]
