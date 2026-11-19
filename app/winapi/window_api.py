"""윈도우 핸들(hwnd) 단위 Win32 호출 래퍼."""
import ctypes
from ctypes import wintypes

from app.winapi.user32 import (
    GW_OWNER,
    GWL_EXSTYLE,
    SW_HIDE,
    SW_RESTORE,
    WS_EX_TOOLWINDOW,
    EnumWindowsProc,
    user32,
)


def enum_top_level_windows() -> list[int]:
    """모든 최상위 윈도우 핸들을 반환한다."""
    handles: list[int] = []

    def collect(hwnd: int, _lparam: int) -> bool:
        handles.append(hwnd)
        return True

    callback = EnumWindowsProc(collect)
    user32.EnumWindows(callback, 0)
    return handles


def is_window(hwnd: int) -> bool:
    return bool(user32.IsWindow(hwnd))


def is_visible(hwnd: int) -> bool:
    return bool(user32.IsWindowVisible(hwnd))


def has_owner(hwnd: int) -> bool:
    return bool(user32.GetWindow(hwnd, GW_OWNER))


def is_tool_window(hwnd: int) -> bool:
    return bool(user32.GetWindowLongW(hwnd, GWL_EXSTYLE) & WS_EX_TOOLWINDOW)


def get_title(hwnd: int) -> str:
    length = user32.GetWindowTextLengthW(hwnd)
    if length <= 0:
        return ""
    buffer = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buffer, length + 1)
    return buffer.value


def get_pid(hwnd: int) -> int:
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return pid.value


def hide_window(hwnd: int) -> None:
    user32.ShowWindow(hwnd, SW_HIDE)


def restore_window(hwnd: int) -> None:
    """숨겨진 최소화 창을 원래 크기로 복원하고 전면으로 가져온다."""
    user32.ShowWindow(hwnd, SW_RESTORE)
    user32.SetForegroundWindow(hwnd)
