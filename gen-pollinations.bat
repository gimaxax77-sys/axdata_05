@echo off
chcp 65001 >nul
cd /d "%~dp0"
title AXdata - 33 character auto-generate (Pollinations)

set "PY="
where python >nul 2>&1 && set "PY=python"
if not defined PY ( where py >nul 2>&1 && set "PY=py" )
if not defined PY (
  echo [ERROR] Python not found (neither 'python' nor 'py').
  echo   Install: https://www.python.org/downloads/  (check "Add python.exe to PATH")
  echo   Or restart this window after installing, then run again.
  pause & exit /b 1
)

echo Generating 33 characters into out_gen ... (internet required, free)
echo   using: %PY%
echo.
"%PY%" "%~dp0scripts\gen_pollinations.py"
echo.
echo [OK] Done! Opening out_gen folder.
if exist "%~dp0out_gen" start "" "%~dp0out_gen"
pause
