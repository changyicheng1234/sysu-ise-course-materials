# -*- coding: utf-8 -*-
"""
彻底清理并推送：创建新分支，确保没有大文件
"""
import subprocess
import os
import sys

def run_command(cmd, description, check=True, show_output=True):
    """执行命令并显示结果"""
    if show_output:
        print(f"\n[步骤] {description}...")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if show_output:
            if result.stdout:
                print(result.stdout)
            if result.stderr and result.returncode != 0:
                print(f"错误: {result.stderr}", file=sys.stderr)
        
        if check and result.returncode != 0:
            if show_output:
                print(f"❌ 命令执行失败，退出码: {result.returncode}")
            return False
        
        return True
    except Exception as e:
        if show_output:
            print(f"❌ 执行命令时出错: {e}")
        return False

def check_large_files():
    """检查是否有大文件"""
    print("\n检查工作目录中的大文件...")
    
    # 检查大于 50MB 的文件
    result = subprocess.run(
        'powershell -Command "Get-ChildItem -Recurse -File | Where-Object {$_.Length -gt 50MB} | Select-Object FullName, @{Name=\'Size(MB)\';Expression={[math]::Round($_.Length/1MB,2)}} | Format-Table -AutoSize"',
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    if result.stdout:
        print("发现以下大文件（>50MB）：")
        print(result.stdout)
        return True
    else:
        print("✓ 未发现大于 50MB 的文件")
        return False

def main():
    print("=" * 70)
    print("彻底清理并推送：创建新分支方案")
    print("=" * 70)
    print("\n⚠️  警告：这会创建一个全新的分支，丢失 Git 历史记录")
    print("    但对于课程作业仓库来说通常不是问题")
    
    confirm = input("\n确定要继续吗？(yes/no): ")
    if confirm.lower() != "yes":
        print("操作已取消")
        return
    
    # 切换到项目目录
    project_path = r"D:\学习\中山大学智能工程学院本科生课程作业"
    os.chdir(project_path)
    print(f"\n工作目录: {os.getcwd()}")
    
    # 检查大文件
    has_large_files = check_large_files()
    if has_large_files:
        print("\n⚠️  警告：发现大文件！")
        print("这些文件应该被 .gitignore 忽略，但如果它们已经被跟踪，")
        print("需要先从 Git 索引中移除。")
        input("\n按 Enter 继续...")
    
    # 步骤 1: 检查当前分支
    print("\n" + "=" * 70)
    print("[步骤 1/8] 检查当前状态...")
    print("=" * 70)
    run_command("git status", "检查 Git 状态", check=False)
    
    # 步骤 2: 确保 .gitignore 正确
    print("\n" + "=" * 70)
    print("[步骤 2/8] 检查 .gitignore...")
    print("=" * 70)
    if os.path.exists(".gitignore"):
        print("✓ .gitignore 文件存在")
        # 检查关键规则
        with open(".gitignore", "r", encoding="utf-8") as f:
            content = f.read()
            if "Plant-Pathology-sysu-2023-main" in content:
                print("✓ 计算机视觉大目录已在 .gitignore 中")
            if "*.jpg" in content or "*.png" in content:
                print("✓ 图片文件已在 .gitignore 中")
    else:
        print("❌ .gitignore 文件不存在！")
        return
    
    # 步骤 3: 创建新的孤立分支
    print("\n" + "=" * 70)
    print("[步骤 3/8] 创建新的孤立分支...")
    print("=" * 70)
    if not run_command("git checkout --orphan new-main", "创建孤立分支"):
        print("尝试删除已存在的 new-main 分支...")
        run_command("git branch -D new-main", "删除旧分支", check=False)
        run_command("git checkout --orphan new-main", "创建孤立分支")
    
    # 步骤 4: 移除所有已跟踪的文件
    print("\n" + "=" * 70)
    print("[步骤 4/8] 清空暂存区...")
    print("=" * 70)
    run_command("git rm -rf --cached .", "移除所有已跟踪的文件", check=False)
    
    # 步骤 5: 添加当前文件（.gitignore 会自动生效）
    print("\n" + "=" * 70)
    print("[步骤 5/8] 添加当前文件（.gitignore 会自动忽略大文件）...")
    print("=" * 70)
    run_command("git add .", "添加文件", check=False)
    
    # 步骤 6: 检查将要提交的文件大小
    print("\n" + "=" * 70)
    print("[步骤 6/8] 检查将要提交的文件...")
    print("=" * 70)
    result = subprocess.run(
        "git ls-files | git cat-file --batch-check='%(objectsize) %(rest)' | awk '{sum+=$1} END {print \"总大小: \" sum/1024/1024 \" MB\"}'",
        shell=True,
        capture_output=True,
        text=True
    )
    
    # 使用 PowerShell 检查
    result = subprocess.run(
        'powershell -Command "$files = git ls-files; $total = 0; foreach($f in $files) { if(Test-Path $f) { $total += (Get-Item $f).Length } }; Write-Host \"总大小: $([math]::Round($total/1MB, 2)) MB\""',
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    if result.stdout:
        print(result.stdout.strip())
    
    # 步骤 7: 创建提交
    print("\n" + "=" * 70)
    print("[步骤 7/8] 创建初始提交...")
    print("=" * 70)
    run_command(
        'git commit -m "清理后的新版本：移除所有大文件"',
        "创建提交",
        check=False
    )
    
    # 步骤 8: 删除旧的 main 分支并重命名
    print("\n" + "=" * 70)
    print("[步骤 8/8] 替换 main 分支...")
    print("=" * 70)
    
    # 切换到 main 分支（如果存在）
    run_command("git checkout main", "切换到 main 分支", check=False)
    
    # 删除旧的 main 分支
    run_command("git branch -D main", "删除旧 main 分支", check=False)
    
    # 切换回 new-main
    run_command("git checkout new-main", "切换回 new-main", check=False)
    
    # 重命名为 main
    run_command("git branch -m main", "重命名为 main", check=False)
    
    print("\n" + "=" * 70)
    print("✅ 本地清理完成！")
    print("=" * 70)
    
    # 询问是否推送
    print("\n下一步：强制推送到远程仓库")
    print("⚠️  注意：强制推送会覆盖远程 main 分支的所有历史！")
    
    push_confirm = input("\n现在推送到远程仓库吗？(yes/no): ")
    if push_confirm.lower() == "yes":
        print("\n正在推送...")
        print("（如果文件仍然很大，可能需要一些时间）")
        
        # 配置 Git 使用更大的缓冲区
        run_command("git config http.postBuffer 524288000", "配置缓冲区", check=False, show_output=False)
        run_command("git config http.maxRequestBuffer 100M", "配置最大请求缓冲区", check=False, show_output=False)
        
        success = run_command("git push -f origin main", "强制推送", check=False)
        
        if success:
            print("\n" + "=" * 70)
            print("✅ 推送成功！")
            print("=" * 70)
            print("\n仓库地址：https://github.com/changyicheng1234/-")
        else:
            print("\n" + "=" * 70)
            print("❌ 推送失败")
            print("=" * 70)
            print("\n可能的原因：")
            print("1. 文件仍然太大（GitHub 限制单次推送约 2GB）")
            print("2. 网络连接问题")
            print("3. GitHub 服务器问题")
            print("4. 需要认证（Personal Access Token）")
            print("\n建议：")
            print("- 检查 .gitignore 是否正确配置")
            print("- 确认工作目录中没有大文件")
            print("- 尝试分批推送或使用 Git LFS")
    else:
        print("\n已跳过推送，你可以稍后手动执行：")
        print("git push -f origin main")
    
    print("\n按 Enter 键退出...")
    input()

if __name__ == "__main__":
    main()
