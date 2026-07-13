@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
set "BLENDER=C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"
set "SPRITE_INPUT=%~dp0input"
set "SPRITE_OUT=%~dp0out"
echo input 폴더의 3D 파일을 모두 렌더합니다...
echo.
"%BLENDER%" --background --python "%~dp0scripts\render_folder.py"
echo.
echo [OK] 완료! 결과 폴더를 엽니다.
if exist "%~dp0out" start "" "%~dp0out"
pause
