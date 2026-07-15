@echo off
chcp 65001 >nul
cd /d "%~dp0"
title AXdata - 33 char generate (Together / Flux)

if "%TOGETHER_API_KEY%"=="" set /p TOGETHER_API_KEY=Together API key 붙여넣고 Enter:
if "%TOGETHER_API_KEY%"=="" ( echo [ERROR] API key not entered. & pause & exit /b 1 )

echo Generating with Together (Flux) into out_together ...
echo.
python "%~dp0scripts\gen_together.py"
if errorlevel 9009 py "%~dp0scripts\gen_together.py"

echo.
echo [OK] Done! Opening out_together folder.
if exist "%~dp0out_together" start "" "%~dp0out_together"
pause
