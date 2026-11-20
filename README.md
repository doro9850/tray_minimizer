# tray_minimizer
Minimizing app to tray for Windows. Made by Claude Sonnet 5.5

### Requirements
- [Python](https://www.python.org) >= 3.10.0
- [PySide6](https://pypi.org/project/PySide6/) >= 6.6
- [psutil](https://pypi.org/project/psutil/) >= 5.9
<br><br>

### Environment Setup
Follow the next step to launch venv & upgrade pip and installing dependencies.
- Terminal
```
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -e .

```

### Build
- Terminal
```
build.bat
```

### Installer Build
#### Requirements
- [Inno Setup](https://jrsoftware.org/inno-setup) >= 7.0
```
installer.bat
```
