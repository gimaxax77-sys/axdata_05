@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0"

REM ===== Blender 경로 (설치 위치 다르면 이 줄만 수정) =====
set "BLENDER=C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"
REM =====================================================

:menu
cls
echo ================================
echo     스프라이트 렌더 도구
echo ================================
echo   [1] 전체 영웅 6종
echo   [2] Knight
echo   [3] Barbarian
echo   [4] Mage
echo   [5] Rogue
echo   [6] Rogue_Hooded
echo   [7] Ranger
echo   [8] 직접 입력
echo   [0] 종료
echo.
set "SPRITE_BODIES="
set /p sel=캐릭터 번호: 
if "!sel!"=="0" exit /b
if "!sel!"=="1" set "SPRITE_BODIES=Knight,Barbarian,Mage,Rogue,Rogue_Hooded,Ranger"
if "!sel!"=="2" set "SPRITE_BODIES=Knight"
if "!sel!"=="3" set "SPRITE_BODIES=Barbarian"
if "!sel!"=="4" set "SPRITE_BODIES=Mage"
if "!sel!"=="5" set "SPRITE_BODIES=Rogue"
if "!sel!"=="6" set "SPRITE_BODIES=Rogue_Hooded"
if "!sel!"=="7" set "SPRITE_BODIES=Ranger"
if "!sel!"=="8" set /p SPRITE_BODIES=캐릭터 이름(쉼표로 여러개): 
if "!SPRITE_BODIES!"=="" ( echo [!] 잘못된 선택입니다. & pause & goto menu )

set "SPRITE_ACTIONS="
set /p SPRITE_ACTIONS=동작 입력 (엔터=Idle): 
if "!SPRITE_ACTIONS!"=="" set "SPRITE_ACTIONS=Idle"

echo.
echo ^>^> 렌더 시작: !SPRITE_BODIES!  /  !SPRITE_ACTIONS!
echo.
"!BLENDER!" --background --python "%~dp0scripts\render_sprites.py"

echo.
echo [OK] 완료! 결과 폴더를 엽니다.
if exist "%~dp0out" start "" "%~dp0out"
echo.
echo 계속하려면 아무 키, 종료는 메뉴에서 [0].
pause >nul
goto menu
