@echo off
chcp 65001 >nul
echo ========================================
echo 上传文件到 GitHub 仓库
echo ========================================
echo.

:: 检查是否已初始化 Git 仓库
if not exist .git (
    echo [步骤 1/6] 初始化 Git 仓库...
    git init
    if errorlevel 1 (
        echo [错误] Git 初始化失败，请确保已安装 Git
        pause
        exit /b 1
    )
) else (
    echo [信息] Git 仓库已存在
)

echo.
echo [步骤 2/6] 检查并设置远程仓库...
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo 添加远程仓库地址...
    git remote add origin https://github.com/changyicheng1234/-.git
    if errorlevel 1 (
        echo [错误] 添加远程仓库失败
        pause
        exit /b 1
    )
) else (
    echo 更新远程仓库地址...
    git remote set-url origin https://github.com/changyicheng1234/-.git
)

echo.
echo [步骤 3/6] 检查 Git 用户配置...
git config user.name >nul 2>&1
if errorlevel 1 (
    echo [警告] 未配置 Git 用户名，使用默认值
    git config user.name "changyicheng1234"
)

git config user.email >nul 2>&1
if errorlevel 1 (
    echo [警告] 未配置 Git 邮箱，使用默认值
    git config user.email "changyicheng1234@users.noreply.github.com"
)

echo.
echo [步骤 4/6] 添加所有文件...
git add .
if errorlevel 1 (
    echo [错误] 添加文件失败
    pause
    exit /b 1
)

echo.
echo [步骤 5/6] 创建提交...
git commit -m "更新：上传课程资料到 GitHub"
if errorlevel 1 (
    echo [警告] 提交失败，可能没有更改的文件
)

echo.
echo [步骤 6/6] 设置主分支并推送到 GitHub...
git branch -M main
git push -u origin main
if errorlevel 1 (
    echo [错误] 推送失败
    echo.
    echo 可能的原因：
    echo 1. 需要配置 GitHub 认证（使用 Personal Access Token）
    echo 2. 远程仓库不存在或没有权限
    echo 3. 网络连接问题
    echo.
    echo 如果使用 HTTPS，可能需要输入用户名和 Personal Access Token
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ 文件已成功上传到 GitHub！
echo ========================================
echo.
echo 仓库地址：https://github.com/changyicheng1234/-
echo.
pause
