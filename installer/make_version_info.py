"""pyproject.toml 의 버전으로 PyInstaller 용 exe 버전 정보 파일을 생성한다.

사용법:  python installer\\make_version_info.py
결과물:  installer\\version_info.txt  (pyinstaller --version-file 에 전달)
"""
import re
from pathlib import Path

from pyproject_version import read_version

OUTPUT_PATH = Path(__file__).resolve().parent / "version_info.txt"

PRODUCT_NAME = "TrayMinimizer"
INTERNAL_NAME = "tray_minimizer"

TEMPLATE = """\
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={numbers},
    prodvers={numbers},
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable('040904B0', [
        StringStruct('FileDescription', '{product}'),
        StringStruct('FileVersion', '{text}'),
        StringStruct('InternalName', '{internal}'),
        StringStruct('OriginalFilename', '{internal}.exe'),
        StringStruct('ProductName', '{product}'),
        StringStruct('ProductVersion', '{text}')
      ])
    ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
"""


def to_version_numbers(version: str) -> tuple[int, int, int, int]:
    """'1.2.3' 또는 '1.2.3rc1' 같은 버전에서 숫자 부분만 뽑아 4개 정수로 맞춘다."""
    match = re.match(r"\d+(?:\.\d+)*", version)
    if match is None:
        raise ValueError(f"해석할 수 없는 버전입니다: {version!r}")
    numbers = [int(part) for part in match.group().split(".")][:4]
    numbers += [0] * (4 - len(numbers))
    return tuple(numbers)  # type: ignore[return-value]


def main() -> None:
    numbers = to_version_numbers(read_version())
    content = TEMPLATE.format(
        numbers=numbers,
        text=".".join(str(n) for n in numbers),
        product=PRODUCT_NAME,
        internal=INTERNAL_NAME,
    )
    OUTPUT_PATH.write_text(content, encoding="utf-8")
    print(f"버전 정보 파일 생성: {OUTPUT_PATH} ({numbers})")


if __name__ == "__main__":
    main()
