# -*- coding: utf-8 -*-
"""
更新远程仓库URL（仓库改名后使用）
"""
import subprocess
import os

def run_command(cmd, description):
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
            print(f"错误: {result.stderr}")
        
        if result.returncode == 0:
            print("✓ 完成")
            return True
        else:
            print(f"❌ 失败，退出码: {result.returncode}")
            return False
    except Exception as e:
        print(f"❌ 执行命令时出错: {e}")
        return False

def main():
    print("=" * 70)
    print("更新远程仓库URL")
    print("=" * 70)
    
    # 切换到项目目录
    project_path = r"D:\学习\中山大学智能工程学院本科生课程作业"
    os.chdir(project_path)
    print(f"\n工作目录: {os.getcwd()}")
    
    # 步骤1: 检查当前远程URL
    print("\n" + "=" * 70)
    print("[步骤 1/3] 检查当前远程仓库配置...")
    print("=" * 70)
    run_command("git remote -v", "查看远程仓库")
    
    # 步骤2: 更新远程URL
    print("\n" + "=" * 70)
    print("[步骤 2/3] 更新远程仓库URL...")
    print("=" * 70)
    new_url = "https://github.com/changyicheng1234/sysu-ise-course-materials.git"
    run_command(f'git remote set-url origin "{new_url}"', "更新远程URL")
    
    # 步骤3: 验证更新
    print("\n" + "=" * 70)
    print("[步骤 3/3] 验证远程仓库连接...")
    print("=" * 70)
    run_command("git remote -v", "验证远程URL")
    run_command("git fetch origin", "测试连接")
    
    print("\n" + "=" * 70)
    print("✅ 更新完成！")
    print("=" * 70)
    print(f"\n新的仓库地址：{new_url}")
    print("\n现在你可以正常使用以下命令：")
    print("  git push origin main")
    print("  git pull origin main")
    
    print("\n按 Enter 键退出...")
    input()

if __name__ == "__main__":
    main()
