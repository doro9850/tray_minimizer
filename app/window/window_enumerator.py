"""사용자에게 보이는 일반 애플리케이션 창 조회."""
from dataclasses import dataclass

from app.winapi import window_api


@dataclass(frozen=True)
class WindowInfo:
    hwnd: int
    pid: int
    title: str


class WindowEnumerator:
    def is_app_window(self, hwnd: int) -> bool:
        """보이는 최상위 창이며 소유자/도구창이 아닌 일반 앱 창인지 판단한다."""
        return (
            window_api.is_visible(hwnd)
            and not window_api.has_owner(hwnd)
            and not window_api.is_tool_window(hwnd)
        )

    def list_app_windows(self) -> list[WindowInfo]:
        """제목이 있는 일반 앱 창 목록."""
        windows: list[WindowInfo] = []
        for hwnd in window_api.enum_top_level_windows():
            if not self.is_app_window(hwnd):
                continue
            title = window_api.get_title(hwnd)
            if title:
                windows.append(WindowInfo(hwnd, window_api.get_pid(hwnd), title))
        return windows
