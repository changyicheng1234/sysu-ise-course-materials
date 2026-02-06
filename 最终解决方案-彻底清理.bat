@echo off
chcp 65001 >nul
echo ========================================
echo 最终解决方案：彻底清理并推送
echo ========================================
echo.
echo 这个脚本会：
echo 1. 检查并确保 .gitignore 正确配置
echo 2. 创建全新的分支（不包含历史）
echo 3. 只添加小文件，排除所有大文件
echo 4. 推送到 GitHub
echo.

cd /d "D:\学习\中山大学智能工程学院本科生课程作业"

echo [步骤 1/9] 检查当前状态...
git status --short
echo.

echo [步骤 2/9] 检查 .gitignore 配置...
if exist .gitignore (
    echo ✓ .gitignore 文件存在
    findstr /C:"Plant-Pathology-sysu-2023-main" .gitignore >nul
    if %errorlevel% equ 0 (
        echo ✓ 计算机视觉大目录已在 .gitignore 中
    ) else (
        echo ✗ 警告：计算机视觉大目录可能未在 .gitignore 中
    )
) else (
    echo ✗ .gitignore 文件不存在！
    pause
    exit /b 1
)
echo.

echo [步骤 3/9] 创建新的孤立分支...
git checkout --orphan clean-main 2>nul
if %errorlevel% neq 0 (
    echo 删除已存在的 clean-main 分支...
    git branch -D clean-main 2>nul
    git checkout --orphan clean-main
)
echo ✓ 新分支已创建
echo.

echo [步骤 4/9] 清空暂存区...
git rm -rf --cached . 2>nul
echo ✓ 暂存区已清空
echo.

echo [步骤 5/9] 添加文件（.gitignore 会自动排除大文件）...
git add .
echo ✓ 文件已添加
echo.

echo [步骤 6/9] 检查将要提交的文件...
git ls-files > temp_files.txt
echo 已跟踪的文件数量：
find /c /v "" < temp_files.txt
del temp_files.txt
echo.

echo [步骤 7/9] 创建提交...
git commit -m "清理后的版本：移除所有大文件，只保留代码和文档"
if %errorlevel% neq 0 (
    echo [警告] 提交失败，可能没有更改
    git status
)
echo.

echo [步骤 8/9] 替换 main 分支...
git branch -D main 2>nul
git branch -m main
echo ✓ main 分支已替换
echo.

echo [步骤 9/9] 配置 Git 并推送...
git config http.postBuffer 524288000
git config http.maxRequestBuffer 100M
git config http.version HTTP/1.1
echo ✓ Git 配置已更新
echo.

echo ========================================
echo 准备推送到远程仓库
echo ========================================
echo.
echo ⚠️  注意：这将强制覆盖远程 main 分支
echo.

set /p confirm="确定要推送吗？(yes/no): "
if /i "%confirm%" neq "yes" (
    echo.
    echo 已取消推送
    echo 你可以稍后手动执行：git push -f origin main
    pause
    exit /b 0
)

echo.
echo 正在推送（这可能需要一些时间）...
echo.

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
    echo 如果仍然失败，可能的原因：
    echo 1. 文件仍然太大（GitHub 限制）
    echo 2. 网络问题
    echo 3. GitHub 服务器问题
    echo.
    echo 建议：
    echo - 检查 .gitignore 是否正确
    echo - 确认工作目录中没有大文件
    echo - 尝试使用 Git LFS 或分批推送
)

echo.
pause
