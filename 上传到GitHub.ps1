# GitHub 上传脚本
# 编码：UTF-8

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "上传文件到 GitHub 仓库" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 切换到项目目录
$projectPath = "D:\学习\中山大学智能工程学院本科生课程作业"
Set-Location $projectPath

# 步骤 1: 初始化 Git 仓库
if (-not (Test-Path .git)) {
    Write-Host "[步骤 1/6] 初始化 Git 仓库..." -ForegroundColor Yellow
    git init
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[错误] Git 初始化失败，请确保已安装 Git" -ForegroundColor Red
        Read-Host "按 Enter 键退出"
        exit 1
    }
} else {
    Write-Host "[信息] Git 仓库已存在" -ForegroundColor Green
}

# 步骤 2: 设置远程仓库
Write-Host ""
Write-Host "[步骤 2/6] 检查并设置远程仓库..." -ForegroundColor Yellow
$remoteUrl = git remote get-url origin 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "添加远程仓库地址..." -ForegroundColor Yellow
    git remote add origin https://github.com/changyicheng1234/-.git
} else {
    Write-Host "更新远程仓库地址..." -ForegroundColor Yellow
    git remote set-url origin https://github.com/changyicheng1234/-.git
}

# 步骤 3: 检查 Git 用户配置
Write-Host ""
Write-Host "[步骤 3/6] 检查 Git 用户配置..." -ForegroundColor Yellow
$userName = git config user.name 2>$null
if (-not $userName) {
    Write-Host "设置 Git 用户名..." -ForegroundColor Yellow
    git config user.name "changyicheng1234"
}

$userEmail = git config user.email 2>$null
if (-not $userEmail) {
    Write-Host "设置 Git 邮箱..." -ForegroundColor Yellow
    git config user.email "changyicheng1234@users.noreply.github.com"
}

# 步骤 4: 添加所有文件
Write-Host ""
Write-Host "[步骤 4/6] 添加所有文件..." -ForegroundColor Yellow
git add .
if ($LASTEXITCODE -ne 0) {
    Write-Host "[错误] 添加文件失败" -ForegroundColor Red
    Read-Host "按 Enter 键退出"
    exit 1
}

# 步骤 5: 创建提交
Write-Host ""
Write-Host "[步骤 5/6] 创建提交..." -ForegroundColor Yellow
git commit -m "更新：上传课程资料到 GitHub"
if ($LASTEXITCODE -ne 0) {
    Write-Host "[警告] 提交失败，可能没有更改的文件" -ForegroundColor Yellow
}

# 步骤 6: 推送
Write-Host ""
Write-Host "[步骤 6/6] 设置主分支并推送到 GitHub..." -ForegroundColor Yellow
git branch -M main
git push -u origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[错误] 推送失败" -ForegroundColor Red
    Write-Host ""
    Write-Host "可能的原因：" -ForegroundColor Yellow
    Write-Host "1. 需要配置 GitHub 认证（使用 Personal Access Token）" -ForegroundColor White
    Write-Host "2. 远程仓库不存在或没有权限" -ForegroundColor White
    Write-Host "3. 网络连接问题" -ForegroundColor White
    Write-Host ""
    Write-Host "如果使用 HTTPS，可能需要输入用户名和 Personal Access Token" -ForegroundColor Yellow
    Write-Host "详细说明请查看：GitHub上传指南.md" -ForegroundColor Yellow
    Read-Host "按 Enter 键退出"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ 文件已成功上传到 GitHub！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "仓库地址：https://github.com/changyicheng1234/-" -ForegroundColor Cyan
Write-Host ""
Read-Host "按 Enter 键退出"
