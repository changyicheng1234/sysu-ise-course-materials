@echo off
chcp 65001 >nul
echo ========================================
echo 快速清理 Git 历史并推送
echo ========================================
echo.
echo 正在运行 Python 清理脚本...
echo.

python 清理Git历史中的大文件.py

pause
