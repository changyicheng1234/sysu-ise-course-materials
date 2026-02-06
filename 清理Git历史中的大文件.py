# -*- coding: utf-8 -*-
"""
清理 Git 历史中的大文件
"""
import subprocess
import os
import sys

def run_command(cmd, description, check=True):
    """执行命令并显示结果"""
    print(f"\n[步骤] {description}...")
    print(f"执行命令: {cmd}")
    
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
        if result.stderr:
            # filter-branch 会输出很多信息到 stderr，这是正常的
            if "Rewrite" in result.stderr or "Ref" in result.stderr:
                print(result.stderr)
            elif result.returncode != 0:
                print(f"错误: {result.stderr}", file=sys.stderr)
        
        if check and result.returncode != 0:
            print(f"❌ 命令执行失败，退出码: {result.returncode}")
            return False
        
        print("✓ 完成")
        return True
    except Exception as e:
        print(f"❌ 执行命令时出错: {e}")
        return False

def main():
    print("=" * 60)
    print("清理 Git 历史中的大文件")
    print("=" * 60)
    print("\n⚠️  警告：此操作会重写 Git 历史记录！")
    print("⚠️  建议先备份仓库或创建新分支！")
    
    confirm = input("\n确定要继续吗？(yes/no): ")
    if confirm.lower() != "yes":
        print("操作已取消")
        return
    
    # 切换到项目目录
    project_path = r"D:\学习\中山大学智能工程学院本科生课程作业"
    os.chdir(project_path)
    print(f"\n工作目录: {os.getcwd()}")
    
    # 步骤 1: 移除计算机视觉大目录的历史记录
    print("\n" + "=" * 60)
    print("[步骤 1/5] 移除计算机视觉大目录的历史记录...")
    print("=" * 60)
    print("（这可能需要很长时间，请耐心等待）")
    
    # 构建 filter-branch 命令（PowerShell 兼容的单行命令）
    filter_cmd = (
        'git filter-branch --force --index-filter '
        '"git rm -rf --cached --ignore-unmatch '
        '计算机视觉/Plant-Pathology-sysu-2023-main" '
        '--prune-empty --tag-name-filter cat -- --all'
    )
    
    success = run_command(filter_cmd, "重写历史记录", check=False)
    
    if not success:
        print("\n⚠️  filter-branch 可能已经运行过，继续执行清理步骤...")
    
    # 步骤 2: 清理引用
    print("\n" + "=" * 60)
    print("[步骤 2/5] 清理引用...")
    print("=" * 60)
    run_command(
        "git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin",
        "清理原始引用",
        check=False
    )
    
    # 步骤 3: 清理 reflog
    print("\n" + "=" * 60)
    print("[步骤 3/5] 清理 reflog...")
    print("=" * 60)
    run_command("git reflog expire --expire=now --all", "清理 reflog", check=False)
    
    # 步骤 4: 强制垃圾回收
    print("\n" + "=" * 60)
    print("[步骤 4/5] 强制垃圾回收...")
    print("=" * 60)
    print("（这可能需要一些时间）")
    run_command("git gc --prune=now --aggressive", "强制垃圾回收", check=False)
    
    # 步骤 5: 检查仓库大小
    print("\n" + "=" * 60)
    print("[步骤 5/5] 检查仓库大小...")
    print("=" * 60)
    run_command("git count-objects -vH", "检查仓库大小", check=False)
    
    print("\n" + "=" * 60)
    print("✅ 清理完成！")
    print("=" * 60)
    
    # 询问是否推送
    print("\n下一步：强制推送到远程仓库")
    print("⚠️  注意：强制推送会覆盖远程历史记录！")
    
    push_confirm = input("\n现在推送到远程仓库吗？(yes/no): ")
    if push_confirm.lower() == "yes":
        print("\n正在推送...")
        success = run_command("git push origin --force --all", "强制推送", check=False)
        
        if success:
            print("\n" + "=" * 60)
            print("✅ 推送成功！")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("❌ 推送失败")
            print("=" * 60)
            print("\n可能的原因：")
            print("1. 网络连接问题")
            print("2. GitHub 服务器问题")
            print("3. 需要认证（Personal Access Token）")
    else:
        print("\n已跳过推送，你可以稍后手动执行：")
        print("git push origin --force --all")
    
    print("\n按 Enter 键退出...")
    input()

if __name__ == "__main__":
    main()
