# -*- coding: utf-8 -*-
"""
首次完整推送：确保所有文件正确上传到GitHub
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
    
    if result.stdout.strip():
        print("⚠️  发现以下大文件（>50MB）：")
        print(result.stdout)
        print("\n这些文件应该被 .gitignore 忽略")
        return True
    else:
        print("✓ 未发现大于 50MB 的文件")
        return False

def check_git_status():
    """检查Git状态"""
    result = subprocess.run(
        "git status --short",
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    return result.stdout.strip()

def main():
    print("=" * 70)
    print("首次完整推送：上传所有文件到GitHub")
    print("=" * 70)
    
    # 切换到项目目录
    project_path = r"D:\学习\中山大学智能工程学院本科生课程作业"
    os.chdir(project_path)
    print(f"\n工作目录: {os.getcwd()}")
    
    # 步骤1: 检查远程仓库配置
    print("\n" + "=" * 70)
    print("[步骤 1/7] 检查远程仓库配置...")
    print("=" * 70)
    run_command("git remote -v", "查看远程仓库", check=False)
    
    # 步骤2: 检查Git状态
    print("\n" + "=" * 70)
    print("[步骤 2/7] 检查Git状态...")
    print("=" * 70)
    run_command("git status", "检查Git状态", check=False)
    
    # 步骤3: 检查大文件
    print("\n" + "=" * 70)
    print("[步骤 3/7] 检查大文件...")
    print("=" * 70)
    has_large_files = check_large_files()
    if has_large_files:
        print("\n⚠️  警告：发现大文件！")
        print("这些文件应该被 .gitignore 忽略")
        confirm = input("\n继续吗？(yes/no): ")
        if confirm.lower() != "yes":
            print("操作已取消")
            return
    
    # 步骤4: 确保.gitignore正确
    print("\n" + "=" * 70)
    print("[步骤 4/7] 检查.gitignore配置...")
    print("=" * 70)
    if os.path.exists(".gitignore"):
        print("✓ .gitignore 文件存在")
        with open(".gitignore", "r", encoding="utf-8") as f:
            content = f.read()
            if "*.pdf" in content:
                print("✓ PDF文件已在 .gitignore 中")
            if "*.jpg" in content or "*.png" in content:
                print("✓ 图片文件已在 .gitignore 中")
            if "*.zip" in content:
                print("✓ 压缩包已在 .gitignore 中")
    else:
        print("❌ .gitignore 文件不存在！")
        return
    
    # 步骤5: 添加所有文件（.gitignore会自动生效）
    print("\n" + "=" * 70)
    print("[步骤 5/7] 添加文件到Git（.gitignore会自动忽略大文件）...")
    print("=" * 70)
    
    # 先检查是否有未跟踪的文件
    result = subprocess.run(
        "git status --porcelain",
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    if not result.stdout.strip():
        print("✓ 没有需要添加的文件（所有文件都已提交）")
    else:
        print("发现以下更改：")
        print(result.stdout)
        run_command("git add .", "添加所有文件", check=False)
    
    # 步骤6: 检查将要提交的文件大小
    print("\n" + "=" * 70)
    print("[步骤 6/7] 检查将要提交的文件...")
    print("=" * 70)
    
    # 检查暂存区的文件
    result = subprocess.run(
        "git diff --cached --name-only",
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    staged_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
    
    if staged_files:
        print(f"将要提交 {len(staged_files)} 个文件")
        
        # 检查文件大小
        result = subprocess.run(
            'powershell -Command "$files = git diff --cached --name-only; $total = 0; $count = 0; foreach($f in $files) { if($f -and (Test-Path $f)) { $size = (Get-Item $f).Length; $total += $size; $count++; if($size -gt 50MB) { Write-Host \"⚠️  大文件: $f ($([math]::Round($size/1MB, 2)) MB)\" } } }; if($count -gt 0) { Write-Host \"总大小: $([math]::Round($total/1MB, 2)) MB ($count 个文件)\" }"',
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        if result.stdout:
            print(result.stdout.strip())
    else:
        print("✓ 没有文件在暂存区")
    
    # 检查是否有需要提交的更改
    git_status = check_git_status()
    if not git_status:
        print("\n" + "=" * 70)
        print("ℹ️  没有需要提交的更改")
        print("=" * 70)
        print("\n可能的原因：")
        print("1. 所有文件都已经被提交了")
        print("2. 所有文件都被 .gitignore 忽略了")
        print("\n检查远程仓库是否有内容...")
        run_command("git ls-remote origin main", "检查远程分支", check=False)
        
        push_confirm = input("\n是否强制推送当前状态？(yes/no): ")
        if push_confirm.lower() == "yes":
            run_command("git push -f origin main", "强制推送", check=False)
        return
    
    # 步骤7: 创建提交并推送
    print("\n" + "=" * 70)
    print("[步骤 7/7] 创建提交并推送...")
    print("=" * 70)
    
    commit_msg = input("请输入提交信息（直接回车使用默认）: ").strip()
    if not commit_msg:
        commit_msg = "首次完整推送：上传所有课程作业文件"
    
    # 创建提交
    success = run_command(
        f'git commit -m "{commit_msg}"',
        "创建提交",
        check=False
    )
    
    if not success:
        print("\n⚠️  提交可能失败，检查是否有错误...")
        run_command("git status", "检查状态", check=False)
        return
    
    # 配置Git使用更大的缓冲区
    print("\n配置Git推送参数...")
    run_command("git config http.postBuffer 524288000", "配置缓冲区", check=False, show_output=False)
    run_command("git config http.maxRequestBuffer 100M", "配置最大请求缓冲区", check=False, show_output=False)
    
    # 推送到远程
    print("\n正在推送到远程仓库...")
    print("（这可能需要一些时间，请耐心等待）")
    
    success = run_command("git push -u origin main", "推送到远程", check=False)
    
    if success:
        print("\n" + "=" * 70)
        print("✅ 推送成功！")
        print("=" * 70)
        print("\n仓库地址：https://github.com/changyicheng1234/sysu-ise-course-materials")
        print("\n你现在可以在GitHub上查看你的文件了！")
    else:
        print("\n" + "=" * 70)
        print("❌ 推送失败")
        print("=" * 70)
        print("\n可能的原因：")
        print("1. 仍有大文件（>100MB）")
        print("2. 网络连接问题")
        print("3. 认证问题（需要Personal Access Token）")
        print("4. GitHub服务器问题")
        print("\n建议：")
        print("- 检查是否有大于100MB的文件")
        print("- 确认.gitignore正确配置")
        print("- 尝试使用 '彻底清理并推送.py' 脚本")
    
    print("\n按 Enter 键退出...")
    input()

if __name__ == "__main__":
    main()
