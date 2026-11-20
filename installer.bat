@echo off
setlocal

rem Build the installer with the Inno Setup command-line compiler (ISCC.exe).
rem Prerequisite: PyInstaller onedir output in out\tray_minimizer\
rem The version is read from pyproject.toml (single source) and passed as /DAppVersion.

cd /d "%~dp0"

set "DIST_DIR=out\tray_minimizer"
set "ISS_FILE=installer\tray_minimizer.iss"

if not exist "%DIST_DIR%\" (
    echo [ERROR] "%DIST_DIR%" not found. Run the PyInstaller build first.
    exit /b 1
)

rem --- Locate ISCC.exe (PATH first, then the default install folders) ---
set "ISCC="
where iscc >nul 2>&1 && set "ISCC=iscc"
if not defined ISCC if exist "%ProgramFiles(x86)%\Inno Setup 7\ISCC.exe" set "ISCC=%ProgramFiles(x86)%\Inno Setup 7\ISCC.exe"
if not defined ISCC if exist "%ProgramFiles%\Inno Setup 7\ISCC.exe" set "ISCC=%ProgramFiles%\Inno Setup 7\ISCC.exe"
if not defined ISCC if exist "%LOCALAPPDATA%\Programs\Inno Setup 7\ISCC.exe" set "ISCC=%LOCALAPPDATA%\Programs\Inno Setup 7\ISCC.exe"
if not defined ISCC (
    echo [ERROR] ISCC.exe not found. Install Inno Setup 6.3 or later, or add it to PATH.
    exit /b 1
)

rem --- Read the version from pyproject.toml ---
set "APP_VERSION="
for /f "usebackq delims=" %%V in (`python -c "import sys; sys.path.insert(0, 'installer'); from pyproject_version import read_version; print(read_version())"`) do set "APP_VERSION=%%V"
if not defined APP_VERSION (
    echo [ERROR] Could not read the version from pyproject.toml. On Python 3.10, run: pip install tomli
    exit /b 1
)

echo Building installer for version %APP_VERSION% ...
"%ISCC%" "/DAppVersion=%APP_VERSION%" "%ISS_FILE%"
if errorlevel 1 (
    echo [ERROR] Inno Setup compile failed.
    exit /b 1
)

echo.
echo Done: installer\Output\TrayMinimizer_Setup_%APP_VERSION%.exe
endlocal
