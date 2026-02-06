@echo off
chcp 65001 >nul
echo ========================================
echo 分批上传所有文件到GitHub
echo ========================================
echo.
echo 这个脚本会将7GB内容分成3批上传
echo 包括所有PDF文件
echo.
pause

python "分批上传所有文件.py"

pause
