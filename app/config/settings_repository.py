"""설정 파일(JSON) 읽기/쓰기."""
import json
import logging
import os
from dataclasses import asdict
from pathlib import Path

from app.config.app_settings import AppSettings

logger = logging.getLogger(__name__)


class SettingsRepository:
    """설정을 JSON 파일로 영속화한다."""

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    @classmethod
    def default(cls) -> "SettingsRepository":
        """%APPDATA%/TrayMinimizer/settings.json 을 사용하는 저장소."""
        base_dir = Path(os.environ.get("APPDATA", Path.home()))
        return cls(base_dir / "TrayMinimizer" / "settings.json")

    def load(self) -> AppSettings:
        """파일이 없거나 손상되었으면 기본 설정을 반환한다."""
        try:
            data = json.loads(self._file_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return AppSettings()

        if not isinstance(data, dict):
            return AppSettings()
        targets = data.get("tray_targets", [])
        if not isinstance(targets, list):
            return AppSettings()
        return AppSettings(tray_targets=[t for t in targets if isinstance(t, str)])

    def save(self, settings: AppSettings) -> None:
        """임시 파일에 쓴 뒤 교체하여 저장 도중 손상을 방지한다."""
        payload = json.dumps(asdict(settings), ensure_ascii=False, indent=2)
        temp_path = self._file_path.with_suffix(".tmp")
        try:
            self._file_path.parent.mkdir(parents=True, exist_ok=True)
            temp_path.write_text(payload, encoding="utf-8")
            temp_path.replace(self._file_path)
        except OSError:
            logger.exception("설정 저장 실패: %s", self._file_path)
