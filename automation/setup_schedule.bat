@echo off
chcp 65001 >nul
set HERE=%~dp0
REM 1) 매일 밤 23:00 자동 렌더
schtasks /create /tn "SpriteNightlyRender" /tr "\"%HERE%..\render.bat\"" /sc DAILY /st 23:00 /f
REM 2) 10분마다 명령 폴링
schtasks /create /tn "SpritePoll" /tr "\"%HERE%poll.bat\"" /sc MINUTE /mo 10 /f
echo.
echo 등록 완료. 확인: schtasks /query /tn SpriteNightlyRender ^& schtasks /query /tn SpritePoll
echo 해제: schtasks /delete /tn SpriteNightlyRender /f  ^&  schtasks /delete /tn SpritePoll /f
pause
