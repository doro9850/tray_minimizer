"""트레이 최소화 대상 프로세스 집합. 변경 즉시 저장하고 변경 신호를 보낸다."""
from collections.abc import Iterable

from PySide6.QtCore import QObject, Signal

from app.config.app_settings import AppSettings
from app.config.settings_repository import SettingsRepository


class TargetStore(QObject):
    """대상 프로세스 키(정규화된 실행 파일 경로)를 보관한다.

    settings 인스턴스는 다른 설정 객체(StartupOptions 등)와 공유하므로
    저장 시 서로의 값을 덮어쓰지 않는다.
    """

    changed = Signal()

    def __init__(
        self,
        repository: SettingsRepository,
        settings: AppSettings,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._repository = repository
        self._settings = settings
        self._targets: set[str] = set(self._settings.tray_targets)

    @property
    def targets(self) -> frozenset[str]:
        return frozenset(self._targets)

    def is_target(self, key: str) -> bool:
        return key in self._targets

    def set_target(self, key: str, enabled: bool) -> None:
        if enabled == (key in self._targets):
            return
        if enabled:
            self._targets.add(key)
        else:
            self._targets.discard(key)
        self._commit()

    def keep_only(self, keys: Iterable[str]) -> None:
        """주어진 키에 해당하는 대상만 남기고 나머지는 해제한다."""
        remaining = self._targets & set(keys)
        if remaining == self._targets:
            return
        self._targets = remaining
        self._commit()

    def _commit(self) -> None:
        self._settings.tray_targets = sorted(self._targets)
        self._repository.save(self._settings)
        self.changed.emit()
