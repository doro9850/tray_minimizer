"""프로젝트 버전의 단일 출처(pyproject.toml)를 읽는다."""
from pathlib import Path

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # Python 3.10: pip install tomli
    import tomli as tomllib

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"


def read_version() -> str:
    """pyproject.toml 의 [project] version 을 반환한다."""
    with PYPROJECT_PATH.open("rb") as file:
        return tomllib.load(file)["project"]["version"]
