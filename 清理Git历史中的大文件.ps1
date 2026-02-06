# 清理 Git 历史中的大文件
# 编码：UTF-8

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "清理 Git 历史中的大文件" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  警告：此操作会重写 Git 历史记录！" -ForegroundColor Yellow
Write-Host "⚠️  建议先备份仓库或创建新分支！" -ForegroundColor Yellow
Write-Host ""

$confirm = Read-Host "确定要继续吗？(yes/no)"
if ($confirm -ne "yes") {
    Write-Host "操作已取消" -ForegroundColor Yellow
    exit
}

# 切换到项目目录
$projectPath = "D:\学习\中山大学智能工程学院本科生课程作业"
Set-Location $projectPath

Write-Host ""
Write-Host "[步骤 1/5] 移除计算机视觉大目录的历史记录..." -ForegroundColor Yellow
Write-Host "（这可能需要很长时间，请耐心等待）" -ForegroundColor Gray

# PowerShell 版本：使用反引号作为续行符，或者写在一行
git filter-branch --force --index-filter "git rm -rf --cached --ignore-unmatch '计算机视觉/Plant-Pathology-sysu-2023-main'" --prune-empty --tag-name-filter cat -- --all

if ($LASTEXITCODE -ne 0) {
    Write-Host "[错误] filter-branch 执行失败" -ForegroundColor Red
    exit 1
}

Write-Host "✓ 历史记录已重写" -ForegroundColor Green

Write-Host ""
Write-Host "[步骤 2/5] 清理引用..." -ForegroundColor Yellow
git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin
Write-Host "✓ 引用已清理" -ForegroundColor Green

Write-Host ""
Write-Host "[步骤 3/5] 清理 reflog..." -ForegroundColor Yellow
git reflog expire --expire=now --all
Write-Host "✓ reflog 已清理" -ForegroundColor Green

Write-Host ""
Write-Host "[步骤 4/5] 强制垃圾回收..." -ForegroundColor Yellow
git gc --prune=now --aggressive
Write-Host "✓ 垃圾回收完成" -ForegroundColor Green

Write-Host ""
Write-Host "[步骤 5/5] 检查仓库大小..." -ForegroundColor Yellow
$repoSize = (git count-objects -vH | Select-String "size-pack").ToString()
Write-Host "仓库大小: $repoSize" -ForegroundColor Cyan

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ 清理完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "下一步：强制推送到远程仓库" -ForegroundColor Yellow
Write-Host "命令：git push origin --force --all" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  注意：强制推送会覆盖远程历史记录！" -ForegroundColor Red
Write-Host ""

$pushConfirm = Read-Host "现在推送到远程仓库吗？(yes/no)"
if ($pushConfirm -eq "yes") {
    Write-Host ""
    Write-Host "正在推送..." -ForegroundColor Yellow
    git push origin --force --all
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ 推送成功！" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "❌ 推送失败" -ForegroundColor Red
    }
} else {
    Write-Host "已跳过推送，你可以稍后手动执行：git push origin --force --all" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "按 Enter 键退出"
