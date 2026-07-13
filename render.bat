@echo off
REM Blender 경로를 본인 설치에 맞게 수정하세요
set BLENDER="C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"
cd /d %~dp0
%BLENDER% --background --python scripts\render_sprites.py
pause
