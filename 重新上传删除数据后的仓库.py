# -*- coding: utf-8 -*-
"""
重新上传删除数据后的仓库到 GitHub
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
        if result.stderr and result.returncode != 0:
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
    print("=" * 50)
    print("重新上传删除数据后的仓库到 GitHub")
    print("=" * 50)
    
    # 切换到项目目录
    project_path = r"D:\学习\中山大学智能工程学院本科生课程作业"
    os.chdir(project_path)
    print(f"\n工作目录: {os.getcwd()}")
    
    # 步骤 1: 检查 Git 状态
    run_command("git status", "检查 Git 状态", check=False)
    
    # 步骤 2: 从 Git 索引中移除已删除的文件
    run_command("git add -u", "从 Git 索引中移除已删除的文件", check=False)
    
    # 步骤 3: 移除被 .gitignore 忽略但仍在跟踪的文件
    print("\n[步骤] 移除被 .gitignore 忽略但仍在跟踪的文件...")
    
    # 移除计算机视觉的大目录
    run_command(
        'git rm -r --cached "计算机视觉/Plant-Pathology-sysu-2023-main" -f',
        "移除 计算机视觉/Plant-Pathology-sysu-2023-main",
        check=False
    )
    
    # 移除自然语言处理的大目录
    run_command(
        'git rm -r --cached "自然语言处理/常毅成小组_期中大作业/text-to-lora/text-to-lora" -f',
        "移除 自然语言处理/常毅成小组_期中大作业/text-to-lora/text-to-lora",
        check=False
    )
    
    print("✓ 已尝试移除被忽略的文件")
    
    # 步骤 4: 添加当前文件
    run_command("git add .", "添加当前文件", check=False)
    
    # 步骤 5: 创建提交
    run_command(
        'git commit -m "清理：移除计算机视觉大文件和被忽略的文件"',
        "创建提交",
        check=False
    )
    
    # 步骤 6: 配置 Git 使用更大的缓冲区
    print("\n[步骤] 配置 Git 使用更大的缓冲区...")
    run_command("git config http.postBuffer 524288000", "设置 postBuffer", check=False)
    run_command("git config http.maxRequestBuffer 100M", "设置 maxRequestBuffer", check=False)
    
    # 步骤 7: 推送
    print("\n" + "=" * 50)
    print("准备推送到 GitHub...")
    print("=" * 50)
    
    confirm = input("\n是否现在推送到远程仓库？(yes/no): ")
    if confirm.lower() == 'yes':
        success = run_command(
            "git push -u origin main",
            "推送到 GitHub",
            check=False
        )
        
        if success:
            print("\n" + "=" * 50)
            print("✅ 文件已成功上传到 GitHub！")
            print("=" * 50)
            print("\n仓库地址：https://github.com/changyicheng1234/-")
        else:
            print("\n" + "=" * 50)
            print("❌ 推送失败")
            print("=" * 50)
            print("\n可能的原因：")
            print("1. 仓库中仍有大文件在历史记录中")
            print("2. 网络连接问题")
            print("3. GitHub 服务器问题")
            print("\n建议：如果问题持续，运行 清理Git历史中的大文件.ps1")
    else:
        print("\n已跳过推送，你可以稍后手动执行：git push -u origin main")
    
    print("\n按 Enter 键退出...")
    input()

if __name__ == "__main__":
    main()
