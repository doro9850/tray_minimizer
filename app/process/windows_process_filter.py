"""Windows 운영체제 자체 프로세스 판별."""
import os

from app.process.process_info import make_process_key


class WindowsProcessFilter:
    """%SystemRoot%(보통 C:\\Windows) 아래에 있는 실행 파일을 Windows 프로세스로 본다.

    explorer.exe, ApplicationFrameHost.exe, SystemSettings.exe 등이 해당된다.
    """

    def __init__(self, windows_dir: str | None = None) -> None:
        root = windows_dir or os.environ.get("SystemRoot", r"C:\Windows")
        self._prefix = make_process_key(root) + os.sep

    def is_windows_process(self, exe_path: str) -> bool:
        return make_process_key(exe_path).startswith(self._prefix)
