@echo off
echo ==========================================
echo  Building University Database System .exe
echo ==========================================
echo.
pyinstaller --onefile --windowed --name UniversityDB main.py
echo.
echo Build complete! Executable is in the dist\ folder.
pause
