@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "BLENDER=C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"

echo ================================================
echo   매핑 기반 렌더 (게임 이름 + 속성색)
echo ================================================
echo   [1] 색 입힘   (속성색 틴트 ON  - 기본)
echo   [2] 색 없음   (원본 그대로     - 색 에러시 사용)
echo ================================================
set "SPRITE_TINT=1"
set /p sel="번호 선택 후 Enter (그냥 Enter = 1): "
if "%sel%"=="2" set "SPRITE_TINT=0"

echo.
if "%SPRITE_TINT%"=="0" (echo 색 없이 원본으로 렌더합니다...) else (echo 속성색을 입혀 렌더합니다...)
echo.
"%BLENDER%" --background --python "%~dp0scripts\render_roster.py"
echo.
echo [OK] 완료! out_roster 폴더를 엽니다.
if exist "%~dp0out_roster" start "" "%~dp0out_roster"
pause
