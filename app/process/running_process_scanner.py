"""현재 실행 중인 선택 가능 프로세스 목록 생성."""
from collections.abc import Iterable

from app.process.process_info import ProcessInfo
from app.process.process_path_resolver import ProcessPathResolver
from app.process.windows_process_filter import WindowsProcessFilter
from app.window.window_enumerator import WindowEnumerator


class RunningProcessScanner:
    """창을 가진 실행 중 프로세스에서 Windows 프로세스와 자기 자신을 제외해 반환한다."""

    def __init__(
        self,
        window_enumerator: WindowEnumerator,
        path_resolver: ProcessPathResolver,
        windows_filter: WindowsProcessFilter,
        own_pid: int,
    ) -> None:
        self._enumerator = window_enumerator
        self._resolver = path_resolver
        self._filter = windows_filter
        self._own_pid = own_pid

    def scan(self, extra_pids: Iterable[int] = ()) -> list[ProcessInfo]:
        """extra_pids: 창이 트레이에 숨겨져 목록에서 보이지 않는 실행 중 프로세스."""
        pids = {window.pid for window in self._enumerator.list_app_windows()}
        pids.update(extra_pids)
        pids.discard(self._own_pid)

        found: dict[str, ProcessInfo] = {}
        for pid in pids:
            exe_path = self._resolver.resolve(pid)
            if exe_path is None or self._filter.is_windows_process(exe_path):
                continue
            info = ProcessInfo.from_exe_path(exe_path)
            found.setdefault(info.key, info)
        return sorted(found.values(), key=lambda p: p.name.lower())
