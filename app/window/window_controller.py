"""개별 윈도우에 대한 조작/조회."""
from app.winapi import window_api


class WindowController:
    def hide(self, hwnd: int) -> None:
        window_api.hide_window(hwnd)

    def restore(self, hwnd: int) -> None:
        window_api.restore_window(hwnd)

    def is_alive(self, hwnd: int) -> bool:
        return window_api.is_window(hwnd)

    def title_of(self, hwnd: int) -> str:
        return window_api.get_title(hwnd)

    def pid_of(self, hwnd: int) -> int:
        return window_api.get_pid(hwnd)
