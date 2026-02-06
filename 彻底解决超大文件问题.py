# -*- coding: utf-8 -*-
"""
彻底解决超大文件问题：确保所有PDF文件都被忽略
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

def check_tracked_files():
    """检查被跟踪的文件中是否有PDF"""
    print("\n检查被Git跟踪的文件...")
    result = subprocess.run(
        "git ls-files",
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    files = [f.strip() for f in result.stdout.split('\n') if f.strip()]
    pdf_files = [f for f in files if f.lower().endswith('.pdf')]
    
    if pdf_files:
        print(f"\n⚠️  发现 {len(pdf_files)} 个PDF文件被跟踪：")
        for pdf in pdf_files[:10]:  # 只显示前10个
            print(f"  - {pdf}")
        if len(pdf_files) > 10:
            print(f"  ... 还有 {len(pdf_files) - 10} 个PDF文件")
        return pdf_files
    else:
        print("✓ 没有PDF文件被跟踪")
        return []

def main():
    print("=" * 70)
    print("彻底解决超大文件问题")
    print("=" * 70)
    print("\n⚠️  这个脚本会：")
    print("1. 检查并确保.gitignore忽略所有PDF文件")
    print("2. 从Git索引中移除所有PDF文件")
    print("3. 创建新的干净分支（不包含任何PDF文件）")
    print("4. 强制推送到远程仓库")
    print("\n⚠️  注意：这会创建一个全新的分支，丢失Git历史记录")
    
    confirm = input("\n确定要继续吗？(yes/no): ")
    if confirm.lower() != "yes":
        print("操作已取消")
        return
    
    # 切换到项目目录
    project_path = r"D:\学习\中山大学智能工程学院本科生课程作业"
    os.chdir(project_path)
    print(f"\n工作目录: {os.getcwd()}")
    
    # 步骤1: 检查.gitignore
    print("\n" + "=" * 70)
    print("[步骤 1/8] 检查.gitignore配置")
    print("=" * 70)
    
    gitignore_path = os.path.join(project_path, ".gitignore")
    gitignore_updated = False
    
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            gitignore_content = f.read()
            if "*.pdf" not in gitignore_content:
                print("⚠️  .gitignore未配置忽略PDF文件，正在添加...")
                with open(gitignore_path, 'a', encoding='utf-8') as f:
                    f.write("\n# PDF文件（通常很大，必须忽略）\n*.pdf\n")
                print("✓ 已添加PDF忽略规则")
                gitignore_updated = True
            else:
                print("✓ .gitignore已配置忽略PDF文件")
    else:
        print("⚠️  未找到.gitignore文件，正在创建...")
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write("# PDF文件（通常很大，必须忽略）\n*.pdf\n")
        print("✓ 已创建.gitignore文件")
        gitignore_updated = True
    
    # 步骤2: 检查当前分支和状态
    print("\n" + "=" * 70)
    print("[步骤 2/8] 检查当前Git状态")
    print("=" * 70)
    
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
    
    # 步骤3: 检查被跟踪的PDF文件
    print("\n" + "=" * 70)
    print("[步骤 3/8] 检查被跟踪的PDF文件")
    print("=" * 70)
    
    pdf_files = check_tracked_files()
    
    # 步骤4: 从Git索引中移除所有PDF文件
    if pdf_files:
        print("\n" + "=" * 70)
        print("[步骤 4/8] 从Git索引中移除所有PDF文件")
        print("=" * 70)
        
        for pdf_file in pdf_files:
            print(f"移除: {pdf_file}")
            run_command(f'git rm --cached "{pdf_file}"', f"从索引移除 {pdf_file}", check=False, show_output=False)
        
        print(f"\n✓ 已从索引中移除 {len(pdf_files)} 个PDF文件")
    
    # 步骤5: 创建新的孤立分支
    print("\n" + "=" * 70)
    print("[步骤 5/8] 创建新的孤立分支")
    print("=" * 70)
    
    # 检查并清理new-main分支
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
        if current_branch == "new-main":
            # 切换到main或其他分支
            if not run_command("git checkout main", "切换到main分支", check=False, show_output=False):
                run_command("git checkout -b temp-branch", "创建临时分支", check=False, show_output=False)
        run_command("git branch -D new-main", "删除已存在的new-main分支", check=False)
    
    # 创建新的孤立分支
    if not run_command("git checkout --orphan new-main", "创建孤立分支new-main"):
        print("❌ 创建孤立分支失败")
        return
    
    # 步骤6: 清空暂存区并添加文件
    print("\n" + "=" * 70)
    print("[步骤 6/8] 清空暂存区并添加文件")
    print("=" * 70)
    
    run_command("git rm -rf --cached .", "清空暂存区", check=False, show_output=False)
    
    # 添加.gitignore（如果更新了）
    if gitignore_updated:
        run_command("git add .gitignore", "添加.gitignore", check=False, show_output=False)
    
    # 添加所有文件（PDF会被.gitignore自动忽略）
    run_command("git add .", "添加所有文件（PDF会被忽略）", check=False)
    
    # 再次检查是否有PDF文件被添加
    pdf_files_after = check_tracked_files()
    if pdf_files_after:
        print("\n❌ 警告：仍有PDF文件被跟踪！")
        print("这不应该发生，.gitignore可能没有正确配置")
        print("正在手动移除这些PDF文件...")
        for pdf_file in pdf_files_after:
            run_command(f'git rm --cached "{pdf_file}"', f"强制移除 {pdf_file}", check=False, show_output=False)
    
    # 步骤7: 创建提交
    print("\n" + "=" * 70)
    print("[步骤 7/8] 创建初始提交")
    print("=" * 70)
    
    commit_msg = "清理后的新版本：移除所有PDF文件"
    run_command(f'git commit -m "{commit_msg}"', "创建提交", check=False)
    
    # 步骤8: 替换main分支
    print("\n" + "=" * 70)
    print("[步骤 8/8] 替换main分支")
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
    
    # 最终检查
    print("\n最终检查：")
    final_pdf_files = check_tracked_files()
    if final_pdf_files:
        print("\n❌ 仍有PDF文件被跟踪！")
        print("请手动检查.gitignore配置")
    else:
        print("\n✓ 确认：没有PDF文件被跟踪")
    
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
            print("\n✓ 所有PDF文件已从Git中移除")
            print("✓ 这些文件现在只存在于本地，不会被推送到GitHub")
        else:
            print("\n" + "=" * 70)
            print("❌ 推送失败")
            print("=" * 70)
            print("\n可能的原因：")
            print("1. 仍有大文件在Git历史中（需要清理历史）")
            print("2. 网络连接问题")
            print("3. 认证问题")
            print("\n如果仍有大文件错误，可能需要使用git filter-branch清理历史")
    else:
        print("\n已跳过推送，你可以稍后手动执行：")
        print("git push -f origin main")
    
    print("\n按 Enter 键退出...")
    input()

if __name__ == "__main__":
    main()
