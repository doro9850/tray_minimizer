"""시작 옵션(시작 시 최소화 여부). 변경 즉시 저장한다."""
from app.config.app_settings import AppSettings
from app.config.settings_repository import SettingsRepository


class StartupOptions:
    """settings 인스턴스는 TargetStore 와 공유한다."""

    def __init__(self, repository: SettingsRepository, settings: AppSettings) -> None:
        self._repository = repository
        self._settings = settings

    @property
    def start_minimized(self) -> bool:
        return self._settings.start_minimized

    def set_start_minimized(self, enabled: bool) -> None:
        if enabled == self._settings.start_minimized:
            return
        self._settings.start_minimized = enabled
        self._repository.save(self._settings)
