@echo off
chcp 65001 >nul
cd /d "%~dp0"
title AXdata - 33 char generate (OpenAI / gpt-image-1 mini)

if "%OPENAI_API_KEY%"=="" set /p OPENAI_API_KEY=OpenAI API key 붙여넣고 Enter:
if "%OPENAI_API_KEY%"=="" ( echo [ERROR] API key not entered. & pause & exit /b 1 )

echo Generating with OpenAI (gpt-image-1 mini) into out_openai ...
echo.
python "%~dp0scripts\gen_openai.py"
if errorlevel 9009 py "%~dp0scripts\gen_openai.py"

echo.
echo [OK] Done! Opening out_openai folder.
if exist "%~dp0out_openai" start "" "%~dp0out_openai"
pause
