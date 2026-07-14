@echo off
chcp 65001 >nul
cd /d "%~dp0"
title AXdata - 33 character auto-generate (Pollinations)

where python >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Python is not installed.
  echo   Install: https://www.python.org/downloads/  (check "Add python.exe to PATH")
  echo   Then run this again.
  pause & exit /b 1
)

echo Generating 33 characters into out_gen ... (internet required, free)
echo.
python "%~dp0scripts\gen_pollinations.py"
echo.
echo [OK] Done! Opening out_gen folder.
if exist "%~dp0out_gen" start "" "%~dp0out_gen"
pause
