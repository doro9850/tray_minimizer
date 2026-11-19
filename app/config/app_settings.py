"""앱 설정 데이터 모델."""
from dataclasses import dataclass, field


@dataclass
class AppSettings:
    """영속화 대상 설정.

    tray_targets: 트레이 최소화 대상 프로세스의 실행 파일 경로 목록.
    """

    tray_targets: list[str] = field(default_factory=list)
