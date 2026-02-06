# 重新上传删除数据后的仓库
# 编码：UTF-8

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "重新上传删除数据后的仓库到 GitHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 切换到项目目录
$projectPath = "D:\学习\中山大学智能工程学院本科生课程作业"
Set-Location $projectPath

# 步骤 1: 检查 Git 状态
Write-Host "[步骤 1/7] 检查 Git 状态..." -ForegroundColor Yellow
git status
Write-Host ""

# 步骤 2: 确保 .gitignore 正确配置
Write-Host "[步骤 2/7] 检查 .gitignore 配置..." -ForegroundColor Yellow
if (Test-Path .gitignore) {
    Write-Host "✓ .gitignore 文件存在" -ForegroundColor Green
} else {
    Write-Host "✗ .gitignore 文件不存在" -ForegroundColor Red
    exit 1
}

# 步骤 3: 从 Git 索引中移除已删除的文件（如果它们被跟踪）
Write-Host ""
Write-Host "[步骤 3/7] 从 Git 索引中移除已删除的文件..." -ForegroundColor Yellow
git add -u
Write-Host "✓ 已更新索引" -ForegroundColor Green

# 步骤 4: 移除被 .gitignore 忽略但仍在跟踪的文件
Write-Host ""
Write-Host "[步骤 4/7] 移除被 .gitignore 忽略但仍在跟踪的文件..." -ForegroundColor Yellow
Write-Host "（这可能需要一些时间）" -ForegroundColor Gray

# 移除计算机视觉的大目录（如果被跟踪）
git rm -r --cached "计算机视觉/Plant-Pathology-sysu-2023-main" -f 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ 已移除 计算机视觉/Plant-Pathology-sysu-2023-main" -ForegroundColor Green
}

# 移除自然语言处理的大目录（如果被跟踪）
git rm -r --cached "自然语言处理/常毅成小组_期中大作业/text-to-lora/text-to-lora" -f 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ 已移除 自然语言处理/常毅成小组_期中大作业/text-to-lora/text-to-lora" -ForegroundColor Green
}

# 移除所有被忽略的大文件类型
Write-Host "移除被忽略的图片文件..." -ForegroundColor Gray
git ls-files | Where-Object { $_ -match '\.(jpg|jpeg|png|gif|bmp|tiff|ico)$' } | ForEach-Object {
    git rm --cached $_ -f 2>$null
}

Write-Host "移除被忽略的压缩包..." -ForegroundColor Gray
git ls-files | Where-Object { $_ -match '\.(zip|rar|7z|tar\.gz|tar)$' } | ForEach-Object {
    git rm --cached $_ -f 2>$null
}

Write-Host "移除被忽略的模型文件..." -ForegroundColor Gray
git ls-files | Where-Object { $_ -match '\.(pth|pt|ckpt|h5|hdf5|pkl|pickle|model|weights)$' } | ForEach-Object {
    git rm --cached $_ -f 2>$null
}

Write-Host "移除被忽略的数据文件..." -ForegroundColor Gray
git ls-files | Where-Object { $_ -match '\.(csv|xlsx|xls|db|sqlite|sqlite3)$' } | ForEach-Object {
    git rm --cached $_ -f 2>$null
}

Write-Host "✓ 已移除所有被忽略的文件" -ForegroundColor Green

# 步骤 5: 添加当前文件（只添加未被忽略的文件）
Write-Host ""
Write-Host "[步骤 5/7] 添加当前文件..." -ForegroundColor Yellow
git add .
Write-Host "✓ 文件已添加" -ForegroundColor Green

# 步骤 6: 创建提交
Write-Host ""
Write-Host "[步骤 6/7] 创建提交..." -ForegroundColor Yellow
$commitMessage = "清理：移除计算机视觉大文件和被忽略的文件"
git commit -m $commitMessage
if ($LASTEXITCODE -ne 0) {
    Write-Host "[警告] 提交失败，可能没有更改的文件" -ForegroundColor Yellow
    Write-Host "检查是否有未提交的更改..." -ForegroundColor Gray
    git status
}

# 步骤 7: 推送（使用较小的包大小）
Write-Host ""
Write-Host "[步骤 7/7] 推送到 GitHub..." -ForegroundColor Yellow
Write-Host "（如果之前推送失败，这次会尝试分批推送）" -ForegroundColor Gray

# 配置 Git 使用更大的缓冲区
git config http.postBuffer 524288000
git config http.maxRequestBuffer 100M

# 尝试推送
git push -u origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[错误] 推送失败" -ForegroundColor Red
    Write-Host ""
    Write-Host "可能的原因：" -ForegroundColor Yellow
    Write-Host "1. 仓库中仍有大文件在历史记录中" -ForegroundColor White
    Write-Host "2. 网络连接问题" -ForegroundColor White
    Write-Host "3. GitHub 服务器问题" -ForegroundColor White
    Write-Host ""
    Write-Host "建议：" -ForegroundColor Yellow
    Write-Host "如果问题持续，可能需要清理 Git 历史记录中的大文件" -ForegroundColor White
    Write-Host "可以使用 git filter-branch 或 BFG Repo-Cleaner 工具" -ForegroundColor White
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
