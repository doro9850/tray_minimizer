"""SetWinEventHook 기반 최소화 이벤트 훅 래퍼."""
from app.winapi.user32 import (
    EVENT_SYSTEM_MINIMIZESTART,
    WINEVENT_OUTOFCONTEXT,
    WINEVENT_SKIPOWNPROCESS,
    WinEventProc,
    user32,
)


def install_minimize_hook(callback: WinEventProc) -> int:
    """창 최소화 시작 이벤트 훅을 설치하고 훅 핸들을 반환한다.

    호출한 스레드에 메시지 루프(Qt 이벤트 루프)가 있어야 콜백이 전달된다.
    """
    handle = user32.SetWinEventHook(
        EVENT_SYSTEM_MINIMIZESTART,
        EVENT_SYSTEM_MINIMIZESTART,
        None,
        callback,
        0,
        0,
        WINEVENT_OUTOFCONTEXT | WINEVENT_SKIPOWNPROCESS,
    )
    if not handle:
        raise OSError("SetWinEventHook 호출에 실패했습니다.")
    return handle


def uninstall_hook(handle: int) -> None:
    user32.UnhookWinEvent(handle)
