@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 正在更新所有课程的README文件...
echo.
python 更新README资料.py
echo.
pause
