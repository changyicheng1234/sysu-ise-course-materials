@echo off
chcp 65001 >nul
echo ============================================================
echo 首次完整推送：上传所有文件到GitHub
echo ============================================================
echo.

cd /d "%~dp0"

echo [步骤 1/5] 检查远程仓库配置...
git remote -v
echo.

echo [步骤 2/5] 检查Git状态...
git status
echo.

echo [步骤 3/5] 检查大文件（大于50MB）...
powershell -Command "Get-ChildItem -Recurse -File | Where-Object {$_.Length -gt 50MB} | Select-Object FullName, @{Name='Size(MB)';Expression={[math]::Round($_.Length/1MB,2)}} | Format-Table -AutoSize"
echo.

echo [步骤 4/5] 添加所有文件（.gitignore会自动忽略大文件）...
git add .
echo.

echo [步骤 5/5] 检查将要提交的文件...
git status --short
echo.

set /p confirm="是否创建提交并推送？(Y/N): "
if /i "%confirm%"=="Y" (
    echo.
    echo 创建提交...
    git commit -m "首次完整推送：上传所有课程作业文件"
    echo.
    echo 配置推送参数...
    git config http.postBuffer 524288000
    git config http.maxRequestBuffer 100M
    echo.
    echo 推送到远程仓库...
    echo （这可能需要一些时间，请耐心等待）
    git push -u origin main
    echo.
    if %errorlevel% equ 0 (
        echo ✅ 推送成功！
        echo.
        echo 仓库地址：https://github.com/changyicheng1234/sysu-ise-course-materials
    ) else (
        echo ❌ 推送失败
        echo.
        echo 可能的原因：
        echo 1. 仍有大文件（大于100MB）
        echo 2. 网络连接问题
        echo 3. 认证问题
        echo.
        echo 建议运行：python 彻底清理并推送.py
    )
) else (
    echo.
    echo 已取消，你可以稍后手动执行：
    echo   git commit -m "首次完整推送"
    echo   git push -u origin main
)

echo.
pause
