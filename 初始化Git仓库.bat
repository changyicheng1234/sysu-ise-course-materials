@echo off
chcp 65001 >nul
echo ========================================
echo GitHub 仓库初始化脚本
echo ========================================
echo.

:: 检查是否已初始化 Git 仓库
if exist .git (
    echo [信息] Git 仓库已存在
    git status
    echo.
    echo 如果已配置远程仓库，可以直接推送：
    echo   git push -u origin main
    echo.
    pause
    exit /b
)

echo [步骤 1/5] 初始化 Git 仓库...
git init
if errorlevel 1 (
    echo [错误] Git 初始化失败，请确保已安装 Git
    pause
    exit /b 1
)

echo.
echo [步骤 2/5] 检查 Git 用户配置...
git config user.name >nul 2>&1
if errorlevel 1 (
    echo [警告] 未配置 Git 用户名
    set /p GIT_USER="请输入你的 GitHub 用户名: "
    git config user.name "%GIT_USER%"
)

git config user.email >nul 2>&1
if errorlevel 1 (
    echo [警告] 未配置 Git 邮箱
    set /p GIT_EMAIL="请输入你的 GitHub 邮箱: "
    git config user.email "%GIT_EMAIL%"
)

echo.
echo [步骤 3/5] 添加所有文件...
git add .
if errorlevel 1 (
    echo [错误] 添加文件失败
    pause
    exit /b 1
)

echo.
echo [步骤 4/5] 创建初始提交...
git commit -m "初始提交：中山大学智能工程学院课程资料共享项目"
if errorlevel 1 (
    echo [错误] 提交失败
    pause
    exit /b 1
)

echo.
echo [步骤 5/5] 设置主分支...
git branch -M main

echo.
echo ========================================
echo ✅ Git 仓库初始化完成！
echo ========================================
echo.
echo 接下来需要：
echo 1. 在 GitHub 上创建新仓库（参考 GitHub仓库设置指南.md）
echo 2. 添加远程仓库地址：
echo    git remote add origin https://github.com/你的用户名/仓库名.git
echo 3. 推送代码：
echo    git push -u origin main
echo 4. 在 GitHub 仓库设置中启用 Actions 并配置权限
echo.
echo 详细说明请查看：GitHub仓库设置指南.md
echo.
pause
