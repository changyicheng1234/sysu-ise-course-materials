# -*- coding: utf-8 -*-
"""
检查删除的文件并推送更新
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

def main():
    print("=" * 70)
    print("检查删除的文件并推送更新")
    print("=" * 70)
    
    # 切换到项目目录
    project_path = r"D:\学习\中山大学智能工程学院本科生课程作业"
    os.chdir(project_path)
    print(f"\n工作目录: {os.getcwd()}")
    
    # 步骤1: 检查Git状态
    print("\n" + "=" * 70)
    print("[步骤 1/5] 检查Git状态...")
    print("=" * 70)
    run_command("git status", "检查Git状态", check=False)
    
    # 步骤2: 检查是否有PDF文件被跟踪
    print("\n" + "=" * 70)
    print("[步骤 2/5] 检查是否有PDF文件被Git跟踪...")
    print("=" * 70)
    result = subprocess.run(
        'git ls-files | findstr /i "\.pdf$"',
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    if result.stdout.strip():
        print("发现以下PDF文件被Git跟踪：")
        print(result.stdout)
        print("\n⚠️  这些PDF文件需要从Git中移除")
    else:
        print("✓ 没有PDF文件被Git跟踪")
    
    # 步骤3: 检查.gitignore是否包含PDF
    print("\n" + "=" * 70)
    print("[步骤 3/5] 检查.gitignore配置...")
    print("=" * 70)
    if os.path.exists(".gitignore"):
        with open(".gitignore", "r", encoding="utf-8") as f:
            content = f.read()
            if "*.pdf" in content:
                print("✓ .gitignore 已包含 *.pdf")
            else:
                print("⚠️  .gitignore 未包含 *.pdf，建议添加")
                add_pdf = input("\n是否将 *.pdf 添加到 .gitignore？(yes/no): ")
                if add_pdf.lower() == "yes":
                    with open(".gitignore", "a", encoding="utf-8") as f:
                        f.write("\n# PDF文件（通常很大）\n*.pdf\n")
                    print("✓ 已添加 *.pdf 到 .gitignore")
    
    # 步骤4: 从Git中移除已删除的文件
    print("\n" + "=" * 70)
    print("[步骤 4/5] 从Git中移除已删除的文件...")
    print("=" * 70)
    
    # 检查是否有已删除的文件
    result = subprocess.run(
        "git status --short",
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    has_deleted = False
    if result.stdout:
        for line in result.stdout.split('\n'):
            if line.startswith(' D') or line.startswith('D '):
                has_deleted = True
                break
    
    if has_deleted:
        print("发现已删除的文件，正在从Git中移除...")
        run_command("git add -A", "添加所有更改（包括删除）", check=False)
        print("✓ 已删除的文件已标记")
    else:
        print("✓ 没有需要移除的已删除文件")
    
    # 步骤5: 检查是否有需要提交的更改
    print("\n" + "=" * 70)
    print("[步骤 5/5] 检查是否有需要提交的更改...")
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
        print("有以下更改需要提交：")
        print(result.stdout)
        
        commit_confirm = input("\n是否创建提交？(yes/no): ")
        if commit_confirm.lower() == "yes":
            commit_msg = input("请输入提交信息（直接回车使用默认）: ").strip()
            if not commit_msg:
                commit_msg = "移除大文件PDF并更新.gitignore"
            
            run_command(f'git commit -m "{commit_msg}"', "创建提交", check=False)
            
            # 询问是否推送
            push_confirm = input("\n是否推送到远程仓库？(yes/no): ")
            if push_confirm.lower() == "yes":
                print("\n正在推送...")
                success = run_command("git push origin main", "推送到远程", check=False)
                
                if success:
                    print("\n" + "=" * 70)
                    print("✅ 推送成功！")
                    print("=" * 70)
                else:
                    print("\n" + "=" * 70)
                    print("❌ 推送失败")
                    print("=" * 70)
                    print("\n可能的原因：")
                    print("1. 网络连接问题")
                    print("2. 认证问题（需要Personal Access Token）")
                    print("3. 仍有大文件在Git历史中")
            else:
                print("\n已跳过推送，你可以稍后手动执行：")
                print("git push origin main")
        else:
            print("\n已跳过提交")
    else:
        print("✓ 没有需要提交的更改")
        print("\n说明：")
        print("- 如果文件只是从文件系统中删除，但从未被Git跟踪，则不需要提交")
        print("- 如果文件之前被Git跟踪，需要运行 'git add -A' 然后提交")
    
    print("\n按 Enter 键退出...")
    input()

if __name__ == "__main__":
    main()
