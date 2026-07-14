@echo off
chcp 65001 >nul
cd /d "%~dp0"
title AXdata - 33 character auto-generate (Pollinations)

echo Generating characters into out_gen ... (internet required, free)
echo.

REM python 을 바로 호출(직접 치면 되는 방식). 없으면(9009) py 로 폴백.
python "%~dp0scripts\gen_pollinations.py"
if errorlevel 9009 (
  echo.
  echo python not found, trying py launcher ...
  py "%~dp0scripts\gen_pollinations.py"
)

echo.
echo [OK] Done! Opening out_gen folder.
if exist "%~dp0out_gen" start "" "%~dp0out_gen"
pause
