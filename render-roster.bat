@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "BLENDER=C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"

echo ================================================
echo   Mapped render (game name + element color)
echo ================================================
echo   [1] With color  (element tint ON  - default)
echo   [2] No color    (original         - if tint errors)
echo ================================================
set "SPRITE_TINT=1"
set /p sel="Select then Enter (Enter = 1): "
if "%sel%"=="2" set "SPRITE_TINT=0"

echo.
if "%SPRITE_TINT%"=="0" (echo Rendering without color...) else (echo Rendering with element color...)
echo.
"%BLENDER%" --background --python "%~dp0scripts\render_roster.py"
echo.
echo [OK] Done! Opening out_roster folder.
if exist "%~dp0out_roster" start "" "%~dp0out_roster"
pause
