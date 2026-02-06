# -*- coding: utf-8 -*-
"""
移除PDF文件并推送：从Git中移除PDF文件，然后推送其他文件
"""
import subprocess
import os
import sys

def run_command(cmd, description, check=False):
    """执行命令并显示结果"""
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
        
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print(f"错误: {result.stderr}")
        
        if check and result.returncode != 0:
            print(f"❌ 失败，退出码: {result.returncode}")
            return False
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 执行出错: {e}")
        return False

def main():
    print("=" * 70)
    print("移除PDF文件并推送")
    print("=" * 70)
    print("\n这个脚本会：")
    print("1. 从Git中移除所有PDF文件（但保留在本地）")
    print("2. 确保.gitignore包含*.pdf")
    print("3. 添加所有其他文件")
    print("4. 创建提交并推送到GitHub")
    
    confirm = input("\n确定要继续吗？(yes/no): ")
    if confirm.lower() != "yes":
        print("操作已取消")
        return
    
    # 切换到项目目录
    project_path = r"D:\学习\中山大学智能工程学院本科生课程作业"
    os.chdir(project_path)
    print(f"\n工作目录: {os.getcwd()}")
    
    # 步骤1: 检查PDF文件
    print("\n" + "=" * 70)
    print("[步骤 1/6] 检查被Git跟踪的PDF文件")
    print("=" * 70)
    
    result = subprocess.run(
        'git ls-files | findstr /i "\.pdf$"',
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    pdf_files = [f.strip() for f in result.stdout.split('\n') if f.strip()]
    
    if pdf_files:
        print(f"发现 {len(pdf_files)} 个PDF文件被Git跟踪：")
        for pdf in pdf_files[:10]:  # 只显示前10个
            print(f"  - {pdf}")
        if len(pdf_files) > 10:
            print(f"  ... 还有 {len(pdf_files) - 10} 个文件")
    else:
        print("✓ 没有PDF文件被Git跟踪")
    
    # 步骤2: 从Git中移除PDF文件
    if pdf_files:
        print("\n" + "=" * 70)
        print("[步骤 2/6] 从Git中移除PDF文件")
        print("=" * 70)
        
        # 移除所有PDF文件
        for pdf in pdf_files:
            run_command(f'git rm --cached "{pdf}"', f"移除 {pdf}", check=False)
        
        print(f"\n✓ 已从Git中移除 {len(pdf_files)} 个PDF文件")
        print("（文件仍然保留在你的本地磁盘上）")
    
    # 步骤3: 确保.gitignore包含PDF
    print("\n" + "=" * 70)
    print("[步骤 3/6] 检查.gitignore配置")
    print("=" * 70)
    
    if os.path.exists(".gitignore"):
        with open(".gitignore", "r", encoding="utf-8") as f:
            content = f.read()
        
        if "*.pdf" not in content:
            print("⚠️  .gitignore中没有*.pdf，正在添加...")
            with open(".gitignore", "a", encoding="utf-8") as f:
                f.write("\n# PDF文件（通常很大）\n*.pdf\n")
            print("✓ 已添加 *.pdf 到 .gitignore")
        else:
            print("✓ .gitignore 已包含 *.pdf")
    else:
        print("❌ .gitignore 文件不存在！")
        return
    
    # 步骤4: 添加所有其他文件
    print("\n" + "=" * 70)
    print("[步骤 4/6] 添加所有文件（PDF会被自动忽略）")
    print("=" * 70)
    
    run_command("git add .", "添加所有文件", check=False)
    
    # 步骤5: 检查将要提交的文件
    print("\n" + "=" * 70)
    print("[步骤 5/6] 检查将要提交的文件")
    print("=" * 70)
    
    result = subprocess.run(
        "git status --short",
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    if result.stdout.strip():
        print("将要提交的更改：")
        print(result.stdout)
    else:
        print("⚠️  没有文件需要提交")
        print("检查是否有提交历史...")
        result2 = subprocess.run(
            "git log --oneline -1",
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        if result2.stdout.strip():
            print("✓ 已有提交，可以直接推送")
        else:
            print("❌ 没有提交历史，无法推送")
            return
    
    # 步骤6: 创建提交并推送
    print("\n" + "=" * 70)
    print("[步骤 6/6] 创建提交并推送")
    print("=" * 70)
    
    # 检查是否有未提交的更改
    result = subprocess.run(
        "git status --short",
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    if result.stdout.strip():
        commit_msg = input("请输入提交信息（直接回车使用默认）: ").strip()
        if not commit_msg:
            commit_msg = "移除PDF文件并上传其他文件"
        
        run_command(f'git commit -m "{commit_msg}"', "创建提交", check=False)
    
    # 配置推送参数
    run_command("git config http.postBuffer 524288000", "配置缓冲区", check=False, show_output=False)
    run_command("git config http.maxRequestBuffer 100M", "配置最大请求缓冲区", check=False, show_output=False)
    
    print("\n正在推送到远程仓库...")
    print("（这可能需要一些时间，请耐心等待）")
    
    success = run_command("git push -f origin main", "强制推送", check=False)
    
    if success:
        print("\n" + "=" * 70)
        print("✅ 推送成功！")
        print("=" * 70)
        print("\n仓库地址：https://github.com/changyicheng1234/sysu-ise-course-materials")
        print("\n现在可以在GitHub上查看你的文件了！")
        print("\n注意：PDF文件已从Git中移除，但仍在你的本地磁盘上。")
    else:
        print("\n" + "=" * 70)
        print("❌ 推送失败")
        print("=" * 70)
        print("\n可能的原因：")
        print("1. 仍有大文件（>100MB）")
        print("2. 网络连接问题")
        print("3. 认证问题（需要Personal Access Token）")
        print("\n建议：运行 'python 彻底清理并推送.py' 来彻底解决问题")
    
    print("\n按 Enter 键退出...")
    input()

if __name__ == "__main__":
    main()
