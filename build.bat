pip install pyinstaller

if exist build rmdir /s /q build
if exist out rmdir /s /q out
pyinstaller ^
  --onedir ^
  --clean ^
  --noconsole ^
  --distpath ./out ^
  --workpath ./build ^
  --specpath ./build ^
  --name tray_minimizer ^
  --icon=../ico/tray_minimizer.ico ^
  --add-data "../ico/tray_minimizer.ico;ico" ^
  main.py