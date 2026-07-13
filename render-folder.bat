@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
set "BLENDER=C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"
set "SPRITE_INPUT=%~dp0input"
set "SPRITE_OUT=%~dp0out"

echo ================================================
echo   Folder render - pick facing
echo   (if character looks sideways/back, re-run and try another)
echo ================================================
echo   [1] front Y  (0,1,0)   default - KayKit
echo   [2] front X  (1,0,0)   - many Tripo/AI models
echo   [3] back  X  (-1,0,0)
echo   [4] back  Y  (0,-1,0)
echo ================================================
set "SPRITE_DIR=0,1,0"
set /p f="Select then Enter (Enter = 1): "
if "%f%"=="2" set "SPRITE_DIR=1,0,0"
if "%f%"=="3" set "SPRITE_DIR=-1,0,0"
if "%f%"=="4" set "SPRITE_DIR=0,-1,0"

echo.
echo Rendering all 3D files in the input folder... (facing %SPRITE_DIR%)
echo.
"%BLENDER%" --background --python "%~dp0scripts\render_folder.py"
echo.
echo [OK] Done! Opening the out folder.
if exist "%~dp0out" start "" "%~dp0out"
pause
