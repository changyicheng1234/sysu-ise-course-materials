@echo off
chcp 65001 >nul
echo ========================================
echo 创建新分支并推送（最简单的方法）
echo ========================================
echo.
echo ⚠️  警告：这会创建一个全新的分支，丢失 Git 历史记录
echo    但对于课程作业仓库来说通常不是问题
echo.

cd /d "D:\学习\中山大学智能工程学院本科生课程作业"

echo [步骤 1/6] 检查当前状态...
git status
echo.

echo [步骤 2/6] 创建新的孤立分支...
git checkout --orphan new-main
if %errorlevel% neq 0 (
    echo [错误] 创建分支失败
    pause
    exit /b 1
)
echo ✓ 新分支已创建
echo.

echo [步骤 3/6] 添加所有当前文件...
git add .
echo ✓ 文件已添加
echo.

echo [步骤 4/6] 创建初始提交...
git commit -m "清理后的新版本：移除大文件"
if %errorlevel% neq 0 (
    echo [警告] 提交失败，可能没有更改
    git status
)
echo.

echo [步骤 5/6] 删除旧的 main 分支...
git branch -D main
echo ✓ 旧分支已删除
echo.

echo [步骤 6/6] 重命名当前分支为 main...
git branch -m main
echo ✓ 分支已重命名
echo.

echo ========================================
echo 准备推送到远程仓库
echo ========================================
echo.
echo ⚠️  注意：这将强制覆盖远程 main 分支
echo.

set /p confirm="确定要推送吗？(yes/no): "
if /i "%confirm%" neq "yes" (
    echo 已取消推送
    echo 你可以稍后手动执行：git push -f origin main
    pause
    exit /b 0
)

echo.
echo 正在推送...
git push -f origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✅ 推送成功！
    echo ========================================
    echo.
    echo 仓库地址：https://github.com/changyicheng1234/-
) else (
    echo.
    echo ========================================
    echo ❌ 推送失败
    echo ========================================
    echo.
    echo 可能的原因：
    echo 1. 网络连接问题
    echo 2. GitHub 服务器问题
    echo 3. 需要认证（Personal Access Token）
)

echo.
pause
