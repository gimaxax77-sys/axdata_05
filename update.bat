@echo off
chcp 65001 >nul
cd /d "%~dp0"
title AXdata Render - Update

set "REPO_URL=https://github.com/gimaxax77-sys/axdata_05.git"

echo ==================================================
echo    AXdata Render Tool  -  Get latest commits
echo ==================================================
echo.

where git >nul 2>&1
if errorlevel 1 (
  echo [ERROR] git is not installed.
  echo   Install: https://git-scm.com/download/win  then run again.
  pause & exit /b 1
)

if exist "%~dp0.git" goto pull

echo [First time] Linking this folder to the repository...
echo   (your own files like character_map.csv are kept)
echo.
git init >nul
git remote remove origin >nul 2>&1
git remote add origin "%REPO_URL%"
git fetch origin main
if errorlevel 1 (
  echo [ERROR] Link failed - check internet or GitHub login.
  pause & exit /b 1
)
git reset --hard origin/main
git branch -M main
git branch --set-upstream-to=origin/main main >nul 2>&1
echo.
echo [OK] Linked. From now this button pulls the latest.
goto done

:pull
echo Pulling latest code (git pull)...
git pull origin main
if errorlevel 1 (
  echo.
  echo [WARN] git pull failed - local changes may conflict.
  choice /c YN /m "Discard my local changes and force latest"
  if errorlevel 2 goto done
  git fetch origin main && git reset --hard origin/main
)

:done
echo.
echo ==================================================
echo    Update complete!
echo ==================================================
echo.
choice /c YN /m "Run the roster render now"
if errorlevel 2 goto end
call "%~dp0render-roster.bat"
goto :eof

:end
echo Double-click render-roster.bat anytime to render.
pause
