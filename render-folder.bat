@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
set "BLENDER=C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"
set "SPRITE_INPUT=%~dp0input"
set "SPRITE_OUT=%~dp0out"
echo Rendering all 3D files in the input folder...
echo.
"%BLENDER%" --background --python "%~dp0scripts\render_folder.py"
echo.
echo [OK] Done! Opening the out folder.
if exist "%~dp0out" start "" "%~dp0out"
pause
