@echo off
chcp 65001 >nul
cd /d "%~dp0"
title AXdata - 33 char generate (OpenAI / DALL-E 3 full)

REM 풀 품질 DALL-E 3 (약 $0.04/장, 33장 ~1300원). hd 로 바꾸면 더 고품질($0.08).
set "OPENAI_MODEL=dall-e-3"
set "OPENAI_QUALITY=standard"
set "SPRITE_OUT=%~dp0out_openai_full"

if "%OPENAI_API_KEY%"=="" set /p OPENAI_API_KEY=OpenAI API key 붙여넣고 Enter:
if "%OPENAI_API_KEY%"=="" ( echo [ERROR] API key not entered. & pause & exit /b 1 )

echo Generating with OpenAI (DALL-E 3, %OPENAI_QUALITY%) into out_openai_full ...
echo.
python "%~dp0scripts\gen_openai.py"
if errorlevel 9009 py "%~dp0scripts\gen_openai.py"

echo.
echo [OK] Done! Opening out_openai_full folder.
if exist "%~dp0out_openai_full" start "" "%~dp0out_openai_full"
pause
