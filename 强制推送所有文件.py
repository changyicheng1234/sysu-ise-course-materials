# -*- coding: utf-8 -*-
"""
强制推送所有文件：确保文件上传到GitHub
"""
import subprocess
import os
import sys

def run_command(cmd, description, check=False):
    """执行命令并显示结果"""
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
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("错误:", result.stderr)
        
        if check and result.returncode != 0:
            print(f"❌ 失败，退出码: {result.returncode}")
            return False
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 执行出错: {e}")
        return False

def main():
    print("=" * 70)
    print("强制推送所有文件到GitHub")
    print("=" * 70)
    print("\n⚠️  这个脚本会：")
    print("1. 添加所有文件（.gitignore会自动忽略大文件）")
    print("2. 创建提交（如果没有提交）")
    print("3. 强制推送到远程仓库")
    print("\n⚠️  注意：这会覆盖远程仓库的内容！")
    
    confirm = input("\n确定要继续吗？(yes/no): ")
    if confirm.lower() != "yes":
        print("操作已取消")
        return
    
    # 切换到项目目录
    project_path = r"D:\学习\中山大学智能工程学院本科生课程作业"
    os.chdir(project_path)
    print(f"\n工作目录: {os.getcwd()}")
    
    # 步骤1: 检查当前状态
    print("\n" + "=" * 70)
    print("[步骤 1/5] 检查当前状态")
    print("=" * 70)
    run_command("git status", "检查Git状态", check=False)
    
    # 步骤2: 添加所有文件
    print("\n" + "=" * 70)
    print("[步骤 2/5] 添加所有文件")
    print("=" * 70)
    run_command("git add .", "添加所有文件", check=False)
    
    # 步骤3: 检查将要提交的文件
    print("\n" + "=" * 70)
    print("[步骤 3/5] 检查将要提交的文件")
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
        print("将要提交的文件：")
        print(result.stdout)
    else:
        # 检查是否有提交
        result2 = subprocess.run(
            "git log --oneline -1",
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result2.stdout.strip():
            print("✓ 没有新文件需要添加，但已有提交")
        else:
            print("⚠️  没有文件被添加！可能所有文件都被.gitignore忽略了")
            print("\n检查被跟踪的文件...")
            result3 = subprocess.run(
                "git ls-files",
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            files = [f for f in result3.stdout.strip().split('\n') if f.strip()]
            print(f"被Git跟踪的文件数量: {len(files)}")
            if len(files) == 0:
                print("\n❌ 没有文件被跟踪！")
                print("\n可能的原因：")
                print("1. 所有文件都被.gitignore忽略了")
                print("2. 需要检查.gitignore配置")
                print("\n建议：运行 'python 诊断仓库为什么是空的.py' 来详细诊断")
                return
    
    # 步骤4: 创建提交
    print("\n" + "=" * 70)
    print("[步骤 4/5] 创建提交")
    print("=" * 70)
    
    # 检查是否已有提交
    result = subprocess.run(
        "git log --oneline -1",
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    if result.stdout.strip():
        print("已有提交，检查是否有新更改...")
        result2 = subprocess.run(
            "git status --short",
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        if result2.stdout.strip():
            commit_msg = input("请输入提交信息（直接回车使用默认）: ").strip()
            if not commit_msg:
                commit_msg = "更新文件：添加上传所有课程作业"
            run_command(f'git commit -m "{commit_msg}"', "创建提交", check=False)
        else:
            print("✓ 没有新更改需要提交")
    else:
        print("⚠️  没有提交历史，创建初始提交...")
        commit_msg = input("请输入提交信息（直接回车使用默认）: ").strip()
        if not commit_msg:
            commit_msg = "初始提交：上传所有课程作业文件"
        run_command(f'git commit -m "{commit_msg}"', "创建初始提交", check=False)
    
    # 步骤5: 强制推送
    print("\n" + "=" * 70)
    print("[步骤 5/5] 强制推送到远程仓库")
    print("=" * 70)
    
    # 配置推送参数（静默执行）
    subprocess.run("git config http.postBuffer 524288000", shell=True, capture_output=True)
    subprocess.run("git config http.maxRequestBuffer 100M", shell=True, capture_output=True)
    print("✓ 已配置推送参数")
    
    print("\n正在强制推送...")
    print("（这可能需要一些时间，请耐心等待）")
    
    success = run_command("git push -f origin main", "强制推送", check=False)
    
    if success:
        print("\n" + "=" * 70)
        print("✅ 推送成功！")
        print("=" * 70)
        print("\n仓库地址：https://github.com/changyicheng1234/sysu-ise-course-materials")
        print("\n现在可以在GitHub上查看你的文件了！")
    else:
        print("\n" + "=" * 70)
        print("❌ 推送失败")
        print("=" * 70)
        print("\n可能的原因：")
        print("1. 仍有大文件（>100MB）")
        print("2. 网络连接问题")
        print("3. 认证问题（需要Personal Access Token）")
        print("4. 所有文件都被.gitignore忽略了")
        print("\n建议：")
        print("1. 运行 'python 诊断仓库为什么是空的.py' 来诊断问题")
        print("2. 运行 'python 彻底清理并推送.py' 来彻底解决问题")
    
    print("\n按 Enter 键退出...")
    input()

if __name__ == "__main__":
    main()
