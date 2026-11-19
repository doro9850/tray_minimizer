"""트레이 최소화 프로그램 진입점."""

import sys


def main() -> int:
    if sys.platform != "win32":
        print("이 프로그램은 Windows 에서만 동작합니다.")
        return 1

    from app.application import Application

    return Application().run()


if __name__ == "__main__":
    sys.exit(main())
