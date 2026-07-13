@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
set "BLENDER=C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"
set "SPRITE_INPUT=%~dp0input"
set "SPRITE_OUT=%~dp0out"

echo ================================================
echo   Folder render - pick facing
echo ================================================
echo   [1] ALL 4 directions (auto)   <- easiest, pick the good one
echo   [2] front Y  (0,1,0)   default - KayKit
echo   [3] front X  (1,0,0)   - many Tripo/AI models
echo   [4] back  X  (-1,0,0)
echo   [5] back  Y  (0,-1,0)
echo ================================================
set "SPRITE_DIR=ALL"
set /p f="Select then Enter (Enter = 1 = ALL): "
if "%f%"=="2" set "SPRITE_DIR=0,1,0"
if "%f%"=="3" set "SPRITE_DIR=1,0,0"
if "%f%"=="4" set "SPRITE_DIR=-1,0,0"
if "%f%"=="5" set "SPRITE_DIR=0,-1,0"

echo.
echo Rendering input folder... (facing %SPRITE_DIR%)
if "%SPRITE_DIR%"=="ALL" echo   Output per file: name_Yp / name_Ym / name_Xp / name_Xm .png
echo.
"%BLENDER%" --background --python "%~dp0scripts\render_folder.py"
echo.
echo [OK] Done! Opening the out folder.
if exist "%~dp0out" start "" "%~dp0out"
pause
