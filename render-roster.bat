@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "BLENDER=C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"
echo 매핑(character_map.csv) 기반으로 게임 이름 + 속성색으로 렌더합니다...
echo.
"%BLENDER%" --background --python "%~dp0scripts\render_roster.py"
echo.
echo [OK] 완료! out_roster 폴더를 엽니다.
if exist "%~dp0out_roster" start "" "%~dp0out_roster"
pause
