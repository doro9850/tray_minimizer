"""프로그램 고유 아이콘(창 타이틀, 제어 트레이)을 제공한다."""
from pathlib import Path

from PySide6.QtGui import QIcon

# 프로젝트 루트(main.py 가 있는 폴더) 기준 ico/tray_minimizer.ico
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_ICON_PATH = _PROJECT_ROOT / "ico" / "tray_minimizer.ico"


class AppIconProvider:
    def __init__(self, icon_path: Path = APP_ICON_PATH) -> None:
        self._icon_path = icon_path

    def load(self, fallback: QIcon) -> QIcon:
        """아이콘 파일이 없거나 읽을 수 없으면 fallback 을 반환한다."""
        icon = QIcon(str(self._icon_path))
        return fallback if icon.isNull() else icon
