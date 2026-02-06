@echo off
chcp 65001 >nul
echo ============================================================
echo 快速检查并推送删除的文件
echo ============================================================
echo.

cd /d "%~dp0"

echo [1/4] 检查Git状态...
git status
echo.

echo [2/4] 检查是否有PDF文件被Git跟踪...
git ls-files | findstr /i "\.pdf$"
if %errorlevel% equ 0 (
    echo 发现PDF文件被跟踪，需要从Git中移除
) else (
    echo ✓ 没有PDF文件被Git跟踪
)
echo.

echo [3/4] 添加所有更改（包括删除的文件）...
git add -A
echo.

echo [4/4] 检查是否有需要提交的更改...
git status --short
echo.

set /p confirm="是否创建提交并推送？(Y/N): "
if /i "%confirm%"=="Y" (
    echo.
    echo 创建提交...
    git commit -m "移除大文件PDF并更新.gitignore"
    echo.
    echo 推送到远程...
    git push origin main
    echo.
    echo ✅ 完成！
) else (
    echo.
    echo 已取消，你可以稍后手动执行：
    echo   git commit -m "移除大文件PDF"
    echo   git push origin main
)

echo.
pause
