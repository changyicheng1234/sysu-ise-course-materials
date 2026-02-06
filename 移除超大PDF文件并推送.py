# -*- coding: utf-8 -*-
"""
移除超大PDF文件并推送：解决GitHub 100MB文件限制问题
使用创建新孤立分支的方法，避免清理历史的问题
"""
import subprocess
import os
import sys

def run_command(cmd, description, check=False, show_output=True):
    """执行命令并显示结果"""
    if show_output:
        print(f"\n[步骤] {description}...")
        print(f"执行: {cmd}")
    
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
            if result.stderr:
                print("错误:", result.stderr)
        
        if check and result.returncode != 0:
            if show_output:
                print(f"❌ 失败，退出码: {result.returncode}")
            return False
        
        return result.returncode == 0
    except Exception as e:
        if show_output:
            print(f"❌ 执行出错: {e}")
        return False

def main():
    print("=" * 70)
    print("移除超大PDF文件并推送（创建新分支方案）")
    print("=" * 70)
    print("\n⚠️  这个脚本会：")
    print("1. 确保.gitignore正确配置忽略PDF文件")
    print("2. 创建一个新的孤立分支（不包含历史中的大文件）")
    print("3. 添加当前所有文件（PDF会被.gitignore自动忽略）")
    print("4. 替换main分支并强制推送到远程仓库")
    print("\n⚠️  注意：这会创建一个全新的分支，丢失Git历史记录")
    print("    但对于课程作业仓库来说通常不是问题")
    
    confirm = input("\n确定要继续吗？(yes/no): ")
    if confirm.lower() != "yes":
        print("操作已取消")
        return
    
    # 切换到项目目录
    project_path = r"D:\学习\中山大学智能工程学院本科生课程作业"
    os.chdir(project_path)
    print(f"\n工作目录: {os.getcwd()}")
    
    # 步骤1: 检查.gitignore是否忽略PDF
    print("\n" + "=" * 70)
    print("[步骤 1/7] 检查.gitignore配置")
    print("=" * 70)
    
    gitignore_path = os.path.join(project_path, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            gitignore_content = f.read()
            if "*.pdf" in gitignore_content:
                print("✓ .gitignore已配置忽略PDF文件")
            else:
                print("⚠️  .gitignore未配置忽略PDF文件，正在添加...")
                with open(gitignore_path, 'a', encoding='utf-8') as f:
                    f.write("\n# PDF文件（通常很大）\n*.pdf\n")
                print("✓ 已添加PDF忽略规则")
    else:
        print("⚠️  未找到.gitignore文件，正在创建...")
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write("# PDF文件（通常很大）\n*.pdf\n")
        print("✓ 已创建.gitignore文件")
    
    # 步骤2: 检查当前状态
    print("\n" + "=" * 70)
    print("[步骤 2/7] 检查当前Git状态")
    print("=" * 70)
    run_command("git status", "检查Git状态", check=False)
    
    # 步骤3: 创建新的孤立分支
    print("\n" + "=" * 70)
    print("[步骤 3/7] 创建新的孤立分支")
    print("=" * 70)
    
    # 检查当前分支
    result = subprocess.run(
        "git branch --show-current",
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    current_branch = result.stdout.strip()
    print(f"当前分支: {current_branch}")
    
    # 如果new-main分支已存在，先切换到其他分支再删除
    result = subprocess.run(
        "git branch --list new-main",
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    if result.stdout.strip():
        print("⚠️  new-main分支已存在，正在清理...")
        # 如果当前在new-main分支上，先切换到main或其他分支
        if current_branch == "new-main":
            # 尝试切换到main分支
            if not run_command("git checkout main", "切换到main分支", check=False, show_output=False):
                # 如果main不存在，创建一个临时分支
                run_command("git checkout -b temp-branch", "创建临时分支", check=False, show_output=False)
        
        # 删除new-main分支
        run_command("git branch -D new-main", "删除已存在的new-main分支", check=False)
    
    # 创建新的孤立分支
    if not run_command("git checkout --orphan new-main", "创建孤立分支new-main"):
        print("❌ 创建孤立分支失败")
        return
    
    # 步骤4: 清空暂存区
    print("\n" + "=" * 70)
    print("[步骤 4/7] 清空暂存区")
    print("=" * 70)
    run_command("git rm -rf --cached .", "移除所有已跟踪的文件", check=False)
    
    # 步骤5: 添加当前文件（.gitignore会自动忽略PDF）
    print("\n" + "=" * 70)
    print("[步骤 5/7] 添加当前文件（PDF会被.gitignore自动忽略）")
    print("=" * 70)
    run_command("git add .", "添加文件", check=False)
    
    # 检查将要提交的文件
    result = subprocess.run(
        "git status --short",
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    if result.stdout.strip():
        print("\n将要提交的文件：")
        print(result.stdout)
    else:
        print("⚠️  没有文件被添加！")
        print("检查被跟踪的文件...")
        result2 = subprocess.run(
            "git ls-files",
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        files = [f for f in result2.stdout.strip().split('\n') if f.strip()]
        print(f"被Git跟踪的文件数量: {len(files)}")
        if len(files) == 0:
            print("\n❌ 没有文件被跟踪！")
            print("可能所有文件都被.gitignore忽略了")
            return
    
    # 步骤6: 创建提交
    print("\n" + "=" * 70)
    print("[步骤 6/7] 创建初始提交")
    print("=" * 70)
    
    commit_msg = "清理后的新版本：移除所有超大PDF文件"
    run_command(f'git commit -m "{commit_msg}"', "创建提交", check=False)
    
    # 步骤7: 替换main分支
    print("\n" + "=" * 70)
    print("[步骤 7/7] 替换main分支")
    print("=" * 70)
    
    # 切换到main分支（如果存在）
    run_command("git checkout main", "切换到main分支", check=False, show_output=False)
    
    # 删除旧的main分支
    run_command("git branch -D main", "删除旧main分支", check=False, show_output=False)
    
    # 切换回new-main
    run_command("git checkout new-main", "切换回new-main", check=False, show_output=False)
    
    # 重命名为main
    run_command("git branch -m main", "重命名为main", check=False)
    
    print("\n" + "=" * 70)
    print("✅ 本地清理完成！")
    print("=" * 70)
    
    # 询问是否推送
    print("\n下一步：强制推送到远程仓库")
    print("⚠️  注意：强制推送会覆盖远程main分支的所有历史！")
    
    push_confirm = input("\n现在推送到远程仓库吗？(yes/no): ")
    if push_confirm.lower() == "yes":
        print("\n正在推送...")
        print("（这可能需要一些时间，请耐心等待）")
        
        # 配置推送参数
        run_command("git config http.postBuffer 524288000", "配置缓冲区", check=False, show_output=False)
        run_command("git config http.maxRequestBuffer 100M", "配置最大请求缓冲区", check=False, show_output=False)
        
        success = run_command("git push -f origin main", "强制推送", check=False)
        
        if success:
            print("\n" + "=" * 70)
            print("✅ 推送成功！")
            print("=" * 70)
            print("\n仓库地址：https://github.com/changyicheng1234/sysu-ise-course-materials")
            print("\n✓ 超大PDF文件已从Git历史中移除")
            print("✓ 这些文件现在只存在于本地，不会被推送到GitHub")
        else:
            print("\n" + "=" * 70)
            print("❌ 推送失败")
            print("=" * 70)
            print("\n可能的原因：")
            print("1. 仍有大文件（检查.gitignore是否正确）")
            print("2. 网络连接问题")
            print("3. 认证问题（需要Personal Access Token）")
            print("\n建议：")
            print("1. 检查.gitignore配置")
            print("2. 确认工作目录中没有超过100MB的文件")
            print("3. 运行 'git ls-files' 检查被跟踪的文件")
    else:
        print("\n已跳过推送，你可以稍后手动执行：")
        print("git push -f origin main")
    
    print("\n按 Enter 键退出...")
    input()

if __name__ == "__main__":
    main()
