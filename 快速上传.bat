@echo off
chcp 65001 >nul
echo ========================================
echo 🚀 快速上传到 GitHub
echo ========================================
echo.

:: 切换到项目目录
cd /d "%~dp0"

:: 1. 初始化（如果需要）
if not exist .git (
    echo [1/6] 初始化 Git 仓库...
    git init
)

:: 2. 设置远程仓库
echo [2/6] 设置远程仓库...
git remote remove origin 2>nul
git remote add origin https://github.com/changyicheng1234/-.git

:: 3. 配置用户
echo [3/6] 配置 Git 用户...
git config user.name "changyicheng1234" 2>nul
git config user.email "changyicheng1234@users.noreply.github.com" 2>nul

:: 4. 添加文件（排除大文件）
echo [4/6] 添加文件（已排除大文件）...
git add .

:: 5. 提交
echo [5/6] 提交更改...
git commit -m "上传课程资料" 2>nul || echo 没有新文件需要提交

:: 6. 推送
echo [6/6] 推送到 GitHub...
git branch -M main
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ✅ 上传成功！
    echo 仓库地址：https://github.com/changyicheng1234/-
) else (
    echo.
    echo ⚠️ 推送可能需要认证
    echo 请按照提示输入用户名和 Personal Access Token
)

echo.
pause
