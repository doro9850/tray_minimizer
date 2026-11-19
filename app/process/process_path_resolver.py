"""PID 로부터 실행 파일 경로를 구한다."""
import psutil


class ProcessPathResolver:
    def resolve(self, pid: int) -> str | None:
        """종료되었거나 접근 불가한 프로세스는 None."""
        try:
            return psutil.Process(pid).exe() or None
        except (psutil.Error, OSError):
            return None
