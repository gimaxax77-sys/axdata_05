@echo off
chcp 65001 >nul
cd /d "%~dp0"
title AXdata 렌더 - 업데이트
REM ── 최신 커밋 받기 (ZIP 재다운로드 대신 이 버튼 하나) ──

set "REPO_URL=https://github.com/gimaxax77-sys/axdata_05.git"

echo ==================================================
echo    AXdata 렌더 도구  -  최신 커밋 받기
echo ==================================================
echo.

REM git 설치 확인
where git >nul 2>&1
if errorlevel 1 (
  echo [ERROR] git 이 설치되어 있지 않습니다.
  echo   https://git-scm.com/download/win 에서 설치 후 다시 실행하세요.
  pause & exit /b 1
)

if exist "%~dp0.git" goto pull

REM ── 최초 1회: ZIP 폴더를 저장소와 연결 ──
echo [최초 1회] 이 폴더를 저장소와 연결합니다...
echo   (character_map.csv 등 직접 넣은 파일은 지워지지 않습니다)
echo.
git init >nul
git remote remove origin >nul 2>&1
git remote add origin "%REPO_URL%"
git fetch origin main
if errorlevel 1 (
  echo [ERROR] 저장소 연결 실패 - 인터넷 연결 또는 GitHub 로그인을 확인하세요.
  pause & exit /b 1
)
git reset --hard origin/main
git branch -M main
git branch --set-upstream-to=origin/main main >nul 2>&1
echo.
echo [OK] 연결 완료! 다음부터는 이 버튼이 바로 최신본을 받습니다.
goto done

REM ── 이후: 최신 커밋 받기 ──
:pull
echo 최신 코드를 받는 중 (git pull)...
git pull origin main
if errorlevel 1 (
  echo.
  echo [주의] git pull 실패 - 내 로컬 변경과 충돌했을 수 있습니다.
  choice /c YN /m "내 로컬 변경을 버리고 강제로 최신본에 맞출까요"
  if errorlevel 2 goto done
  git fetch origin main && git reset --hard origin/main
)

:done
echo.
echo ==================================================
echo    업데이트 완료!
echo ==================================================
echo.
choice /c YN /m "지금 매핑 로스터 렌더를 실행할까요"
if errorlevel 2 goto end
call "%~dp0render-roster.bat"
goto :eof

:end
echo render-roster.bat 을 더블클릭하면 언제든 렌더할 수 있습니다.
pause
