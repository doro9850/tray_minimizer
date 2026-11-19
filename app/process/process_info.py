"""프로세스 식별 모델.

같은 실행 파일은 하나의 항목으로 취급하며, 실행 파일 경로를 정규화한 값을 키로 쓴다.
"""
import os
from dataclasses import dataclass
from pathlib import Path


def make_process_key(exe_path: str) -> str:
    """대소문자/구분자 차이를 제거한 실행 파일 경로 키."""
    return os.path.normcase(os.path.normpath(exe_path))


@dataclass(frozen=True)
class ProcessInfo:
    key: str
    exe_path: str

    @property
    def name(self) -> str:
        return Path(self.exe_path).name

    @classmethod
    def from_exe_path(cls, exe_path: str) -> "ProcessInfo":
        return cls(key=make_process_key(exe_path), exe_path=exe_path)
