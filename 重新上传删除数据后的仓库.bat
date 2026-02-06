@echo off
chcp 65001 >nul
echo ========================================
echo 重新上传删除数据后的仓库到 GitHub
echo ========================================
echo.

cd /d "D:\学习\中山大学智能工程学院本科生课程作业"

echo [步骤 1/7] 检查 Git 状态...
git status
echo.

echo [步骤 2/7] 检查 .gitignore 配置...
if exist .gitignore (
    echo ✓ .gitignore 文件存在
) else (
    echo ✗ .gitignore 文件不存在
    pause
    exit /b 1
)

echo.
echo [步骤 3/7] 从 Git 索引中移除已删除的文件...
git add -u
echo ✓ 已更新索引

echo.
echo [步骤 4/7] 移除被 .gitignore 忽略但仍在跟踪的文件...
echo （这可能需要一些时间）

git rm -r --cached "计算机视觉/Plant-Pathology-sysu-2023-main" -f 2>nul
if %errorlevel% equ 0 (
    echo ✓ 已移除 计算机视觉/Plant-Pathology-sysu-2023-main
)

git rm -r --cached "自然语言处理/常毅成小组_期中大作业/text-to-lora/text-to-lora" -f 2>nul
if %errorlevel% equ 0 (
    echo ✓ 已移除 自然语言处理/常毅成小组_期中大作业/text-to-lora/text-to-lora
)

echo ✓ 已移除所有被忽略的文件

echo.
echo [步骤 5/7] 添加当前文件...
git add .
echo ✓ 文件已添加

echo.
echo [步骤 6/7] 创建提交...
git commit -m "清理：移除计算机视觉大文件和被忽略的文件"
if %errorlevel% neq 0 (
    echo [警告] 提交失败，可能没有更改的文件
    echo 检查是否有未提交的更改...
    git status
)

echo.
echo [步骤 7/7] 推送到 GitHub...
echo （配置 Git 使用更大的缓冲区以处理大文件）

git config http.postBuffer 524288000
git config http.maxRequestBuffer 100M

git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo [错误] 推送失败
    echo.
    echo 可能的原因：
    echo 1. 仓库中仍有大文件在历史记录中
    echo 2. 网络连接问题
    echo 3. GitHub 服务器问题
    echo.
    echo 建议：
    echo 如果问题持续，可能需要清理 Git 历史记录中的大文件
    echo 可以使用 git filter-branch 或 BFG Repo-Cleaner 工具
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
